from django import forms


class TextBoxForm(forms.Form):
    """A simple textarea-only form."""

    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}), label=""
    )


class TextBoxWithPasswordForm(forms.Form):
    """A textarea form with an extra text box for a password."""

    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}), label="Message"
    )
    secret_key = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), label="Secret Key"
    )
