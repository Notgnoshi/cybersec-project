import hashlib

from django.urls import reverse
from django.views.generic import FormView

from passwords.apps import PasswordsModule
from passwords.forms import CrackPasswordsForm
from passwords.src.password_db import (
    COMMON_PASSWORDS,
    DICT_WORDS,
    INSECURE_DB,
    DEE_USERNAME,
    DUM_USERNAME,
)

from .mixin import PasswordsMixin


class PasswordsCrackingView(PasswordsMixin, FormView):
    form_class = CrackPasswordsForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("cracking")) + "#guess-password"

    def form_valid(self, form):
        self.request.session[PasswordsModule.scope("cracking_user")] = form.cleaned_data["choices"]
        self.request.session[PasswordsModule.scope("cracking_attempts")] = (
            self.request.session.get(PasswordsModule.scope("cracking_attempts"), 0) + 1
        )
        if "crack_guess_alpha" in self.request.POST:
            self.request.session[PasswordsModule.scope("cracking_method")] = "crack_guess_alpha"
        else:
            self.request.session[PasswordsModule.scope("cracking_method")] = "crack_guess_common"

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["password_db"] = INSECURE_DB
        context["cracking_attempts"] = self.request.session.get(
            PasswordsModule.scope("cracking_attempts"), 0
        )

        cracked = False
        method = self.request.session.get(PasswordsModule.scope("cracking_method"), "")
        context["cracking_method"] = method
        user = self.request.session.get(PasswordsModule.scope("cracking_user"), "")
        context["cracking_user"] = user

        salt = ""
        actual_hash = ""
        idx = None
        if user == DEE_USERNAME:
            idx = 0
        elif user == DUM_USERNAME:
            idx = 1

        if idx is not None:
            salt = INSECURE_DB[idx][3]
            actual_hash = INSECURE_DB[idx][4]

        context["salt"] = salt
        context["actual_hash"] = actual_hash

        attempts = []
        if method == "crack_guess_alpha":
            for word in DICT_WORDS[:15]:
                _hash = hashlib.md5((salt + word).encode()).hexdigest()
                if _hash == actual_hash:
                    cracked = True
                attempts.append((word, _hash))
        else:
            for word in COMMON_PASSWORDS[:15]:
                _hash = hashlib.md5((salt + word).encode()).hexdigest()
                if _hash == actual_hash:
                    cracked = True
                attempts.append((word, _hash))

        context["attempted_words"] = attempts
        context["cracked"] = cracked

        return context
