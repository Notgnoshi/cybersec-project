from ..apps import SteganographyModule

from shared.src import cybered


class SteganographyMixin(SteganographyModule, cybered.PaginatedMixin, cybered.PageMixin):
    pass


class ImageChoicesMixin:
    image_choices = ()
    image_choice_session_key = ""

    def form_valid(self, form):
        """Add validated form data to the user session."""

        self.request.session[
            SteganographyModule.scope(self.image_choice_session_key)
        ] = form.cleaned_data["image_static_url"]

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["name_url_pairs"] = self.image_choices
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["image_list"] = self.image_choices
        return context

