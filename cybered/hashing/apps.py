from shared.src.cyberedappconfig import CyberEdAppConfig


class HashingConfig(CyberEdAppConfig):
    """The app configuration for the hashing module."""

    # The name of this app.
    name = "hashing"

    module_name = "Hashing and Message Digests"
    module_base_link = "hashing/"
    module_start_link = "begin"
    # TODO: Come up with a better description than this.
    module_description = "This is a long description of the hashing module."
