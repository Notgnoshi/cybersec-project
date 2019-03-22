from django.urls import path
from .apps import PasswordsConfig
from .views import PasswordsPage1View

app_name = PasswordsConfig.name
urlpatterns = [path(PasswordsConfig.module_start_link, PasswordsPage1View.as_view(), name="page1")]
