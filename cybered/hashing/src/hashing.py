from shared.src import cybered


class HashingModule(cybered.ModuleMixin):
    """The cybered module configuration for the hashing module."""

    # The name of this app.
    name = "hashing"

    module_name = "Hashing and Message Digests"
    module_base_link = "hashing/"
    module_start_link = "begin"

    # TODO: Come up with a better description than this.
    module_description = "This is a long description of the hashing module."


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
