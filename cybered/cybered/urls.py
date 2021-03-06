"""cybered URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.apps import apps
from shared.src import cybered

urlpatterns = [path("", include("landingpage.urls"), name="landingpage")]

for app_config in apps.get_app_configs():
    if isinstance(app_config, cybered.LessonModule):
        urlpatterns.append(
            path(
                app_config.module_base_link,
                include(app_config.name + ".urls"),
                name="cyberedmodule_" + app_config.name,
            )
        )
