from passwords.apps import PasswordsModule
from shared.src import cybered


class PasswordsMixin(PasswordsModule, cybered.PageMixin):
    pass
