from django.urls import path

from .src.steganography import SteganographyPageManager
from .apps import SteganographyConfig
from .views import *

app_name = SteganographyConfig.name
urlpatterns = cybered.get_paginated_urls(
    [
        SteganographyMainPageView,
        SteganographyImageMetadataPageView,
        SteganographyImageMetadataExampleResultPageView,
        SteganographyImageDeltasPageView,
        SteganographyImageBitPlanesPageView,
    ],
    SteganographyPageManager,
    app_name,
) + [
    path("exif-encoded-image", exif_encoded_image, name="exif_encoded_image"),
    path("exif-original-image", exif_original_image, name="exif_original_image"),
]
