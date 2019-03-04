from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.shortcuts import redirect

from .forms import TextBoxForm
from .apps import HashingConfig
from .src.hash_functions import *

# Custom scoping function to prevent name collisions with other apps
# in session dict and be able to reverse-lookup sibling pages
def scoped(text):
    return HashingConfig.name + ":" + text


class HashingMainPageView(TemplateView):
    template_name = "hashing/hashing_begin.html"


class HashingExamplesPageView(FormView):
    template_name = "hashing/hashing_examples.html"
    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        """Override of get_success_url so that the url conf files
        are all loaded and reverse() can be called"""
        return reverse(scoped("hash_examples_result"))

    def form_valid(self, form):
        """Called when valid form data has been POSTed."""

        print("Form data posted!")

        # Passing data between views is done with a session; which is
        # created implicitly for each separate connection (not sure when/if they time out)
        self.request.session[scoped("example_hash_text")] = form.cleaned_data["text"]

        return super().form_valid(form)


class HashingExamplesResultPageView(TemplateView):
    template_name = "hashing/hashing_examples_result.html"

    def dispatch(self, request, *args, **kwargs):
        """Verifies that there's input text to process
        before we try to render the page. This can only happen
        if we start clearing the session data, or users enter the url
        for this page directly without a session"""
        given_text = ""
        if scoped("example_hash_text") in self.request.session:
            given_text = self.request.session[scoped("example_hash_text")]

        return (
            super().dispatch(request, *args, **kwargs)
            if given_text
            else redirect(reverse(scoped("hash_examples")))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Need to make sure that the user went through the
        # text entry, and that they put in non-empty data
        # before we process this page
        assert scoped("example_hash_text") in self.request.session
        assert self.request.session[scoped("example_hash_text")]

        given_text = self.request.session[scoped("example_hash_text")]
        context["input_text"] = given_text

        hash_results = []
        for fun, text in (
            (get_MD5_digest, "MD5"),
            (get_SHA1_digest, "SHA1"),
            (get_SHA2_digest, "SHA2"),
            (get_SHA3_digest, "SHA3"),
        ):
            result = {}
            result["digest"] = fun(given_text)
            result["name"] = text
            hash_results.append(result)

        context["hash_results"] = hash_results

        return context
