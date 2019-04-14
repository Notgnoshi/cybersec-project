from shared.src import cybered

from .apps import PasswordsConfig, PasswordsPageManager
from .views import *

app_name = PasswordsConfig.name
urlpatterns = cybered.get_paginated_urls(
    (
        PasswordsBeginView,
        PasswordsVerificationView,
        PasswordsVerificationToolView,
        PasswordsCrackingView,
        PasswordsCrackingToolView,
        PasswordsStrengthView,
        PasswordsStrengthToolView,
        PasswordsSaltView,
        PasswordsSaltToolView,
    ),
    PasswordsPageManager,
    app_name,
)
