from django.urls import include, path
from .views import LandingpageView

urlpatterns = [path("", LandingpageView.as_view(), name="landingpage")]
