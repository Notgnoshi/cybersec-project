from django.apps import AppConfig

from .src.hashing import HashingModule


class HashingConfig(HashingModule, AppConfig):
    """The django app configuration for the hashing module."""

    pass
