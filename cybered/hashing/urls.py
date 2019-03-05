from django.urls import path

from .apps import HashingConfig
from .views import HashingExamplesPageView, HashingExamplesResultPageView, HashingMainPageView

app_name = HashingConfig.name
urlpatterns = [
    path(
        HashingConfig.module_start_link, HashingMainPageView.as_view(), name="begin"
    ),
    path("examples-input", HashingExamplesPageView.as_view(), name="examples_form"),
    path(
        "examples-results", HashingExamplesResultPageView.as_view(), name="examples_results"
    ),
]
