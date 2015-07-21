from lisa_api.lisa.logger import logger
from lisa_api.lisa.plugin import PluginBase


class ShoppingPlugin(PluginBase):
    def __init__(self):
        pass

    def get_version(self):
        return __version__

    def add_intents(self):
        from lisa_api.api.models import Intent

        obj, created = Intent.objects.update_or_create(
            name='shopping_item_add',
            defaults={
                'method': 'POST',
                'api_url': '/api/v1/plugin-shopping/lists/{list_name}/item_add/'
            }
        )
        logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

        obj, created = Intent.objects.update_or_create(
            name='shopping_item_delete',
            defaults={
                'method': 'POST',
                'api_url': '/api/v1/plugin-shopping/lists/{list_name}/item_delete/'
            }
        )
        logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

        obj, created = Intent.objects.update_or_create(
            name='shopping_item_list',
            defaults={
                'method': 'GET',
                'api_url': '/api/v1/plugin-shopping/lists/{list_name}/item_list/'
            }
        )
        logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

        obj, created = Intent.objects.update_or_create(
            name='shopping_list_add',
            defaults={
                'method': 'POST',
                'api_url': '/api/v1/plugin-shopping/lists/'
            }
        )
        logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

        obj, created = Intent.objects.update_or_create(
            name='shopping_list_delete',
            defaults={
                'method': 'DELETE',
                'api_url': '/api/v1/plugin-shopping/lists/'
            }
        )
        logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

        obj, created = Intent.objects.update_or_create(
            name='shopping_list_list',
            defaults={
                'method': 'GET',
                'api_url': '/api/v1/plugin-shopping/lists/'
            }
        )
        logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

__title__ = 'Lisa Plugins Shopping'
__version__ = '0.2.0'
__author__ = 'Julien Syx'
__license__ = 'Apache'
__copyright__ = 'Copyright 2015 Julien Syx'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'
