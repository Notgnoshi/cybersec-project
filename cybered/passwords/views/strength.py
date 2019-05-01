from password_strength import PasswordStats

from django.urls import reverse
from django.views.generic import FormView

from passwords.apps import PasswordsModule
from passwords.forms import PasswordEntropyForm

from .mixin import PasswordsMixin


class PasswordsStrengthView(PasswordsMixin, FormView):
    form_class = PasswordEntropyForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("strength")) + "#entropy-calculator"

    def form_valid(self, form):
        self.request.session["strength_password"] = form.cleaned_data["password"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["password"] = self.request.session.get("strength_password", "")
        context["entropy"] = PasswordStats(context["password"]).entropy_bits if context["password"] else 0

        return context
