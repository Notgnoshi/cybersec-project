from django.urls import include, path
from .views import HashingMainPageView
from .apps import HashingConfig

urlpatterns = [
    path(
        HashingConfig.cybered_module_start_link,
        HashingMainPageView.as_view(),
        name="hashing_module_begin",
    )
]
