from django.views import generic
from django.apps import apps
from shared.src.cyberedappconfig import CyberEdAppConfig


class LandingpageView(generic.TemplateView):
    template_name = "landingpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        modules = []
        for app_config in apps.get_app_configs():
            if isinstance(app_config, CyberEdAppConfig):
                module = {}

                # TODO: Prevent collisions in module_base_link
                module["link"] = app_config.module_base_link + app_config.module_start_link
                module["name"] = app_config.module_name
                module["description"] = app_config.module_description

                modules.append(module)

        print("Loading landing page with modules", modules)
        context["modules"] = modules

        return context
