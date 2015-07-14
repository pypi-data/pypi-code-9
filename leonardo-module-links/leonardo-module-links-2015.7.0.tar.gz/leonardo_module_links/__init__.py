
from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo_module_links.LinksConfig'


class Default(object):

    optgroup = ('Link lists')

    apps = [
            'leonardo_module_links',
        ]

    @property
    def widgets(self):
        return [
            LinkButtonWidget,
            LinkMenuWidget,
        ]


class LinksConfig(AppConfig, Default):
    name = 'leonardo_module_links'
    verbose_name = "Link lists"

default = Default()
