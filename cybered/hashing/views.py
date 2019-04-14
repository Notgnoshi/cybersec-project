from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from .apps import HashingModule
from .forms import *
from .src.hash_functions import *

from shared.src import cybered


class HashingMixin(HashingModule, cybered.PageMixin, cybered.PaginatedMixin):
    """ Mixin for Hashing module pages that adds the cybered page mixin, and the cybered paginate
    mixing. This step of the get_context_data chain will disable all buttons on the paginator
    after the furthest one that the user has 'unlocked' to require they go through the module
    in order """
    def get_context_data(self, disabled_pages=[], **kwargs):
        page_index = self.kwargs["page_index"]
        page_count = self.kwargs["page_count"]

        key = HashingModule.scope("progress")
        if key not in self.request.session:
            self.request.session[key] = page_index
        self.request.session[key] = max(self.request.session[key], page_index)

        disabled_pages = disabled_pages + list(range(self.request.session[key]+2, page_count))
        return super().get_context_data(disabled_pages=disabled_pages, **kwargs)

DIGEST_FUNCS = (
    (get_MD5_digest, "MD5"),
    (get_SHA1_digest, "SHA1"),
    (get_SHA2_digest, "SHA2"),
    (get_SHA3_digest, "SHA3"),
)


class HashingMainPageView(HashingMixin, TemplateView):
    """The main page for the hashing module."""

    pass


class HashingMotivationPageView(HashingMixin, TemplateView):
    """The motivation page for the hashing module."""

    pass


class HashingExamplesPageView(HashingMixin, FormView):
    """Page listing several example hash functions."""

    form_class = TextBoxForm
    success_url = ""

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(HashingModule.scope("examples_results"))

    def form_valid(self, form):
        """Add validated form data to the user session."""
        # Passing data between views is done with a session; which is
        # created implicitly for each separate connection (not sure when/if they time out)
        self.request.session[HashingModule.scope("example_hash_text")] = form.cleaned_data["text"]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Always lock the next page if there's no data in the session
        if HashingModule.scope("example_hash_text") in self.request.session:
            return super().get_context_data(**kwargs)

        page_index = self.kwargs["page_index"]
        context = super().get_context_data(disabled_pages=[page_index+1], **kwargs)
        return context


class HashingExamplesResultPageView(HashingMixin, TemplateView):
    """Display the results of the example hashes."""

    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """
        given_text = ""
        if HashingModule.scope("example_hash_text") in self.request.session:
            given_text = self.request.session[HashingModule.scope("example_hash_text")]

        return (
            super().dispatch(request, *args, **kwargs)
            if given_text
            else redirect(reverse(HashingModule.scope("examples_form")))
        )

    def get_context_data(self, **kwargs):
        """Compute the hashes of the submitted text and add the results to the page context."""
        context = super().get_context_data(**kwargs)

        # Need to make sure that the user went through the
        # text entry, and that they put in non-empty data
        # before we process this page
        assert HashingModule.scope("example_hash_text") in self.request.session
        assert self.request.session[HashingModule.scope("example_hash_text")]

        given_text = self.request.session[HashingModule.scope("example_hash_text")]
        context["input_text"] = given_text

        hash_results = []
        for func, text in DIGEST_FUNCS:
            result = {}
            result["digest"] = func(given_text)
            result["name"] = text
            hash_results.append(result)

        context["hash_results"] = hash_results

        return context


class HashingKeyedExamplesPageView(HashingMixin, FormView):
    """Page explaining keyed hash functions."""

    form_class = TextBoxWithPasswordForm
    success_url = ""

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(HashingModule.scope("keyed_examples_results"))

    def form_valid(self, form):
        """Add validated form data to the user session."""
        # Passing data between views is done with a session; which is
        # created implicitly for each separate connection (not sure when/if they time out)
        self.request.session[HashingModule.scope("example_keyed_hash_text")] = form.cleaned_data[
            "text"
        ]
        self.request.session[HashingModule.scope("example_keyed_hash_key")] = form.cleaned_data[
            "secret_key"
        ]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Always lock the next page if there's no data in the session
        if HashingModule.scope("example_keyed_hash_key") in self.request.session:
            return super().get_context_data(**kwargs)

        page_index = self.kwargs["page_index"]
        context = super().get_context_data(disabled_pages=[page_index+1], **kwargs)
        return context

class HashingKeyedExamplesResultPageView(HashingMixin, TemplateView):
    """Display the results of the keyed example hashes."""

    def dispatch(self, request, *args, **kwargs):
        """Verify that there is input text to process before rendering the page.

        This can only happen if we start clearing the session data at some point, or
        if a user enters the url for this page directly without a preexisting session.
        """
        given_text = ""
        if HashingModule.scope("example_keyed_hash_text") in self.request.session:
            given_text = self.request.session[HashingModule.scope("example_keyed_hash_text")]

        given_key = ""
        if HashingModule.scope("example_keyed_hash_key") in self.request.session:
            given_key = self.request.session[HashingModule.scope("example_keyed_hash_key")]

        return (
            super().dispatch(request, *args, **kwargs)
            if given_text and given_key
            else redirect(reverse(HashingModule.scope("keyed_examples_form")))
        )

    def get_context_data(self, **kwargs):
        """Compute the hashes of the submitted text and add the results to the page context."""
        context = super().get_context_data(**kwargs)

        # Need to make sure that the user went through the
        # text entry, and that they put in non-empty data
        # before we process this page
        assert HashingModule.scope("example_hash_text") in self.request.session
        assert self.request.session[HashingModule.scope("example_hash_text")]
        assert HashingModule.scope("example_keyed_hash_key") in self.request.session
        assert self.request.session[HashingModule.scope("example_keyed_hash_key")]

        given_text = self.request.session[HashingModule.scope("example_keyed_hash_text")]
        given_key = self.request.session[HashingModule.scope("example_keyed_hash_key")]

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


class HashingConclusionPageView(HashingMixin, TemplateView):
    """The conclusion page for the hashing module."""

    pass


class HashingToolsPageView(HashingMixin, FormView):
    """The Tools page for the hashing module."""

    form_class = TextBoxWithOptionalPasswordForm
    success_url = ""

    def get_success_url(self):
        """Load url conf files so that reverse() can be called."""
        return reverse(HashingModule.scope("tools"))

    def form_valid(self, form):
        """Add validated form data to the user session."""
        # Passing data between views is done with a session; which is
        # created implicitly for each separate connection (not sure when/if they time out)
        self.request.session[HashingModule.scope("tools_hash_text")] = form.cleaned_data["text"]
        self.request.session[HashingModule.scope("tools_hash_key")] = form.cleaned_data[
            "secret_key"
        ]

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Compute the hashes of the submitted text and add the results to the page context."""
        context = super().get_context_data(**kwargs)

        given_text = ""
        if HashingModule.scope("tools_hash_text") in self.request.session:
            given_text = self.request.session[HashingModule.scope("tools_hash_text")]

        given_key = ""
        if HashingModule.scope("tools_hash_key") in self.request.session:
            given_key = self.request.session[HashingModule.scope("tools_hash_key")]

        context["input_text"] = given_text

        if given_text:
            if given_key:
                context["input_key"] = given_key
                context["keyed_text"] = add_key(given_text, given_key)

            hash_results = []
            for func, text in DIGEST_FUNCS:
                result = {}
                result["digest"] = func(given_text)
                result["name"] = text

                if given_key:
                    result["keyed_digest"] = func(given_text, given_key)

                hash_results.append(result)

            context["hash_results"] = hash_results

        return context
