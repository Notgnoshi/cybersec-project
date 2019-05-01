from django.views import generic
from django.apps import apps
from shared.src import cybered


class LandingpageView(generic.TemplateView):
    """The landing page view.

    This view searches through the apps in this Django project for AppConfig's that are derived
    from the cybered.AppConfig abstract base class, defining an educational module. If such a module
    is found, it is added to the list of links on the landing page.

    Each module chooses their own base URL, so we must be careful in the unlikely even of a URL
    collision.
    """

    template_name = "landingpage.html"

    def get_context_data(self, **kwargs):
        """Add any apps derived from the cybered.AppConfig base class to this page's context.

        Add a list of modules to the context, and for each module, add the module's base link, name,
        and description.
        """
        context = super().get_context_data(**kwargs)

        modules = []
        for app_config in apps.get_app_configs():
            if isinstance(app_config, cybered.LessonModule):
                module = {}

                # TODO: Prevent collisions in module_base_link
                module["link"] = app_config.module_base_link + app_config.module_start_link
                module["name"] = app_config.module_name
                module["description"] = app_config.module_description

                modules.append(module)

        print("Loading landing page with modules", modules)
        context["modules"] = modules

        return context
