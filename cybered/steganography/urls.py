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
        SteganographyImageDeltasExampleResult1PageView,
        SteganographyImageBitPlanesPageView,
    ],
    SteganographyPageManager,
    app_name,
) + [
    path("exif-encoded-image", exif_encoded_image, name="exif_encoded_image"),
    path("exif-original-image", exif_original_image, name="exif_original_image"),
    path("bmp-encoded-image1", bmp_encoded_image1, name="bmp_encoded_image1"),
    path("bmp-original-image1", bmp_original_image1, name="bmp_original_image1"),
]
