from django.urls import path
from .apps import PasswordsConfig
from .views import PasswordsBeginView

app_name = PasswordsConfig.name
urlpatterns = [path(PasswordsConfig.module_start_link, PasswordsBeginView.as_view(), name="begin")]
