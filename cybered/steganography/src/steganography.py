from shared.src import cybered


class SteganographyModule(cybered.LessonModule):
    """The cybered module configuration for the steganography module."""

    # The name of this app.
    name = "steganography"

    module_name = "Intro to Steganography"
    module_base_link = "steganography/"
    module_start_link = "begin/"
    module_description = "An introduction to basic steganographic techniques"


class SteganographyPageManager(cybered.PageManager):
    page_list = (
        ("begin", SteganographyModule.module_start_link, "steganography/begin.html"),
        ("image_metadata", "image-metadata/", "steganography/image_metadata.html"),
        (
            "image_metadata_result",
            "image-metadata-example-result/",
            "steganography/image_metadata_result.html",
        ),
        ("image_deltas1", "image-deltas1/", "steganography/image_deltas1.html"),
        ("image_deltas_result1", "image-deltas-result1/", "steganography/image_deltas_result1.html"),
        ("image_deltas2", "image-deltas2/", "steganography/image_deltas2.html"),
        ("image_deltas_result2", "image-deltas-result2/", "steganography/image_deltas_result2.html"),
        ("end", "conclusion/", "steganography/conclusion.html"),
        ("tools", "image-steganography-tools/", "steganography/tools.html"),
    )
