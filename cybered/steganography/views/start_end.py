from django.views.generic import TemplateView

from .shared import *


class SteganographyMainPageView(SteganographyMixin, TemplateView):
    """The main page for the steganography module."""

    pass

