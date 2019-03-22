from django.urls import reverse
from django.views.generic import FormView, TemplateView

from passwords.apps import PasswordsModule
from passwords.forms import TextBoxForm

from .mixin import PasswordsMixin


class PasswordsSaltView(PasswordsMixin, TemplateView):
    template_name = "passwords/salt.html"


class PasswordsSaltToolView(PasswordsMixin, FormView):
    template_name = "passwords/salt-tool.html"
    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt-tool"))

    def form_valid(self, form):
        return super().form_valid(form)
