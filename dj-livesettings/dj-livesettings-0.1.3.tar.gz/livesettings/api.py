# coding: utf-8
import logging

from . import __version__
from .forms import parse_value
from .models import LiveSetting
from django.conf import settings
from memoize import memoize


log = logging.getLogger('livesettings')


class LiveSettings(object):

    def __getattr__(self, key):
        return self._get_value(key)

    @memoize(timeout=settings.LIVE_SETTINGS_CACHE_TIME)
    def _get_all_from_db(self, _version=__version__):
        return \
            {
                ls.key: ls
                for ls in LiveSetting.objects.all()
            }

    def _get_value(self, key):
        value = self._get_value_from_db(key)
        if value is None:
            value = getattr(settings, key)
        return value

    def _get_value_from_db(self, key):
        value = None
        result = self._get_all_from_db()
        live_setting = result.get(key)
        if live_setting:
            try:
                value = parse_value(live_setting.value, live_setting.key_type)
            except Exception:
                log.error('invalid livesetting value', exc_info=True)
        return value

live_settings = LiveSettings()
