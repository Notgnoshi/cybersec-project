from django.views import generic


class LandingpageView(generic.TemplateView):
    template_name = "landingpage.html"
