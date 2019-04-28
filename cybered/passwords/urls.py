from shared.src import cybered

from .apps import PasswordsConfig, PasswordsPageManager
from .views import *

app_name = PasswordsConfig.name
urlpatterns = cybered.get_paginated_urls(
    (
        PasswordsBeginView,
        PasswordsVerificationView,
        PasswordsVerificationDetailsView,
        PasswordsSaltMotivation1View,
        PasswordsSaltMotivation2View,
        PasswordsSaltView,
        PasswordsCrackingView,
        PasswordsCrackingToolView,
        PasswordsStrengthView,
        PasswordsStrengthToolView,
    ),
    PasswordsPageManager,
    app_name,
)
