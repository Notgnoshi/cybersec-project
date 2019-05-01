from shared.src import cybered


class HashingModule(cybered.LessonModule):
    """The cybered module configuration for the hashing module."""

    # The name of this app.
    name = "hashing"

    module_name = "Hashing and Message Digests"
    module_base_link = "hashing/"
    module_start_link = "begin"

    module_description = (
        "An introduction to message digests and their uses in message authentication and integrity"
    )


class HashingPageManager(cybered.PageManager):
    page_list = (
        ("begin", HashingModule.module_start_link, "hashing/begin.html"),
        ("motivation", "motivation", "hashing/motivation.html"),
        ("examples_form", "examples-input", "hashing/examples_form.html"),
        ("examples_results", "examples-results", "hashing/examples_results.html"),
        ("keyed_examples_form", "keyed-examples-input", "hashing/keyed_hashes_form.html"),
        ("keyed_examples_results", "keyed-examples-results", "hashing/keyed_hashes_results.html"),
        ("conclusions", "conclusions", "hashing/conclusion.html"),
        ("tools", "tools", "hashing/tools.html"),
    )
