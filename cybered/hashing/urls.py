from django.urls import path

from .apps import HashingConfig
from .views import *

app_name = HashingConfig.name
urlpatterns = [
    path(HashingConfig.module_start_link, HashingMainPageView.as_view(), name="begin"),
    path("motivation", HashingMotivationPageView.as_view(), name="motivation"),
    path("examples-input", HashingExamplesPageView.as_view(), name="examples_form"),
    path("examples-results", HashingExamplesResultPageView.as_view(), name="examples_results"),
    path(
        "keyed-examples-input", HashingKeyedExamplesPageView.as_view(), name="keyed_examples_form"
    ),
    path(
        "keyed-examples-results",
        HashingKeyedExamplesResultPageView.as_view(),
        name="keyed_examples_results",
    ),
]
