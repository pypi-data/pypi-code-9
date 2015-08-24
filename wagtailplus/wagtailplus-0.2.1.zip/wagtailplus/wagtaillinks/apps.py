"""
Contains application configuration.
"""
from django.apps import AppConfig


class WagtailLinksAppConfig(AppConfig):
    name            = 'wagtailplus.wagtaillinks'
    label           = 'wagtaillinks'
    verbose_name    = 'Links'
