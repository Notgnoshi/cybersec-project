from django.urls import path
from .views import LandingpageView

app_name = "landingpage"
urlpatterns = [path("", LandingpageView.as_view(), name="index")]
