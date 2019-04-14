from django import template

register = template.Library()


@register.filter
def list_index(l, i):
    return l[i]


@register.filter
def subtract(a, b):
    return a - b

