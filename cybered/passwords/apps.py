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
