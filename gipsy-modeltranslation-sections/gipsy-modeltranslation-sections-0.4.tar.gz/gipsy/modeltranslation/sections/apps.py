from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GipsySections(AppConfig):
    name = 'gipsy.modeltranslation.sections'
    verbose_name = _("Gipsy Sections")
