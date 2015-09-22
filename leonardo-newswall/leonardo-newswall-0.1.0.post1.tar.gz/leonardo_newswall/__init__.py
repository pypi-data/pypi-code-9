
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .widget import *

default_app_config = 'leonardo_newswall.Config'


LEONARDO_APPS = [
    'leonardo_newswall',
    'newswall',
]

LEONARDO_PLUGINS = [
    ('leonardo_newswall.apps.newswall', _('Newswall'), ),
]

LEONARDO_OPTGROUP = 'Leonardo Newswall'

LEONARDO_WIDGETS = [
    RecentNewsWidget,
]


class Config(AppConfig):
    name = 'leonardo_newswall'
    verbose_name = LEONARDO_OPTGROUP
