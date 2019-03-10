from django import forms


class TextBoxForm(forms.Form):
    """A simple textarea-only form."""

    text = forms.CharField(widget=forms.Textarea(), label="")


class TextBoxWithPasswordForm(forms.Form):
    """A textarea form with an extra text box for a password."""

    text = forms.CharField(widget=forms.Textarea(), label="")
    secret_key = forms.CharField(label="Secret Key")
