from django.urls import path

from .apps import SteganographyConfig
from .views import *

app_name = SteganographyConfig.name
urlpatterns = [
    path(SteganographyConfig.module_start_link, SteganographyMainPageView.as_view(), name="begin")
]
