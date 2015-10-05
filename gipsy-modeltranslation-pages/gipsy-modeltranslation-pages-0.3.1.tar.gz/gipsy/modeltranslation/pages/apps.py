from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GipsyPages(AppConfig):
    name = 'gipsy.modeltranslation.pages'
    verbose_name = _("Gipsy Pages")
