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

from ..apps import SteganographyModule
from ..forms import *
from ..src import image_tools

from .shared import *


class SteganographyMainPageView(SteganographyMixin, TemplateView):
    """The main page for the steganography module."""

    pass


class SteganographyConclusionPageView(SteganographyMixin, TemplateView):
    """The conclusion page for the steganography module."""

    pass


class SteganographyToolsPageView(SteganographyMixin, MultiFormView):
    """The tools page for the steganography module."""

    forms = (
        ("img_img_form", "img_img", ImageForm),
        ("msg_img_form", "msg_img", SecretMessageImageForm),
        ("msg_hdr_form", "msg_hdr", SecretMessageImageForm),
    )

    image_in_image_choices = (
        ("img_img-boat", "steganography/images/boat_bw.bmp"),
        ("img_img-houses", "steganography/images/houses_bw.bmp"),
        ("img_img-mountain", "steganography/images/mountain_bw.bmp"),
    )

    text_in_image_choices = (
        ("msg_img-boat", "steganography/images/boat_bw.bmp"),
        ("msg_img-houses", "steganography/images/houses_bw.bmp"),
        ("msg_img-mountain", "steganography/images/mountain_bw.bmp"),
    )

    text_in_comment_images = (
        ("msg_hdr-butterfly", "steganography/images/butterfly.jpg"),
        ("msg_hdr-cat_image", "steganography/images/cat.jpg"),
        ("msg_hdr-peppers_image", "steganography/images/peppers.jpg"),
    )

    bw_images = (
        "steganography/images/face_overlay.bmp",
        "steganography/images/qmark_overlay.bmp",
        "steganography/images/rad_overlay.bmp",
    )

    def get_form_kwargs(self, form_name):
        kwargs = super().get_form_kwargs(form_name)

        if form_name == "img_img_form":
            kwargs["name_url_pairs"] = self.image_in_image_choices
        elif form_name == "msg_img_form":
            kwargs["name_url_pairs"] = self.text_in_image_choices
        elif form_name == "msg_hdr_form":
            kwargs["name_url_pairs"] = self.text_in_comment_images
        else:
            raise Exception()

        return kwargs

    def form_valid(self, form, form_name):
        """Add validated form data to the user session."""

        self.request.session[SteganographyModule.scope("tools_image_url")] = form.cleaned_data[
            "image_static_url"
        ]

        self.request.session[
            SteganographyModule.scope("tools_secret_message")
        ] = form.cleaned_data.get("secret_message", "")

        self.request.session[SteganographyModule.scope("tools_image_name")] = form.cleaned_data[
            "image_name"
        ]

        self.request.session[SteganographyModule.scope("tools_overlay_url")] = random.choice(
            self.bw_images
        )

        # Save a seed value to make sure the 'random' pixels chosen when generating the images
        # are the same until the user picks a new image
        self.request.session[SteganographyModule.scope("tools_random_seed")] = int(time.time())

        # Redisplay same page; we'll fill context data to add the result
        return super().form_valid(form, form_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file_url = self.request.session[SteganographyModule.scope("tools_image_url")]
        secret_message = self.request.session[SteganographyModule.scope("tools_secret_message")]
        random_seed = self.request.session[SteganographyModule.scope("tools_random_seed")]

        context["image_in_image_choices"] = self.image_in_image_choices
        context["text_in_image_choices"] = self.text_in_image_choices
        context["text_in_comment_choices"] = self.text_in_comment_images

        # Previously submitted, fill out the results info
        image_name = self.request.session.get(SteganographyModule.scope("tools_image_name"), None)
        if image_name:
            if image_name.startswith("img_img"):
                context["show_image_in_image_results"] = True

            elif image_name.startswith("msg_img"):
                context["show_text_in_image_results"] = True

                buffer = BytesIO()
                file_path = finders.find(file_url)

                reng = random.Random()
                reng.seed(random_seed)
                image_tools.encode_text_delta_in_greyscale_bmp(
                    file_path, buffer, secret_message, reng
                )

                context["decoded_message"] = image_tools.decode_text_delta_from_greyscale_bmp(
                    file_path, buffer
                )

            elif image_name.startswith("msg_hdr"):
                context["show_text_in_metadata_results"] = True

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
            else:
                raise Exception()

        return context

