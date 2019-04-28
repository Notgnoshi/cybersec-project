import hashlib

from django.urls import reverse
from django.views.generic import FormView

from passwords.apps import PasswordsModule
from passwords.forms import MadhatterLoginForm

from .mixin import PasswordsMixin


ALICE_USERNAME = "alice@wonderland.org"
ALICE_PASSWORD = "IntoTheLookingGlass"
ALICE_HASH = hashlib.md5(ALICE_PASSWORD.encode()).hexdigest()

# Use alice's password for bill too, because I need an example of two users with the same password for the conversation on salting.
PASSWORD_DB = {
    "users": ["mad.hatter@wonderland.org", ALICE_USERNAME, "bill.the.lizard@wonderland.org"],
    "hashes": [hashlib.md5("madhatter".encode()).hexdigest(), ALICE_HASH, ALICE_HASH],
    "passwords": ["madhatter", ALICE_PASSWORD, ALICE_PASSWORD],
}

MADHATTER_USERNAME = PASSWORD_DB["users"][0]
MADHATTER_PASSWORD = PASSWORD_DB["passwords"][0]

HASH_LIST = [
    ("544842c3b9a0d0c1562f555bc12444cd", "pentiumm"),
    ("544894d3b1f5b4ed3ebebc3c0a59bc25", "thisisit"),
    ("54489653fb9e8da76c4dbd03bda11ac2", "just4fun"),
    ("5448c1f319e45c44e2f8b602f899500c", "sibila"),
    ("5449175df9f6179154fa26f238c36e54", "ruairid"),
    ("54491de8a3f2b61da65a7322228d79c7", "madhatter"),
    ("54499e18a660b0d5a978dcf06bb8acec", "crxesi"),
    ("544a0180deb641dc1ca70169dd2a6cbc", "lespaul1"),
    ("544aab8af92829deb945d9f8cd4d5ad4", "7532789"),
    ("544b3befd3b2964fa66cea518c5b3bd7", "g00fy"),
    ("544babc97987d460e6b696a95bf8f7b5", "phpbbmystix"),
    ("544c358ceaf975db88198563ffe2510f", "xp0dxrh"),
]


class PasswordsSaltView(PasswordsMixin, FormView):
    form_class = MadhatterLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt"))

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("salt_email")] = form.cleaned_data["email"]
        self.request.session[PasswordsModule.scope("salt_password")] = form.cleaned_data["password"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Only unlock the next page once they have entered the correct password.
        key = PasswordsModule.scope("salt_password")
        if self.request.session.get(key, "") == MADHATTER_PASSWORD:
            context = super().get_context_data(**kwargs)
        else:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)

        key = PasswordsModule.scope("salt_password")
        input_password = self.request.session.get(key, "")
        input_hash = hashlib.md5(input_password.encode()).hexdigest()
        key = PasswordsModule.scope("salt_email")
        input_email = self.request.session.get(key, "")

        context["actual_password"] = MADHATTER_PASSWORD
        context["actual_email"] = MADHATTER_USERNAME
        context["input_email"] = input_email
        context["input_password"] = input_password

        context["hash_list"] = HASH_LIST
        context["password_db"] = PASSWORD_DB

        logged_in = False
        if input_email in PASSWORD_DB["users"]:
            idx = PASSWORD_DB["users"].index(input_email)
            logged_in = PASSWORD_DB["hashes"][idx] == input_hash
        context["logged_in"] = logged_in

        return context


class PasswordsSaltToolView(PasswordsMixin, FormView):
    form_class = MadhatterLoginForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt-tool"))

    def form_valid(self, form):
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     # Always lock the next page if there's no data in the session
    #     if PasswordsModule.scope("example_hash_text") in self.request.session:
    #         return super().get_context_data(**kwargs)

    #     page_index = self.kwargs["page_index"]
    #     context = super().get_context_data(disabled_pages=[page_index+1], **kwargs)
    #     return context
