from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.templatetags.static import static

from io import BytesIO
import os

from .apps import SteganographyModule
from .forms import *
from .src import image_tools

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


class SteganographyMainPageView(SteganographyMixin, TemplateView):
    """The main page for the steganography module."""

    pass


class SteganographyImageMetadataPageView(SteganographyMixin,ImageChoicesMixin, FormView):
    form_class = SecretMessageImageForm
    success_url = ""

    image_choice_session_key = "exif_encode_image_url"
    image_choices = (
        ("butterfly_image", "steganography/images/butterfly.jpg"),
        ("cat_image", "steganography/images/cat.jpg"),
        ("peppers_image", "steganography/images/peppers.jpg"),
    )

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(SteganographyModule.scope("image_metadata_result"))

    def form_valid(self, form):
        """Add validated form data to the user session."""

        self.request.session[SteganographyModule.scope("exif_secret_message")] = form.cleaned_data[
            "secret_message"
        ]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = None

        # Always lock the next page if there's no data in the session
        if (
            SteganographyModule.scope("exif_secret_message") in self.request.session
            and SteganographyModule.scope("exif_encode_image_url") in self.request.session
        ):
            context = super().get_context_data(**kwargs)
        else:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)

        return context


class SteganographyImageMetadataExampleResultPageView(SteganographyMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """

        file_path = self.request.session.get(SteganographyModule.scope("exif_encode_image_url"), "")
        secret_message = self.request.session.get(
            SteganographyModule.scope("exif_secret_message"), ""
        )

        return (
            super().dispatch(request, *args, **kwargs)
            if file_path and secret_message
            else redirect(reverse(SteganographyModule.scope("image_metadata")))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file_url = self.request.session[SteganographyModule.scope("exif_encode_image_url")]
        secret_message = self.request.session[SteganographyModule.scope("exif_secret_message")]

        # Add the EXIF tag and pull out the beginning bytes of the file
        file_path = finders.find(file_url)
        buffer = BytesIO()
        image_tools.set_user_comment_exif(file_path, buffer, secret_message)

        context["original_total_size"] = os.path.getsize(file_path)
        context["encoded_total_size"] = buffer.getbuffer().nbytes

        context["original_start_bytes"] = str(
            image_tools.get_starting_n_bytes(file_path, len(secret_message) + 64)
        )[2:-1]

        context["encoded_start_bytes"] = str(
            image_tools.get_starting_n_bytes(buffer, len(secret_message) + 64)
        )[2:-1]

        return context


def exif_encoded_image(request):
    file_url = request.session[SteganographyModule.scope("exif_encode_image_url")]
    secret_message = request.session[SteganographyModule.scope("exif_secret_message")]

    response = HttpResponse(content_type="image/jpeg")

    file_path = finders.find(file_url)
    image_tools.set_user_comment_exif(file_path, response, secret_message)

    return response


def exif_original_image(request):
    file_url = request.session[SteganographyModule.scope("exif_encode_image_url")]
    return redirect(static(file_url))


class SteganographyImageDeltasPageView(SteganographyMixin, ImageChoicesMixin, FormView):
    form_class = ImageForm
    success_url = ""

    image_choice_session_key = "bmp_encode1_image_url"
    image_choices = (
        ("boat_image", "steganography/images/boat_bw.bmp"),
        ("houses_image", "steganography/images/houses_bw.bmp"),
        ("mountain_image", "steganography/images/mountain_bw.bmp"),
    )

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(SteganographyModule.scope("image_deltas_result1"))

    def get_context_data(self, **kwargs):
        context = None

        # Always lock the next page if there's no data in the session
        if (SteganographyModule.scope(self.image_choice_session_key) in self.request.session):
            context = super().get_context_data(**kwargs)
        else:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)

        return context


class SteganographyImageDeltasExampleResult1PageView(SteganographyMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """

        file_path = self.request.session.get(SteganographyModule.scope("bmp_encode1_image_url"), "")

        return (
            super().dispatch(request, *args, **kwargs)
            if file_path
            else redirect(reverse(SteganographyModule.scope("image_deltas")))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file_url = self.request.session[SteganographyModule.scope("bmp_encode1_image_url")]

        # Add the EXIF tag and pull out the beginning bytes of the file
        file_path = finders.find(file_url)
        buffer = BytesIO()
        #image_tools.set_user_comment_exif(file_path, buffer, secret_message)

        return context


def bmp_encoded_image1(request):
    file_url = request.session[SteganographyModule.scope("bmp_encode1_image_url")]

    response = HttpResponse(content_type="image/bmp")

    file_path = finders.find(file_url)
    #image_tools.set_user_comment_exif(file_path, response, secret_message)

    return response


def bmp_original_image1(request):
    file_url = request.session[SteganographyModule.scope("bmp_encode1_image_url")]
    return redirect(static(file_url))


class SteganographyImageBitPlanesPageView(SteganographyMixin, TemplateView):
    pass

