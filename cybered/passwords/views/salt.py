import hashlib

from django.urls import reverse
from django.views.generic import FormView

from passwords.apps import PasswordsModule
from passwords.forms import AliceLoginForm, MadhatterLoginForm
from passwords.src.password_db import MADHATTER_PASSWORD, MADHATTER_USERNAME
from passwords.src.password_db import HASH_LIST, PASSWORD_DB, PASSWORD_DB_USERS

from .mixin import PasswordsMixin


class PasswordsSaltMotivation1View(PasswordsMixin, FormView):
    form_class = MadhatterLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt-motivation-1"))

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("salt1_email")] = form.cleaned_data["email"]
        self.request.session[PasswordsModule.scope("salt1_password")] = form.cleaned_data["password"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Only unlock the next page once they have entered the correct password.
        key = PasswordsModule.scope("salt1_password")
        if self.request.session.get(key, "") == MADHATTER_PASSWORD:
            context = super().get_context_data(**kwargs)
        else:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)

        key = PasswordsModule.scope("salt1_password")
        input_password = self.request.session.get(key, "")
        input_hash = hashlib.md5(input_password.encode()).hexdigest()
        key = PasswordsModule.scope("salt1_email")
        input_email = self.request.session.get(key, "")

        context["actual_password"] = MADHATTER_PASSWORD
        context["actual_email"] = MADHATTER_USERNAME
        context["input_email"] = input_email
        context["input_password"] = input_password

        context["hash_list"] = HASH_LIST
        context["password_db"] = PASSWORD_DB

        logged_in = False
        if input_email in PASSWORD_DB_USERS:
            idx = PASSWORD_DB_USERS.index(input_email)
            logged_in = PASSWORD_DB[idx][2] == input_hash
        context["logged_in"] = logged_in

        return context

class PasswordsSaltMotivation2View(PasswordsMixin, FormView):
    form_class = AliceLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt-motivation-2"))

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("salt2_email")] = form.cleaned_data["email"]
        self.request.session[PasswordsModule.scope("salt2_password")] = form.cleaned_data["password"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["password_db"] = PASSWORD_DB

        return context

class PasswordsSaltView(PasswordsMixin, FormView):
    form_class = AliceLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt"))

    def form_valid(self, form):
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     # Always lock the next page if there's no data in the session
    #     if PasswordsModule.scope("example_hash_text") in self.request.session:
    #         return super().get_context_data(**kwargs)

    #     page_index = self.kwargs["page_index"]
    #     context = super().get_context_data(disabled_pages=[page_index+1], **kwargs)
    #     return context
