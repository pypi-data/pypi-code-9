import abc
import six


@six.add_metaclass(abc.ABCMeta)
class PluginBase(object):
    """Base class for example plugin.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_version(self):
        return __version__

    @abc.abstractmethod
    def add_intents(self):
        """Install intents in the database
        """

__title__ = 'Lisa Plugins'
__version__ = '0.1'
__author__ = 'Lisa User'
__license__ = 'Apache'
__copyright__ = 'Copyright 2015'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'
