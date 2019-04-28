from ..apps import SteganographyModule

from shared.src import cybered

from django.views.generic import TemplateView


class SteganographyMixin(SteganographyModule, cybered.PaginatedMixin, cybered.PageMixin):
    def get_context_data(self, disabled_pages=[], **kwargs):
        page_index = self.kwargs["page_index"]
        page_count = self.kwargs["page_count"]

        key = SteganographyModule.scope("progress")
        if key not in self.request.session:
            self.request.session[key] = page_index
        self.request.session[key] = max(self.request.session[key], page_index)

        disabled_pages = disabled_pages + list(range(self.request.session[key] + 2, page_count))
        return super().get_context_data(disabled_pages=disabled_pages, **kwargs)


class ImageChoicesMixin:
    image_choices = ()
    image_choice_session_key = ""

    def form_valid(self, form):
        """Add validated form data to the user session."""

        self.request.session[
            SteganographyModule.scope(self.image_choice_session_key)
        ] = form.cleaned_data["image_static_url"]

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["name_url_pairs"] = self.image_choices
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["image_list"] = self.image_choices
        return context


# See https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
class MultiFormView(TemplateView):

    forms = ()
    """ Forms should be a list of 3-tuples, containing 'form name', 'form prefix', and 'form class' """

    def __get_form(self, request, formcls, prefix, name):
        for k in request.POST.keys():
            if k.startswith(prefix):
                return formcls(request.POST, prefix=prefix, **self.get_form_kwargs(name))
        return formcls(None, prefix=prefix, **self.get_form_kwargs(name))

    def __rerender(self):
        return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        return self.__rerender()

    def post(self, request, *args, **kwargs):
        for n, p, f in self.forms:
            f_filled = self.__get_form(request, f, p, n)
            if f_filled.is_bound and f_filled.is_valid():
                return self.form_valid(f_filled, n)

        return self.__rerender()

    def get_context_data(self, **kwargs):
        """ Override to add context for template """
        return dict([(n, f(prefix=p, **self.get_form_kwargs(n))) for n, p, f in self.forms])

    def get_form_kwargs(self, form_name):
        """ Override to add kwargs used to init one of the forms """
        return {}

    def form_valid(self, form, form_name):
        """ Override to handle a valid form and respond with a location to render """
        return self.__rerender()
