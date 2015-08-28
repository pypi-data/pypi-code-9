"""Templatetags for the django_ember_toolkit app."""
from django import template

register = template.Library()

#@register.filter
#def lower(value):
#    """
#    Converts a string into all lowercase
#
#    """
#    return value.lower()
