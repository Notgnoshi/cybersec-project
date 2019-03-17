from abc import ABCMeta, abstractmethod

class ModuleMixin(metaclass=ABCMeta):
    """An educational module for the CyberEd website.

    An educational module is a linear sequence of pages. A page might contain instructional
    materials, examples, and preferably some kind of interaction to reduce boredom. It is highly
    recommended that each module implement at least one standalone interactive tool that a student
    can repeatedly (ab)use without preventing them from moving on with the instructional content.

    The information in this ModuleMixin is used to automatically discover new modules and add them
    to the landing page. Each derived application must define a module name, base link, start link,
    and description. Dervied classes will likely want to inherit from django.apps.AppConfig so that they
    can be a full-fledged django app.

    Module Mixins also contain a scope() function which can be use along with the django app_name
    variable and the ModuleMixin.name property to reverse project urls.

    See the modules included in this project for examples of how to use app_name, ModuleMix, AppConfig
    and the django reverse() function together.
    """

    @property
    @abstractmethod
    def name(self):
        """Get the name of the module containing the Django application.

        This is the name of the *Python module*, containing the Django application, which implements
        an educational module. This is *not* the same as the `module_name`, which is the natural
        language, long English name of the module that will be displayed on the website.

        A 'name' property is also required by django AppConfig objects; including it here makes
        it easy for new module developers to create a django app that is also a cybered module
        by inheriting from the ModuleMixing before the django AppConfig type
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

    @classmethod
    def scope(this_class, sub_object):
        """Returns the scoped name that django will use
        if app_name is set to this_class.name in the urls.py
        file when the site is loaded.
        """
        return this_class.name + ":" + sub_object
