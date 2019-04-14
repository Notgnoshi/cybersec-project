from abc import ABCMeta, abstractmethod


class PageMixin:
    """Mixin class that can be added to django template views
    that adds the module name to the view's context.

    If present, the module name is displayed in the header of each page in the module.
    """

    @property
    @abstractmethod
    def module_name(self):
        """Get the module name.

        The module name should be a long(ish), English, natural language name for the module. For
        example, a module explaining the detailed semantics of underwater basket-weaving and its
        implications in the field of cybersecurity might be named "Underwater Basket-Weaving in
        Cybersecurity". It should be properly capitalized, and not end with any punctuation.

        This is the text that will be displayed as the name in the header block of pages
        which inherit the shared header.html template. It is not required that it be the same
        as the module_name defined in the module's ModuleConfig, but it is very easy to
        do so by creating a type that inherits first from the ModuleConfig, then PageMixin, and finally
        a django template page type
        """

    def get_context_data(self, **kwargs):
        """Add this module's name to the view's context."""

        context = super().get_context_data(**kwargs)
        if self.module_name:
            context["module_name"] = self.module_name
        return context
