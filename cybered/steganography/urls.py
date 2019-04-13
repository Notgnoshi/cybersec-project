from django.urls import path

from .src.steganography import SteganographyPageManager
from .apps import SteganographyConfig
from .views import *

app_name = SteganographyConfig.name
urlpatterns = cybered.get_paginated_urls(
    [
        SteganographyMainPageView,
        SteganographyImageMetadataPageView,
        SteganographyImageDeltasPageView,
        SteganographyImageBitPlanesPageView,
    ],
    SteganographyPageManager,
    app_name,
)
