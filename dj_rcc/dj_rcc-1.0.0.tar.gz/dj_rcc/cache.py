# -*- coding: utf-8 -*-
from django.core.cache.backends.base import BaseCache
import pickle
from rediscluster import StrictRedisCluster

DEFAULT_TIMEOUT = 0


class RedisClusterCache(BaseCache):
    """
    If a command is implemented over the one in BaseCache then it requires some
    changes compared to the regular implementation of the method.
    """
    def __init__(self, server, params):
        super(
            RedisClusterCache, self).__init__(params)

        self.startup_nodes = []
        if isinstance(server, list):
            for server in server:
                try:
                    host = server['host']
                    port = server['port']
                    port = int(port)

                    if not isinstance(host, str) and not isinstance(host,
                                                                    unicode):
                        raise ValueError(
                            'Excepting host string for server location: {}.'
                            ' Got {} instead'.format(
                                server, server['host']
                            )
                        )
                    self.startup_nodes.append(server)
                except KeyError, msg:
                    raise KeyError(
                        'Missing key for server location: {}'.format(msg)
                    )
                except TypeError:
                    raise TypeError(
                        'Expecting integer for port number, got {}'.format(
                            type(server['port'])
                        )
                    )
        else:
            raise TypeError(
                'Excepting list for server location, got {}: {}'.format(
                    type(server), server
                )
            )
        self._options = params.get('OPTIONS')
        self.max_connections = self._options.get('max_connections')
        self._client = StrictRedisCluster(startup_nodes=self.startup_nodes,
                                          max_connections=self.max_connections)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if not isinstance(key, str) and not isinstance(key, unicode):
            raise TypeError(
                'Expecting str for key, got {} instead: {}'.format(
                    type(key), key
                )
            )
        self.set(key, value, timeout)

        if value == self.get(key):
            return True
        return False

    def get(self, key, default=None, version=None):
        if not isinstance(key, str) and not isinstance(key, unicode):
            raise TypeError(
                'Expecting str for key, got {} instead: {}'.format(
                    type(key), key
                )
            )
        value = self._client.get(key)

        if value:
            value = pickle.loads(value)

        return value

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        value = pickle.dumps(value)
        self._client.set(key, value, timeout)

    def delete(self, key, version=None):
        self._client.delete(key)
