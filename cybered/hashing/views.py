from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from .apps import HashingConfig
from .forms import *
from .src.hash_functions import *

DIGEST_FUNCS = (
    (get_MD5_digest, "MD5"),
    (get_SHA1_digest, "SHA1"),
    (get_SHA2_digest, "SHA2"),
    (get_SHA3_digest, "SHA3"),
)


def scoped(text):
    """Prevent name collisions with other apps in the session.

    Enable reverse lookup of sibling pages.
    """
    return HashingConfig.name + ":" + text


class HashingTemplateView(TemplateView):
    """Base for simple template views in the module
    which does nothing more than set the module name for
    the header"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module_name"] = HashingConfig.module_name
        return context


class HashingFormView(FormView):
    """Base for simple form views in the module
    which does nothing more than set the module name for
    the header"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module_name"] = HashingConfig.module_name
        return context


class HashingMainPageView(HashingTemplateView):
    """The main page for the hasing module."""

    template_name = "hashing/begin.html"


class HashingMotivationPageView(HashingTemplateView):
    """The main page for the hasing module."""

    template_name = "hashing/motivation.html"


class HashingExamplesPageView(HashingFormView):
    """Page listing several example hash functions."""

    template_name = "hashing/examples_form.html"
    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(scoped("examples_results"))

    def form_valid(self, form):
        """Add validated form data to the user session."""
        print("Form data posted!")

        # Passing data between views is done with a session; which is
        # created implicitly for each separate connection (not sure when/if they time out)
        self.request.session[scoped("example_hash_text")] = form.cleaned_data["text"]

        return super().form_valid(form)


class HashingExamplesResultPageView(HashingTemplateView):
    """Display the results of the example hashes."""

    template_name = "hashing/examples_results.html"

    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """
        given_text = ""
        if scoped("example_hash_text") in self.request.session:
            given_text = self.request.session[scoped("example_hash_text")]

        return (
            super().dispatch(request, *args, **kwargs)
            if given_text
            else redirect(reverse(scoped("examples_form")))
        )

    def get_context_data(self, **kwargs):
        """Compute the hashes of the submitted text and add the results to the page context."""
        context = super().get_context_data(**kwargs)

        # Need to make sure that the user went through the
        # text entry, and that they put in non-empty data
        # before we process this page
        assert scoped("example_hash_text") in self.request.session
        assert self.request.session[scoped("example_hash_text")]

        given_text = self.request.session[scoped("example_hash_text")]
        context["input_text"] = given_text

        hash_results = []
        for func, text in DIGEST_FUNCS:
            result = {}
            result["digest"] = func(given_text)
            result["name"] = text
            hash_results.append(result)

        context["hash_results"] = hash_results

        return context


class HashingKeyedExamplesPageView(HashingFormView):
    """Page listing several example hash functions."""

    template_name = "hashing/keyed_hashes_form.html"
    form_class = TextBoxWithPasswordForm
    success_url = ""

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(scoped("keyed_examples_results"))

    def form_valid(self, form):
        """Add validated form data to the user session."""

        # Passing data between views is done with a session; which is
        # created implicitly for each separate connection (not sure when/if they time out)
        self.request.session[scoped("example_keyed_hash_text")] = form.cleaned_data["text"]
        self.request.session[scoped("example_keyed_hash_key")] = form.cleaned_data["secret_key"]

        return super().form_valid(form)


class HashingKeyedExamplesResultPageView(HashingTemplateView):
    """Display the results of the keyed example hashes."""

    template_name = "hashing/keyed_hashes_results.html"

    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """
        given_text = ""
        if scoped("example_keyed_hash_text") in self.request.session:
            given_text = self.request.session[scoped("example_keyed_hash_text")]

        given_key = ""
        if scoped("example_keyed_hash_key") in self.request.session:
            given_key = self.request.session[scoped("example_keyed_hash_key")]

        return (
            super().dispatch(request, *args, **kwargs)
            if given_text and given_key
            else redirect(reverse(scoped("keyed_examples_form")))
        )

    def get_context_data(self, **kwargs):
        """Compute the hashes of the submitted text and add the results to the page context."""
        context = super().get_context_data(**kwargs)

        # Need to make sure that the user went through the
        # text entry, and that they put in non-empty data
        # before we process this page
        assert scoped("example_hash_text") in self.request.session
        assert self.request.session[scoped("example_hash_text")]
        assert scoped("example_keyed_hash_key") in self.request.session
        assert self.request.session[scoped("example_keyed_hash_key")]

        given_text = self.request.session[scoped("example_keyed_hash_text")]
        given_key = self.request.session[scoped("example_keyed_hash_key")]

        context["input_text"] = given_text
        context["input_key"] = given_key
        context["keyed_text"] = add_key(given_text, given_key)

        hash_results = []
        for func, text in DIGEST_FUNCS:
            result = {}
            result["digest"] = func(given_text)
            result["keyed_digest"] = func(given_text, given_key)
            result["name"] = text
            hash_results.append(result)

        context["hash_results"] = hash_results

        return context
