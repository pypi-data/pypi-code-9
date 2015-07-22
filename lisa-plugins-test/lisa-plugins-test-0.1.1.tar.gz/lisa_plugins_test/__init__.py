from lisa_api.lisa.plugin import PluginBase


class TestPlugin(PluginBase):
    def __init__(self):
        pass

    def get_version(self):
        return __version__

    def add_intents(self):
        from lisa_api.api.models import Intent


__title__ = 'Lisa Plugins Test'
__version__ = '0.1.1'
__author__ = 'Julien Syx'
__license__ = 'Apache'
__copyright__ = 'Copyright 2015 Julien Syx'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'
