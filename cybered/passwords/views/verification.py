import hashlib

from django.urls import reverse
from django.views.generic import FormView

from passwords.apps import PasswordsModule
from passwords.forms import AliceLoginForm
from passwords.src.password_db import ALICE_HASH, ALICE_PASSWORD, ALICE_USERNAME
from passwords.src.password_db import PASSWORD_DB, PASSWORD_DB_USERS

from .mixin import PasswordsMixin


class PasswordsVerificationView(PasswordsMixin, FormView):
    form_class = AliceLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("verification")) + "#login"

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
        input_password = self.request.session.get(key, "")
        input_hash = hashlib.md5(input_password.encode()).hexdigest()
        key = PasswordsModule.scope("verification_email")
        input_email = self.request.session.get(key, "")

        context["actual_password"] = ALICE_PASSWORD
        context["actual_email"] = ALICE_USERNAME
        context["input_email"] = input_email
        context["input_password"] = input_password

        context["password_db"] = PASSWORD_DB
        logged_in = False
        if input_email in PASSWORD_DB_USERS:
            idx = PASSWORD_DB_USERS.index(input_email)
            logged_in = PASSWORD_DB[idx][2] == input_hash
        context["logged_in"] = logged_in

        return context


class PasswordsVerificationDetailsView(PasswordsMixin, FormView):
    form_class = AliceLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("verification-details")) + "#login"

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("details_user")] = form.cleaned_data["email"]
        self.request.session[PasswordsModule.scope("details_password")] = form.cleaned_data[
            "password"
        ]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        key = PasswordsModule.scope("details_password")
        input_password = self.request.session.get(key, "")
        key = PasswordsModule.scope("details_user")
        input_user = self.request.session.get(key, "")

        input_hash = hashlib.md5(input_password.encode()).hexdigest()

        context["actual_user"] = ALICE_USERNAME
        context["actual_password"] = ALICE_PASSWORD
        context["actual_hash"] = ALICE_HASH

        context["input_user"] = input_user
        context["input_password"] = input_password
        context["input_hash"] = input_hash

        context["password_db"] = PASSWORD_DB
        logged_in = False
        if input_user in PASSWORD_DB_USERS:
            idx = PASSWORD_DB_USERS.index(input_user)
            logged_in = PASSWORD_DB[idx][2] == input_hash
        context["logged_in"] = logged_in

        return context
