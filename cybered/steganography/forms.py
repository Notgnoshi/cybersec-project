from django import forms
from django.contrib.staticfiles import finders


class ImageChoicesMixin:
    __IMAGE_SEARCH_STRINGS = ("{}", "{}.x", "{}.y")

    def __init__(self, *args, name_url_pairs=None, **kwargs):
        self.__name_url_pairs = name_url_pairs or ()
        super().__init__(*args, **kwargs)

    def clean(self):
        """Verifies that an image exists that can have data encoded in it, and
        stores the request url to said image in 'image_static_url'. It should be possible
        to put this url into a static file finder to get the full path to it, or to put it
        into the static template tag to display it on screen
        
        Right now this works with hard-coded images, but the form could be modified
        to take an image upload, in which case this function should verify that the uploaded
        image is a jpg and that it is in a valid disk location (in the MEDIA_ROOT)
        """

        cleaned_data = super().clean()

        # Not sure why, but using images as submit buttons adds [image_name].x and [image_name].y
        # to the POST data instead of just setting the image name
        chosen_image = ""
        chosen_static_url = ""
        for img_name, img_path in self.__name_url_pairs:
            for search_str in self.__IMAGE_SEARCH_STRINGS:
                if search_str.format(img_name) in self.data:
                    chosen_image = img_name
                    chosen_static_url = img_path

        if chosen_image == "":
            raise forms.ValidationError("No image chosen")

        # Sanity check that file finders can find the image
        chosen_path = finders.find(chosen_static_url)
        if chosen_path == "":
            raise forms.ValidationError("No image found for static path", chosen_static_url)

        cleaned_data["image_static_url"] = chosen_static_url
        cleaned_data["image_name"] = chosen_image
        self.cleaned_data = cleaned_data
        return self.cleaned_data


class ImageForm(ImageChoicesMixin, forms.Form):
    pass


class SecretMessageImageForm(ImageChoicesMixin, forms.Form):
    secret_message = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), label="Secret Message"
    )
