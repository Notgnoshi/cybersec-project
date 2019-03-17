from abc import ABCMeta, abstractmethod

from django.apps import AppConfig


class CyberEdAppConfig(AppConfig, metaclass=ABCMeta):
    """An educational module for the CyberEd website.

    An educational module is a linear sequence of pages. A page might contain instructional
    materials, examples, and preferably some kind of interaction to reduce boredom. It is highly
    recommended that each module implement at least one standalone interactive tool that a student
    can repeatedly (ab)use without preventing them from moving on with the instructional content.

    The information in this AppConfig is used to automatically discover new modules and add them
    to the landing page. Each derived application must define a module name, base link, start link,
    and description, in addition to whatever definitions AppConfig requires.
    """

    # NOTE: This attribute is required by the AppConfig base class, but we redundantly require it
    # here in order to provide documentation specific to the CyberEd project.
    @property
    @abstractmethod
    def name(self):
        """Get the name of the module containing the Django application.

        This is the name of the *Python module*, containing the Django application, which implements
        an educational module. This is *not* the same as the `module_name`, which is the natural
        language, long English name of the module that will be displayed on the website.
        """

    @property
    @abstractmethod
    def module_name(self):
        """Get the module name.

        The module name should be a long(ish), English, natural language name for the module. For
        example, a module explaining the detailed semantics of underwater basket-weaving and its
        implications in the field of cybersecurity might be named "Underwater Basket-Weaving in
        Cybersecurity". It should be properly capitalized, and not end with any punctuation.
        """

    @property
    @abstractmethod
    def module_base_link(self):
        """Get the module base link.

        The module base link is a kind of namespace inside of which every page in the derived
        application will be hosted.

        Care should be taken to avoid URL collisions, but doing so is left to the module authors.
        """

    @property
    @abstractmethod
    def module_start_link(self):
        """Get the link to the module's first page.

        Since each module is essentially a doubly linked list of pages, we need to know where the
        first page is.
        """

    @property
    @abstractmethod
    def module_description(self):
        """Get the module's long description.

        This is a description of the topic(s) the implemented module teaches, as well as a mention
        of any prerequisites.
        """
