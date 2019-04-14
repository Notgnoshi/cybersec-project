from django.urls import reverse
from django.views.generic import FormView, TemplateView

from passwords.apps import PasswordsModule
from passwords.forms import TextBoxForm

from .mixin import PasswordsMixin


class PasswordsSaltView(PasswordsMixin, TemplateView):
    pass


class PasswordsSaltToolView(PasswordsMixin, FormView):
    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        return reverse(PasswordsModule.scope("salt-tool"))

    def form_valid(self, form):
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     # Always lock the next page if there's no data in the session
    #     if PasswordsModule.scope("example_hash_text") in self.request.session:
    #         return super().get_context_data(**kwargs)

    #     page_index = self.kwargs["page_index"]
    #     context = super().get_context_data(disabled_pages=[page_index+1], **kwargs)
    #     return context
