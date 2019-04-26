from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.templatetags.static import static

from io import BytesIO
import random
import os
import time
import threading

# Lock to prevent nondeterministic response orders to the functions
# that use randomization
random_module_lock = threading.Lock()


from ..apps import SteganographyModule
from ..forms import *
from ..src import image_tools

from .shared import *


class SteganographyImageDeltas2PageView(SteganographyMixin, ImageChoicesMixin, FormView):
    form_class = SecretMessageImageForm
    success_url = ""

    image_choice_session_key = "bmp_encode2_image_url"
    image_choices = (
        ("boat_image", "steganography/images/boat_bw.bmp"),
        ("houses_image", "steganography/images/houses_bw.bmp"),
        ("mountain_image", "steganography/images/mountain_bw.bmp"),
    )

    def form_valid(self, form):
        """Add validated form data to the user session."""

        self.request.session[SteganographyModule.scope("bmp_secret_message")] = form.cleaned_data[
            "secret_message"
        ]

        # Save a seed value to make sure the 'random' pixels chosen when generating the images
        # are the same until the user picks a new image
        self.request.session[SteganographyModule.scope("bmp_random_seed")] = int(time.time())

        return super().form_valid(form)

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(SteganographyModule.scope("image_deltas_result2"))

    def get_context_data(self, **kwargs):
        context = None

        # Always lock the next page if there's no data in the session
        if (
            SteganographyModule.scope(self.image_choice_session_key) in self.request.session
            and SteganographyModule.scope("bmp_secret_message") in self.request.session
        ):
            context = super().get_context_data(**kwargs)
        else:
            page_index = self.kwargs["page_index"]
            context = super().get_context_data(disabled_pages=[page_index + 1], **kwargs)

        return context


class SteganographyImageDeltasExampleResult2PageView(SteganographyMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """

        file_path = self.request.session.get(SteganographyModule.scope("bmp_encode2_image_url"), "")
        secret_message = self.request.session.get(
            SteganographyModule.scope("bmp_secret_message"), ""
        )

        return (
            super().dispatch(request, *args, **kwargs)
            if file_path and secret_message
            else redirect(reverse(SteganographyModule.scope("image_deltas2")))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file_url = self.request.session[SteganographyModule.scope("bmp_encode2_image_url")]
        secret_message = self.request.session[SteganographyModule.scope("bmp_secret_message")]
        random_seed = self.request.session[SteganographyModule.scope("bmp_random_seed")]

        buffer = BytesIO()
        file_path = finders.find(file_url)

        with random_module_lock:
            random.seed(random_seed)
            image_tools.encode_text_delta_in_greyscale_bmp(file_path, buffer, secret_message)

        context["decoded_message"] = image_tools.decode_text_delta_from_greyscale_bmp(
            file_path, buffer
        )

        return context


def bmp_encoded_image2(request):
    file_url = request.session[SteganographyModule.scope("bmp_encode2_image_url")]
    secret_message = request.session[SteganographyModule.scope("bmp_secret_message")]
    random_seed = request.session[SteganographyModule.scope("bmp_random_seed")]

    response = HttpResponse(content_type="image/bmp")
    file_path = finders.find(file_url)

    with random_module_lock:
        random.seed(random_seed)
        image_tools.encode_text_delta_in_greyscale_bmp(file_path, response, secret_message)

    return response


def bmp_decoded_image2(request):
    file_url = request.session[SteganographyModule.scope("bmp_encode2_image_url")]
    secret_message = request.session[SteganographyModule.scope("bmp_secret_message")]
    random_seed = request.session[SteganographyModule.scope("bmp_random_seed")]

    response = HttpResponse(content_type="image/bmp")
    file_path = finders.find(file_url)

    buffer = BytesIO()
    with random_module_lock:
        random.seed(random_seed)
        image_tools.encode_text_delta_in_greyscale_bmp(file_path, buffer, secret_message)

    image_tools.decode_bw_delta_from_greyscale_bmp(file_path, buffer, response, 255)

    return response


def bmp_original_image2(request):
    file_url = request.session[SteganographyModule.scope("bmp_encode2_image_url")]
    return redirect(static(file_url))

