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
        SteganographyImageDeltas1PageView,
        SteganographyImageDeltasExampleResult1PageView,
        SteganographyImageDeltas2PageView,
        SteganographyImageDeltasExampleResult2PageView,
    ],
    SteganographyPageManager,
    app_name,
) + [
    path("original-image/<str:key_prefix>", original_image, name="original_image"),
    path("decoded-image/<int:operation>/<str:key_prefix>", decoded_image, name="decoded_image"),
    path("encoded-image/<int:operation>/<str:key_prefix>", encoded_image, name="encoded_image"),
    path(
        "intermediate-image/<int:operation>/<str:key_prefix>",
        intermediate_image,
        name="intermediate_image",
    ),
]
