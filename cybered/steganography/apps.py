from shared.src import cybered
from django.apps import AppConfig

from .src.steganography import SteganographyModule


class SteganographyConfig(SteganographyModule, AppConfig):
    """The django app configuration for the steganography module."""

    pass
