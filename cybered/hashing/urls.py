from django.urls import path

from .apps import HashingConfig
from .views import HashingExamplesPageView, HashingExamplesResultPageView, HashingMainPageView

app_name = HashingConfig.name
urlpatterns = [
    path(
        HashingConfig.module_start_link, HashingMainPageView.as_view(), name="hashing_begin"
    ),
    path("hash_examples", HashingExamplesPageView.as_view(), name="hash_examples"),
    path(
        "hash_examples_result", HashingExamplesResultPageView.as_view(), name="hash_examples_result"
    ),
]
