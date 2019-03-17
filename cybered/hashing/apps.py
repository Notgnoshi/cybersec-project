from shared.src import cybered
from django.apps import AppConfig

class HashingModule(cybered.ModuleMixin):
    """The cybered module configuration for the hashing module."""

    # The name of this app.
    name = "hashing"

    module_name = "Hashing and Message Digests"
    module_base_link = "hashing/"
    module_start_link = "begin"

    # TODO: Come up with a better description than this.
    module_description = "This is a long description of the hashing module."


class HashingConfig(HashingModule, AppConfig):
    """The django app configuration for the hashing module."""
    pass