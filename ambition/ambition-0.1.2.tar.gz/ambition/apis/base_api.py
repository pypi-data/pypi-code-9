from abc import ABCMeta

from ..configuration import ApiConfiguration
from ..api_client import ApiClient


class AbstractBaseApi(object):
    """
    Base Api class which provides a factory method
    """
    __metaclass__ = ABCMeta

    @classmethod
    def create_client(cls, subdomain, api_key, scheme='http', port=None):
        """
        Factory method for creating a client for this api
        """
        hostname = '%s://%s.ambition.com' % (scheme, subdomain)
        if port is not None:
            hostname = '%s:%s' % (hostname, port)
        configuration = ApiConfiguration(hostname, api_key)
        client = ApiClient(configuration)
        return cls(client)
