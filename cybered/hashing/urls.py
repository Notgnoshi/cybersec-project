from django.urls import path
from shared.src import cybered

from .src.hashing import HashingPageManager
from .apps import HashingConfig
from .views import *

app_name = HashingConfig.name
urlpatterns = cybered.get_paginated_urls(
    [
        HashingMainPageView,
        HashingMotivationPageView,
        HashingExamplesPageView,
        HashingExamplesResultPageView,
        HashingKeyedExamplesPageView,
        HashingKeyedExamplesResultPageView,
        HashingConclusionPageView,
        HashingToolsPageView,
    ],
    HashingPageManager,
    app_name,
)
