from lisa_api.lisa.logger import logger
from lisa_api.lisa.plugin import PluginBase


class WifiledPlugin(PluginBase):
    def __init__(self):
        pass

    def get_version(self):
        return __version__

    def add_intents(self):
        from lisa_api.api.models import Intent

        obj, created = Intent.objects.update_or_create(
            name='wifiled_turn_power',
            defaults={
                'method': 'POST',
                'api_url': '/api/v1/plugin-wifiled/controllers/{controller_name}/turn_power/'
            }
        )
        logger.debug("Adding {intent_name} intent for wifiled plugin".format(intent_name=obj.name))

        obj, created = Intent.objects.update_or_create(
            name='wifiled_change_color',
            defaults={
                'method': 'POST',
                'api_url': '/api/v1/plugin-wifiled/controllers/{controller_name}/change_color/'
            }
        )
        logger.debug("Adding {intent_name} intent for wifiled plugin".format(intent_name=obj.name))

__title__ = 'Lisa Plugins Wifiled'
__version__ = '0.1.3'
__author__ = 'Julien Syx'
__license__ = 'Apache'
__copyright__ = 'Copyright 2015 Julien Syx'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'
