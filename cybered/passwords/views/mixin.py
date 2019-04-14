from passwords.apps import PasswordsModule
from shared.src import cybered


class PasswordsMixin(PasswordsModule, cybered.PageMixin, cybered.PaginatedMixin):
    """Mixin for the Passwords module that enforces completing the pages in order."""

    def get_context_data(self, disabled_pages=[], **kwargs):
        page_index = self.kwargs["page_index"]
        page_count = self.kwargs["page_count"]

        key = PasswordsModule.scope("progress")
        if key not in self.request.session:
            self.request.session[key] = page_index
        self.request.session[key] = max(self.request.session[key], page_index)

        disabled_pages = disabled_pages + list(range(self.request.session[key] + 2, page_count))
        return super().get_context_data(disabled_pages=disabled_pages, **kwargs)
