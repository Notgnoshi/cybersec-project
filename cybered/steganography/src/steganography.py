from shared.src import cybered


class SteganographyPageManager(cybered.PageManager):
    page_list = (
        ("begin", "begin", "steganography/begin.html"),
        ("image_metadata", "image-metadata", "steganography/image_metadata.html"),
        (
            "image_metadata_result",
            "image-metadata-example-result",
            "steganography/image_metadata_result.html",
        ),
        ("image_deltas", "image-deltas", "steganography/image_deltas1.html"),
        ("image_deltas_result1", "image-deltas-result1", "steganography/image_deltas_result1.html"),
        ("image_bitplanes", "image-bitplanes", "steganography/image_bitplanes.html"),
    )


class SteganographyModule(cybered.ModuleMixin):
    """The cybered module configuration for the steganography module."""

    # The name of this app.
    name = "steganography"

    module_name = "Intro to Steganography"
    module_base_link = "steganography/"
    module_start_link = "begin"
    module_description = "An introduction to basic steganographic techniques"

