from __future__ import absolute_import


class ApiConfiguration(object):
    """
    API Configuration Class
    """
    # Base url
    host = None

    # Authentication settings
    _api_key = None
    _api_key_prefix = None

    def __init__(self, host, api_key, api_key_prefix='Token'):
        self.host = host
        self._api_key = api_key
        self._api_key_prefix = api_key_prefix

    @property
    def api_key(self):
        if self._api_key and self._api_key_prefix:
            return self._api_key_prefix + ' ' + self._api_key
        return self._api_key

    def auth_settings(self):
        return {
            'default': {
                'type': 'api_key',
                'in': 'header',
                'key': 'Authorization',
                'value': self.api_key
            },
        }
