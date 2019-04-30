import hashlib
import operator

from django.urls import reverse
from django.views.generic import FormView

from passwords.apps import PasswordsModule
from passwords.forms import AliceLoginForm, MadhatterLoginForm, SaltedHashForm
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
        self.request.session[PasswordsModule.scope("salt1_password")] = form.cleaned_data[
            "password"
        ]
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
        self.request.session[PasswordsModule.scope("salt2_password")] = form.cleaned_data[
            "password"
        ]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["password_db"] = PASSWORD_DB

        return context


class PasswordsSaltView(PasswordsMixin, FormView):
    form_class = SaltedHashForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt"))

    def form_valid(self, form):
        salt_rows_key = PasswordsModule.scope("salted_rows")
        password = form.cleaned_data.get("password", "")
        salt = form.cleaned_data.get("salt", "")

        row = (
            salt,
            password,
            hashlib.md5((salt + password).encode()).hexdigest(),
            hashlib.md5(password.encode()).hexdigest(),
        )

        if salt_rows_key not in self.request.session:
            self.request.session[salt_rows_key] = [row]
        else:
            # Avoid adding duplicate rows to the session. This can happen when a user types in a
            # bunch of duplicates, *and* when the page is refreshed due to form resubmission.
            unique_rows = {tuple(r) for r in self.request.session.get(salt_rows_key, [])}
            unique_rows.add(row)
            unique_rows = list(unique_rows)
            unique_rows.sort(key=operator.itemgetter(1))
            # TODO: Figure out if the same password is entered multiple times to highlight it in the table?
            self.request.session[salt_rows_key] = unique_rows

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        salt_rows_key = PasswordsModule.scope("salted_rows")

        if len(self.request.session.get(salt_rows_key, [])) < 3:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)
        else:
            context = super().get_context_data(**kwargs)

        context["num_hashed"] = len(self.request.session.get(salt_rows_key, []))
        context["salt_rows"] = self.request.session.get(salt_rows_key, [])

        return context


class PasswordsSaltDetailsView(PasswordsMixin, FormView):
    form_class = AliceLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt-details"))

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("salt_details_user")] = form.cleaned_data["email"]
        self.request.session[PasswordsModule.scope("salt_details_password")] = form.cleaned_data[
            "password"
        ]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        key = PasswordsModule.scope("salt_details_password")
        input_password = self.request.session.get(key, "")
        key = PasswordsModule.scope("salt_details_user")
        input_user = self.request.session.get(key, "")

        input_hash = ""
        logged_in = False
        if input_user in PASSWORD_DB_USERS:
            idx = PASSWORD_DB_USERS.index(input_user)
            salt = PASSWORD_DB[idx][3]
            input_hash = hashlib.md5((salt + input_password).encode()).hexdigest()
            logged_in = PASSWORD_DB[idx][4] == input_hash

        context["input_user"] = input_user
        context["input_password"] = input_password
        context["input_hash"] = input_hash

        context["password_db"] = PASSWORD_DB
        context["password_db_users"] = PASSWORD_DB_USERS
        context["logged_in"] = logged_in

        return context
