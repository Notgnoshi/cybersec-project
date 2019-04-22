from django.urls import reverse
from django.views.generic import FormView, TemplateView

from passwords.apps import PasswordsModule
from passwords.forms import TextBoxForm, AliceLoginForm

from .mixin import PasswordsMixin

ALICE_USERNAME = "alice@wonderland.org"
ALICE_PASSWORD = "IntoTheLookingGlass"

class PasswordsVerificationView(PasswordsMixin, FormView):
    form_class = AliceLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("verification"))

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("verification_email")] = form.cleaned_data[
            "email"
        ]
        self.request.session[PasswordsModule.scope("verification_password")] = form.cleaned_data[
            "password"
        ]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Only unlock the next page once they have entered the correct password.
        key = PasswordsModule.scope("verification_password")
        if self.request.session.get(key, "") == ALICE_PASSWORD:
            context = super().get_context_data(**kwargs)
        else:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)

        key = PasswordsModule.scope("verification_password")
        verification_password = self.request.session.get(key, "")
        key = PasswordsModule.scope("verification_email")
        verification_email = self.request.session.get(key, "")

        context["actual_password"] = ALICE_PASSWORD
        context["actual_username"] = ALICE_USERNAME
        context["input_email"] = verification_email
        context["input_password"] = verification_password

        return context


class PasswordsVerificationDetailsView(PasswordsMixin, FormView):
    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("verification-details"))

    def form_valid(self, form):
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     # Always lock the next page if there's no data in the session
    #     if PasswordsModule.scope("example_hash_text") in self.request.session:
    #         return super().get_context_data(**kwargs)

    #     page_index = self.kwargs["page_index"]
    #     context = super().get_context_data(disabled_pages=[page_index+1], **kwargs)
    #     return context
