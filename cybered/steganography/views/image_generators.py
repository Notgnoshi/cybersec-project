from ..src import image_tools
from ..apps import SteganographyModule

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.http import Http404

from io import BytesIO
import random
import os


def __exif_encoded_image(file_url, secret_message):
    response = HttpResponse(content_type="image/jpeg")

    file_path = finders.find(file_url)
    image_tools.set_user_comment_exif(file_path, response, secret_message)

    return response


def __bmp_encoded_image(file_url, overlay_url):
    response = HttpResponse(content_type="image/bmp")

    file_path = finders.find(file_url)
    overlay_path = finders.find(overlay_url)
    image_tools.encode_bw_delta_in_greyscale_bmp(file_path, response, overlay_path)

    return response


def __bmp_decoded_image(file_url, overlay_url):
    response = HttpResponse(content_type="image/bmp")

    file_path = finders.find(file_url)
    overlay_path = finders.find(overlay_url)

    buffer = BytesIO()
    image_tools.encode_bw_delta_in_greyscale_bmp(file_path, buffer, overlay_path)
    image_tools.decode_bw_delta_from_greyscale_bmp(file_path, buffer, response, 255)

    return response


def __bmp_intermediate_image(file_url, overlay_url):
    response = HttpResponse(content_type="image/bmp")

    file_path = finders.find(file_url)
    overlay_path = finders.find(overlay_url)

    buffer = BytesIO()
    image_tools.encode_bw_delta_in_greyscale_bmp(file_path, buffer, overlay_path)
    image_tools.decode_bw_delta_from_greyscale_bmp(file_path, buffer, response, 15)

    return response


def __bmp_encoded_text(file_url, secret_message, random_seed):
    response = HttpResponse(content_type="image/bmp")
    file_path = finders.find(file_url)

    reng = random.Random()
    reng.seed(random_seed)
    image_tools.encode_text_delta_in_greyscale_bmp(file_path, response, secret_message, reng)

    return response


def __bmp_intermediate_text(file_url, secret_message, random_seed):
    response = HttpResponse(content_type="image/bmp")
    file_path = finders.find(file_url)

    buffer = BytesIO()

    reng = random.Random()
    reng.seed(random_seed)
    image_tools.encode_text_delta_in_greyscale_bmp(file_path, buffer, secret_message, reng)

    image_tools.decode_bw_delta_from_greyscale_bmp(file_path, buffer, response, 255)

    return response


def original_image(request, key_prefix):
    file_url = request.session[SteganographyModule.scope("{}_image_url".format(key_prefix))]
    return redirect(static(file_url))


def __get_args_from_request(request, key_prefix):
    file_url = request.session.get(SteganographyModule.scope("{}_image_url".format(key_prefix)), "")
    secret_message = request.session.get(
        SteganographyModule.scope("{}_secret_message".format(key_prefix)), ""
    )
    random_seed = request.session.get(
        SteganographyModule.scope("{}_random_seed".format(key_prefix)), ""
    )
    overlay_url = request.session.get(
        SteganographyModule.scope("{}_overlay_url".format(key_prefix)), ""
    )

    return (file_url, secret_message, random_seed, overlay_url)


def encoded_image(request, operation, key_prefix):
    file_url, secret_message, random_seed, overlay_url = __get_args_from_request(
        request, key_prefix
    )

    if operation == 0:
        return __exif_encoded_image(file_url, secret_message)
    elif operation == 1:
        return __bmp_encoded_image(file_url, overlay_url)
    elif operation == 2:
        return __bmp_encoded_text(file_url, secret_message, random_seed)

    raise Http404("Encoded image {} does not exist".format(operation))


def decoded_image(request, operation, key_prefix):
    file_url, secret_message, random_seed, overlay_url = __get_args_from_request(
        request, key_prefix
    )

    if operation == 1:
        return __bmp_decoded_image(file_url, overlay_url)

    raise Http404("Decoded image {} does not exist".format(operation))


def intermediate_image(request, operation, key_prefix):
    file_url, secret_message, random_seed, overlay_url = __get_args_from_request(
        request, key_prefix
    )

    if operation == 1:
        return __bmp_intermediate_image(file_url, overlay_url)
    elif operation == 2:
        return __bmp_intermediate_text(file_url, secret_message, random_seed)

    raise Http404("Intermediate image {} does not exist".format(operation))
