
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .widget import *

default_app_config = 'leonardo_module_folio.FolioConfig'


class Default(object):

    optgroup = 'Portfolio'

    apps = ['leonardo_module_folio']

    plugins = [('leonardo_module_folio.apps.folio', _('Portfolio')), ]

    widgets = [
        ProjectCategoriesWidget,
        FeaturedProjectsWidget
    ]


class FolioConfig(AppConfig, Default):
    name = 'leonardo_module_folio'
    verbose_name = "Folio"


default = Default()
