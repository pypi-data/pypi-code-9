from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class SabotApp(AppConfig):
    name = 'sabot'
    verbose_name = _('Sabot')

    def ready(self):
        for patch in getattr(settings, 'SABOT_PATCHES', ()):
            patch.init()
