from PIL import Image, TiffTags
from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import ImageFileDirectory_v2

from pathlib import Path
from io import BytesIO
import random

__JPG_FORMAT_STR = "JPEG"
__BMP_FORMAT_STR = "BMP"

# See https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ExifTags.html
# as source for how we're handling EXIF tags here
__EXIF_KEY_STR = "parsed_exif"
__USER_COMMENT_TAG = "UserComment"
__EXIF_STRING_TYPE = 2
__TAGS_r = dict(((v, k) for k, v in TAGS.items()))


class ImageToolError(Exception):
    pass


def to_path(path_or_str):
    return path_or_str if isinstance(path_or_str, Path) else Path(path_or_str)


def get_starting_n_bytes(fp, count):
    # After input is resolved, call this to actually
    # read the data
    def get_bytes(fp, count):
        curr_loc = fp.tell()

        fp.seek(0, 2)
        max_size = fp.tell()

        fp.seek(0)
        result = fp.read(min(count, max_size))

        fp.seek(curr_loc)
        return result

    # Resolve input to a file pointer
    # Try to open file pointer to fp, if that fails with a type error,
    # assume it's already a readable object
    try:
        with to_path(fp).open(mode="rb") as fp:
            return get_bytes(fp, count)
    except TypeError:
        return get_bytes(fp, count)



def get_user_comment_exif_bytes(user_comment=""):
    """ Returns the bytes for EXIF tags containing only the given user comment """
    ifd = ImageFileDirectory_v2()
    ifd[__TAGS_r[__USER_COMMENT_TAG]] = user_comment
    ifd.tagtype[__TAGS_r[__USER_COMMENT_TAG]] = __EXIF_STRING_TYPE

    out = BytesIO()
    ifd.save(out)

    exif = b"Exif\x00\x00" + out.getvalue()
    return exif


def clear_exifs(image_dir):
    img_dir = to_path(image_dir)

    for img_path in img_dir.iterdir():
        set_exif(img_path, img_path, b"")


def get_user_comment_exif(fp):
    """ Gets the UserComment EXIF tag from an image """
    try:
        img_obj = Image.open(fp)
        if img_obj.format is not __JPG_FORMAT_STR:
            raise ImageToolError("File at", str(fp), "is not jpeg")

        user_comment_tag = __TAGS_r[__USER_COMMENT_TAG]
        return (
            img_obj.info[__EXIF_KEY_STR][user_comment_tag]
            if __EXIF_KEY_STR in img_obj.info and user_comment_tag in img_obj.info[__EXIF_KEY_STR]
            else ""
        )
    except IOError as err:
        raise ImageToolError("Unable to read/write", str(fp)) from err


def set_user_comment_exif(input_fp, output_fp, user_comment_str=""):
    """ Sets the EXIF tags for a JPG image to containly only the given User Comment"""

    set_exif(input_fp, output_fp, get_user_comment_exif_bytes(user_comment_str))


def set_exif(input_fp, output_fp, exif_bytes=b""):
    """ Sets the EXIF tags for a JPG image"""
    try:
        img_obj = Image.open(input_fp)
        if img_obj.format is not __JPG_FORMAT_STR:
            raise ImageToolError("File at", str(input_fp), "is not jpeg")

        if exif_bytes is not None:
            img_obj.save(output_fp, exif=exif_bytes, format=__JPG_FORMAT_STR)
        else:
            img_obj.save(output_fp, format=__JPG_FORMAT_STR)
    except IOError as err:
        raise ImageToolError("Unable to read/write", str(input_fp), "->", str(output_fp)) from err


def encode_bw_delta_in_greyscale_bmp(input_fp, output_fp, hidden_fp):
    """ Hides a black and white image in a greyscale image by
        modifying all pixels by +1 or -1 if they correspond to
        a black pixel in the input black and white image """

    # PIL appears to break if given a Path object for some of these operations?
    input_fp = str(input_fp) if isinstance(input_fp, Path) else input_fp
    output_fp = str(output_fp) if isinstance(output_fp, Path) else output_fp
    hidden_fp = str(hidden_fp) if isinstance(hidden_fp, Path) else hidden_fp

    try:
        img_obj = Image.open(input_fp).convert("L")
        overlay_obj = Image.open(hidden_fp).convert("L")

        w, h = img_obj.size
        overlay_obj = overlay_obj.resize((w, h), Image.NEAREST)

        img_data = img_obj.getdata()
        overlay_data = overlay_obj.getdata()
        result_data = [
            orig if over > 0 else (orig + 1 if orig < 255 else orig - 1)
            for orig, over in zip(img_data, overlay_data)
        ]

        img_obj.putdata(result_data)
        img_obj.save(output_fp, __BMP_FORMAT_STR)
    except IOError as err:
        raise ImageToolError(
            "Unable to read/write", str(input_fp), ",", str(overlay_obj), "->", str(output_fp)
        ) from err


