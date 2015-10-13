
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from leonardo.apps import app_reverse_lazy
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


def source_url_override(self):
    return app_reverse_lazy(
        'newswall_source_detail',
        'leonardo_newswall.apps.newswall',
        kwargs={'slug': self.slug})

LEONARDO_ABSOLUTE_URL_OVERRIDES = {
    'newswall.source': 'leonardo_newswall.source_url_override'}


class Config(AppConfig):
    name = 'leonardo_newswall'
    verbose_name = LEONARDO_OPTGROUP
