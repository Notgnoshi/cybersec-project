from django.views.generic import FormView as NativeFormView
from django.views.generic import TemplateView as NativeTemplateView

from passwords.apps import PasswordsConfig


class TemplateView(NativeTemplateView):
    def get_context_data(self, **kwargs):
        """Add this module's name to the view's context."""
        context = super().get_context_data(**kwargs)
        # TODO: There's got to be a way to do with with a metaclass or something in such a way that
        # we don't have to copy paste these definitions for each module.
        context["module_name"] = PasswordsConfig.module_name
        return context


class FormView(NativeFormView):
    def get_context_data(self, **kwargs):
        """Add this module's name to the view's context."""
        context = super().get_context_data(**kwargs)
        context["module_name"] = PasswordsConfig.module_name
        return context
