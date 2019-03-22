from django.views.generic import TemplateView

from .mixin import PasswordsMixin


class PasswordsBeginView(PasswordsMixin, TemplateView):
    template_name = "passwords/begin.html"
