from django.views.generic import TemplateView

from .mixin import PasswordsMixin


class PasswordsBeginView(PasswordsMixin, TemplateView):
    pass


class PasswordsConclusionView(PasswordsMixin, TemplateView):
    pass
