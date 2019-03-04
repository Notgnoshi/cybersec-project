from django.urls import include, path
from .apps import HashingConfig
from .views import HashingMainPageView, HashingExamplesPageView, HashingExamplesResultPageView

app_name = HashingConfig.name
urlpatterns = [
    path(
        HashingConfig.cybered_module_start_link, HashingMainPageView.as_view(), name="hashing_begin"
    ),
    path("hash_examples", HashingExamplesPageView.as_view(), name="hash_examples"),
    path(
        "hash_examples_result", HashingExamplesResultPageView.as_view(), name="hash_examples_result"
    ),
]
