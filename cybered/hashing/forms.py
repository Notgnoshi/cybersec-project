from django import forms


class TextBoxForm(forms.Form):
    """A simple textarea-only form."""

    text = forms.CharField(widget=forms.Textarea(), label="")
