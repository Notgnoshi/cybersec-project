from abc import ABCMeta, abstractmethod

from django.urls import path


class PaginatorError(TypeError):
    """ Base exception for paginator errors """

    pass


class NoPagesFoundError(PaginatorError):
    """ Indicates that pagination was attempted but no page list was found """

    pass


class PageViewCountMismatchError(PaginatorError):
    """ Indicates that the number of pages in the page list did not match the number 
    of views in the view list """

    pass


class NonPaginatedViewError(PaginatorError):
    """ Indicates that one of the paginated views """

    pass


class PageManager:
    @property
    @abstractmethod
    def page_list(self):
        """Get the list of pages for the module. This only needs to be non-empty if you plan on using the
        cybered pagination code

        This should be a python tuple of tuples, where each of the inner tuples represents
        a page of the module. The page tuple will contain the following three pieces of information, in order
        * Page name - Internal string used to reference the page throughout django and python
        * Page url  - Substring of the url that is used to access the page.
        * Path to template - Subpath to the .html template

        The page url for the first element will be ignored, and module_start_link will be used instead.
        Populating this list and using 
        """
        pass


class PaginatedMixin:

    allow_next_previous_buttons = True
    """Set false in inherited type to never show "Next" and "Previous" buttons on paginator"""
    allow_num_buttons = True
    """Set false in inherited type to never show numeric buttons on paginator"""
    show_disabled_pages = True
    """Set false in inherited type to omit disabled buttons instead of graying them out"""

    def get_context_data(self, disabled_pages=[], **kwargs):
        """ Gets page context data with pagination information included. Indicate any page indexes
        in disabled_pages to disable clicking those page's buttons """

        context = super().get_context_data(**kwargs)

        page_manager = self.kwargs["page_manager"]
        page_index = self.kwargs["page_index"]
        app_name = self.kwargs["app_name"]

        if len(page_manager.page_list) > 0:
            page_list = page_manager.page_list

            def scope(text):
                return "{}:{}".format(app_name, text) if app_name else text

            context_page_list = [
                {"url": scope(page[0]), "enabled": index not in disabled_pages}
                for page, index in zip(page_list, range(len(page_list)))
            ]

            context["paginator"] = {
                "page_index": page_index,
                "page_list": context_page_list,
                "allow_next_prev_buttons": self.allow_next_previous_buttons,
                "allow_num_buttons": self.allow_num_buttons,
                "show_disabled_buttons": self.show_disabled_pages,
            }

            return context


def get_paginated_urls(view_list, page_manager, app_name=""):
    """ Builds a django url patterns list from a page manager and a set of views.
    The page manager must have the same number of pages in its page_list as there
    are views in the view_list. """

    try:
        if len(page_manager.page_list) != len(view_list):
            raise PageViewCountMismatchError()

        urlpatterns = [
            path(
                page[1],
                view.as_view(template_name=page[2]),
                {
                    "page_manager": page_manager,
                    "page_index": index,
                    "app_name": app_name,
                    "page_count": len(view_list),
                },
                name=page[0],
            )
            for page, view, index in zip(page_manager.page_list, view_list, range(len(view_list)))
        ]

        return urlpatterns

    except AttributeError as ae:
        raise NoPagesFoundError() from ae
    except TypeError as te:
        raise NonPaginatedViewError() from te

