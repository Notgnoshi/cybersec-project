from .base import FormView, TemplateView


class PasswordsBeginView(TemplateView):
    template_name = "passwords/begin.html"
