from django import template

register = template.Library()

@register.filter
def intersect(qs1, qs2):
    """Return intersection of two querysets"""
    return qs1 & qs2