def decode_bw_delta_from_greyscale_bmp(input_fp1, input_fp2, delta_fp, white_value=255):
    """ Diffs two images and returns a black and white delta image
    where every pixel that differed in the input images is black """

    # PIL appears to break if given a Path object for some of these operations?
    input_fp1 = str(input_fp1) if isinstance(input_fp1, Path) else input_fp1
    input_fp2 = str(input_fp2) if isinstance(input_fp2, Path) else input_fp2
    delta_fp = str(delta_fp) if isinstance(delta_fp, Path) else delta_fp

    try:
        img1_obj = Image.open(input_fp1).convert("L")
        img2_obj = Image.open(input_fp2).convert("L")

        if img1_obj.width != img2_obj.width or img1_obj.height != img2_obj.height:
            raise ImageToolError("Cannot find delta for differently sized images")

        data1 = img1_obj.getdata()
        data2 = img2_obj.getdata()

        result_data = [0 if a != b else white_value for a, b in zip(data1, data2)]

        img1_obj.putdata(result_data)
        img1_obj.save(delta_fp, __BMP_FORMAT_STR)
    except IOError as err:
        raise ImageToolError(
            "Unable to read/write", str(input_fp1), ",", str(input_fp2), "->", str(delta_fp)
        ) from err


def encode_text_delta_in_greyscale_bmp(input_fp, output_fp, hidden_message, reng=random):
    """ Hides a black and white image in a greyscale image by
        modifying all pixels by a value in [-13, 13] corresponding to the 26 letters
        of the alphabet. Non-alphabetic characters are ignored. If the message
        is too long to encode in the image, it will be truncated """

    # PIL appears to break if given a Path object for some of these operations?
    input_fp = str(input_fp) if isinstance(input_fp, Path) else input_fp
    output_fp = str(output_fp) if isinstance(output_fp, Path) else output_fp

    try:
        img_obj = Image.open(input_fp).convert("L")
        img_data = list(img_obj.getdata())

        # Get a list of the pixels that are at least 13 values away from 0, 255
        # so we know we can use them to encode
        modify_pixel_options = list(
            map(
                lambda pair: pair[0],
                filter(
                    lambda pair: pair[1] >= 13 or pair[1] <= 242,
                    zip(range(len(img_data)), img_data),
                ),
            )
        )

        # Filter message to letters only, then truncate the message to make sure we have enough pixels for it
        hidden_message = "".join(filter(lambda c: c.isalpha(), hidden_message))[
            : len(modify_pixel_options)
        ].lower()
        modify_pixels = sorted(reng.sample(modify_pixel_options, len(hidden_message)))

        for pixel, char in zip(modify_pixels, hidden_message):
            diff = ord(char) - ord("a") - 13
            if diff >= 0:
                diff = diff + 1
            img_data[pixel] = img_data[pixel] + diff

        img_obj.putdata(img_data)
        img_obj.save(output_fp, __BMP_FORMAT_STR)

    except IOError as err:
        raise ImageToolError("Unable to read/write", str(input_fp), "->", str(output_fp)) from err


def decode_text_delta_from_greyscale_bmp(input_fp1, input_fp2):
    """ Decodes text hidden in a greyscale image. The image delta is found,
    and each pixel that differs is converted to a letter of the alphabet """

    # PIL appears to break if given a Path object for some of these operations?
    input_fp1 = str(input_fp1) if isinstance(input_fp1, Path) else input_fp1
    input_fp2 = str(input_fp2) if isinstance(input_fp2, Path) else input_fp2

    try:
        img_obj1 = Image.open(input_fp1).convert("L")
        img_obj2 = Image.open(input_fp2).convert("L")

        if img_obj1.width != img_obj2.width or img_obj1.height != img_obj2.height:
            raise ImageToolError("Cannot find delta for differently sized images")

        img_data1 = img_obj1.getdata()
        img_data2 = img_obj2.getdata()

        result = "".join(
            map(
                lambda x: chr((x - 1 if x > 0 else x) + 13 + ord("a")),
                filter(lambda x: x != 0, [b - a for a, b in zip(img_data1, img_data2)]),
            )
        )

        return result
    except IOError as err:
        raise ImageToolError(
            "Unable to read/write", str(input_fp1), ",", str(input_fp2)
        ) from err
