from django.views.generic import TemplateView
from passwords.apps import PasswordsConfig

class PasswordsTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        """Add this module's name to the view's context."""
        context = super().get_context_data(**kwargs)
        context["module_name"] = PasswordsConfig.module_name
        return context

class PasswordsPage1View(PasswordsTemplateView):
    template_name = "passwords/page1.html"
