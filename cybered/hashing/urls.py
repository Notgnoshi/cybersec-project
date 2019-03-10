from django.urls import path

from .apps import HashingConfig
from .views import *

app_name = HashingConfig.name
urlpatterns = [
    path("motivation", HashingMotivationPageView.as_view(), name="motivation"),
    path(
        HashingConfig.module_start_link, HashingMainPageView.as_view(), name="begin"
    ),
    path("examples-input", HashingExamplesPageView.as_view(), name="examples_form"),
    path(
        "examples-results", HashingExamplesResultPageView.as_view(), name="examples_results"
    ),
]
