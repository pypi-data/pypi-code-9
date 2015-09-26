
from django.utils import six
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings


default_app_config = 'leonardo_module_analytics.AnalyticsConfig'


class Default(object):

    apps = [
        'analytical',
        'leonardo_module_analytics',
    ]

    config = {
        'GOOGLE_ANALYTICS_PROPERTY_ID': ('UA-62809705-1', _('Google Site identificator')),
        'GOOGLE_ANALYTICS_SITE_SPEED': (False, _('analyze page speed')),
        'GOOGLE_ANALYTICS_ANONYMIZE_IP': (False, _('anonymize ip')),
    }


class AnalyticsConfig(AppConfig, Default):
    name = 'leonardo_module_analytics'
    verbose_name = ("Leonardo Analytics")

    def ready(self):
        # chech defaults and delete it from main settings
        # because it's activate JS in templates
        from constance import config

        for k, values in six.iteritems(self.config):
            if values[0] == getattr(config, k, None):

                setattr(django_settings, k, None)


default = Default()
