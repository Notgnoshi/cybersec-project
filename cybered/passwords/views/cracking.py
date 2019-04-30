from django.urls import reverse
from django.views.generic import FormView, TemplateView

from passwords.apps import PasswordsModule

from .mixin import PasswordsMixin


class PasswordsCrackingView(PasswordsMixin, TemplateView):
    pass


class PasswordsCrackingToolView(PasswordsMixin, TemplateView):
    pass
