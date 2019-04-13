from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from .apps import SteganographyModule

from shared.src import cybered


class SteganographyMixin(SteganographyModule, cybered.PaginatedMixin, cybered.PageMixin):
    pass


class SteganographyMainPageView(SteganographyMixin, TemplateView):
    """The main page for the steganography module."""

    pass


class SteganographyImageMetadataPageView(SteganographyMixin, TemplateView):
    pass




class SteganographyImageDeltasPageView(SteganographyMixin, TemplateView):
    pass


class SteganographyImageBitPlanesPageView(SteganographyMixin, TemplateView):
    pass

