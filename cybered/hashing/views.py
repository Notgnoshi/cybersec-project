from django.shortcuts import render
from django.views.generic import TemplateView


class HashingMainPageView(TemplateView):
    template_name = "hashing_begin.html"
