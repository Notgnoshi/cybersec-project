from django.urls import path
from .apps import PasswordsConfig
from .views import (
    PasswordsBeginView,
    PasswordsVerificationView,
    PasswordsVerificationToolView,
    PasswordsCrackingView,
    PasswordsCrackingToolView,
    PasswordsStrengthView,
    PasswordsStrengthToolView,
    PasswordsSaltView,
    PasswordsSaltToolView,
)

app_name = PasswordsConfig.name
urlpatterns = [
    path(PasswordsConfig.module_start_link, PasswordsBeginView.as_view(), name="begin"),
    path("verification", PasswordsVerificationView.as_view(), name="verification"),
    path("verification-tool", PasswordsVerificationToolView.as_view(), name="verification-tool"),
    path("cracking", PasswordsCrackingView.as_view(), name="cracking"),
    path("cracking-tool", PasswordsCrackingToolView.as_view(), name="cracking-tool"),
    path("strength", PasswordsStrengthView.as_view(), name="strength"),
    path("strength-tool", PasswordsStrengthToolView.as_view(), name="strength-tool"),
    path("salt", PasswordsSaltView.as_view(), name="salt"),
    path("salt-tool", PasswordsSaltToolView.as_view(), name="salt-tool"),
]
