import random
import string

from django import forms

from passwords.src.password_db import DEE_USERNAME, DUM_USERNAME


def _gen_random_salt():
    SIZE = 12
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(SIZE))


class SaltedHashForm(forms.Form):
    """A simple form to compute the hash of a salted value."""

    salt = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Salt",
        initial=_gen_random_salt,
    )

    password = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}),
        label="Password",
    )


class AliceLoginForm(forms.Form):
    """A sample login form with email and password."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "alice@wonderland.org"}
        ),
        label="Email",
        initial="alice@wonderland.org",
        # disabled=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "off"}),
        label="Password",
    )


class MadhatterLoginForm(forms.Form):
    """A sample login form with email and password."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "mad.hatter@wonderland.org"}
        ),
        label="Email",
        initial="mad.hatter@wonderland.org",
        # disabled=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "off"}),
        label="Password",
    )


class CrackPasswordsForm(forms.Form):
    choices = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        choices=((DEE_USERNAME, DEE_USERNAME), (DUM_USERNAME, DUM_USERNAME)),
        label="User",
    )


class PasswordEntropyForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "off"}),
        label="Password",
    )
