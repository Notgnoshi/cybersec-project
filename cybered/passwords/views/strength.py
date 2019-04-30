from django.urls import reverse
from django.views.generic import FormView, TemplateView

from passwords.apps import PasswordsModule

from .mixin import PasswordsMixin


class PasswordsStrengthView(PasswordsMixin, TemplateView):
    pass


class PasswordsStrengthToolView(PasswordsMixin, TemplateView):
    pass
