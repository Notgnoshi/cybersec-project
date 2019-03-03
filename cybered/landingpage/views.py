from django.views import generic
from django.apps import apps
from shared.src.cyberedappconfig import CyberEdAppConfig


class LandingpageView(generic.TemplateView):
    template_name = "landingpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cybered_module_list = []
        for app_cfg in apps.get_app_configs():
            if isinstance(app_cfg, CyberEdAppConfig):
                this_module = {}
                this_module["link"] = (
                    app_cfg.cybered_module_base_link + app_cfg.cybered_module_start_link
                )
                this_module["buttonid"] = "frm1_submit_" + app_cfg.name
                this_module["name"] = app_cfg.cybered_module_name

                cybered_module_list.append(this_module)

        print("Loading landing page with modules", cybered_module_list)
        context["cybered_module_list"] = cybered_module_list

        return context
