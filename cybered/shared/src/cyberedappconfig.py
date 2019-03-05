from abc import ABCMeta, abstractmethod

from django.apps import AppConfig


class CyberEdAppConfig(AppConfig, metaclass=ABCMeta):
    """An educational module for the CyberEd website."""

    @property
    @abstractmethod
    def module_name(self):
        """Get the long, descriptive module name."""

    @property
    @abstractmethod
    def module_base_link(self):
        """Get the module base link."""

    @property
    @abstractmethod
    def module_start_link(self):
        """Get the link to the module's first page."""

    @property
    @abstractmethod
    def module_description(self):
        """Get the module's long description."""
