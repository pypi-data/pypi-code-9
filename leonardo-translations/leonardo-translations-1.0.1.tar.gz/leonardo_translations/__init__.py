
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'leonardo_translations.Config'

LEONARDO_OPTGROUP = 'translation'
LEONARDO_APPS = [
    'leonardo_translations',
    'rosetta'
]


class Config(AppConfig):
    name = 'leonardo_translations'
    verbose_name = _("Translations")
