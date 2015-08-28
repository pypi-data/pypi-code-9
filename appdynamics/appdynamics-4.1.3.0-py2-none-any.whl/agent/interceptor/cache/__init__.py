# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Base interceptor for distributed caches (typically, key-value stores).

"""

from appdynamics.agent.models.exitcalls import EXIT_CACHE
from appdynamics.agent.interceptor.base import ExitCallInterceptor


class CacheInterceptor(ExitCallInterceptor):
    """Base class for cache interceptors.

    Extra Parameters
    -----------------
    vendor : string
        The vendor name of this cache backend e.g. MEMCACHED.

    """

    def __init__(self, agent, cls, vendor):
        self.vendor = vendor
        super(CacheInterceptor, self).__init__(agent, cls)

    def get_backend(self, server_pool):
        """

        Parameters
        ----------
        server_pool : list of str

        """

        identifying_properties = {
            'VENDOR': self.vendor,
            'SERVER POOL': '\n'.join(server_pool),
        }

        # All of the agents take the last server in the pool; not sure why.
        display_name = "{server_pool} - {vendor}".format(vendor=self.vendor, server_pool=server_pool[-1])
        return self.agent.backend_registry.get_backend(EXIT_CACHE, identifying_properties, display_name)

from .redis import intercept_redis
from .memcache import intercept_memcache

__all__ = ['intercept_redis', 'intercept_memcache']
