from django import forms


class TextBoxForm(forms.Form):
    """A simple textarea-only form."""

    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}), label=""
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
