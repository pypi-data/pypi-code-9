import six
from threading import local
from collections import namedtuple
from django.core.cache import CacheHandler

_getitem = CacheHandler.__getitem__
def patch_cache_handler():
    _caches_cls = namedtuple("_caches", ["caches"])
    def __getitem__(self, alias):
        if isinstance(self._caches, local):
            self._caches = _caches_cls(getattr(self._caches, "caches", {}))
        return _getitem(self, alias)
    CacheHandler.__getitem__ = __getitem__


try:
    import cPickle as pickle
except ImportError:
    import pickle
from . import client
from django.core.cache.backends.memcached import BaseMemcachedCache

unserialize_types = []
unserialize_types += six.integer_types
unserialize_types.append(six.binary_type)

def serialize_pickle(key, value):
    if isinstance(value, tuple(unserialize_types)):
        return value, 1
    return pickle.dumps(value), 2


def deserialize_pickle(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return pickle.loads(value)
    raise Exception('Unknown flags for value: {1}'.format(flags))


class PyMemcacheCache(BaseMemcachedCache):

    """An implementation of a cache binding using pymemcache."""

    def __init__(self, server, params):
        BaseMemcachedCache.__init__(
            self,
            server,
            params,
            library=client,
            value_not_found_exception=ValueError
        )
        self._client = None

    @property
    def _cache(self):
        if not self._client:
            kwargs = {
                'serializer': serialize_pickle,
                'deserializer': deserialize_pickle,
            }
            if self._options:
                for key, value in self._options.items():
                    kwargs[key.lower()] = value

            # default use_pooling
            if "use_pooling" not in kwargs:
                kwargs["use_pooling"] = True

            servers = []
            for server in self._servers:
                host, port = server.split(":")
                servers.append((host, int(port)))
            self._client = self._lib.Client(servers, **kwargs)
            if self._client.use_pooling:
                patch_cache_handler()
        return self._client
