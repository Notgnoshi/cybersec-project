from shared.src import cybered


class SteganographyModule(cybered.ModuleMixin):
    """The cybered module configuration for the steganography module."""

    # The name of this app.
    name = "steganography"

    module_name = "Intro to Steganography"
    module_base_link = "steganography/"
    module_start_link = "begin"
    module_description = "An introduction to basic steganographic techniques"

