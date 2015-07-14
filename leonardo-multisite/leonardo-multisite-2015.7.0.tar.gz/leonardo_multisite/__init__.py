
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'leonardo_multisite.Config'

LEONARDO_OPTGROUP = 'multisite'
LEONARDO_APPS = ['leonardo_multisite']
LEONARDO_MIDDLEWARES = ['leonardo_multisite.middleware.MultiSiteMiddleware']

LEONARDO_CONFIG = {
    'MULTISITE_ENABLED': (False, _(
        'Enable multi site request processing')),
}


class Config(AppConfig):
    name = 'leonardo_multisite'
    verbose_name = _("Multisite")
