from django.apps import AppConfig

from shared.src import cybered


class PasswordsModule(cybered.ModuleMixin):
    """The cybered module configuration for the passwords module."""

    name = "passwords"
    module_name = "Password Security and Cracking"
    module_base_link = "passwords/"
    module_start_link = "begin/"
    module_description = "A look at what makes passwords secure and common attempts to crack them."


class PasswordsConfig(PasswordsModule, AppConfig):
    """The django app configuration for the passwords module."""


class PasswordsPageManager(cybered.PageManager):
    page_list = (
        # ('name', 'url', 'template')
        ("begin", PasswordsModule.module_start_link, "passwords/begin.html"),
        ("verification", "verification", "passwords/verification.html"),
        ("verification-details", "verification-details", "passwords/verification-details.html"),
        ("salt-motivation-1", "salt-motivation-1", "passwords/salt-motivation-1.html"),
        ("salt-motivation-2", "salt-motivation-2", "passwords/salt-motivation-2.html"),
        ("salt", "salt", "passwords/salt.html"),
        ("salt-details", "salt-details", "passwords/salt-details.html"),
        ("cracking", "cracking", "passwords/cracking.html"),
        ("strength", "strength", "passwords/strength.html"),
    )
