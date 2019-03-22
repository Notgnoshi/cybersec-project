from django.urls import reverse
from django.views.generic import FormView, TemplateView

from passwords.apps import PasswordsModule
from passwords.forms import TextBoxForm

from .mixin import PasswordsMixin


class PasswordsVerificationView(PasswordsMixin, TemplateView):
    template_name = "passwords/verification.html"


class PasswordsVerificationToolView(PasswordsMixin, FormView):
    template_name = "passwords/verification-tool.html"
    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("verification-tool"))

    def form_valid(self, form):
        return super().form_valid(form)
