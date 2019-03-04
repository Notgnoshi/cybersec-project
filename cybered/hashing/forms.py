from django import forms


class TextBoxForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label="")
