from __future__ import absolute_import

import redisext.backend.abc
import redisext.backend.redis as redis
import redisext.packages.dsnparse as dsnparse


class Model(object):
    KEY = None
    CONNECTION = None
    CONNECTION_REUSE = True

    def __init__(self, key=None):
        self.key = key or getattr(self, 'KEY', None)

        self._connection = None
        self._master = None
        self._slave = None

    @classmethod
    def decode(cls, value):
        serializer = getattr(cls, 'SERIALIZER', None)
        if value and serializer:
            return serializer.decode(value)
        else:
            return value

    @classmethod
    def encode(cls, value):
        serializer = getattr(cls, 'SERIALIZER', None)
        if value and serializer:
            return serializer.encode(value)
        else:
            return value

    @property
    def connection(self):
        if not self._connection:
            if isinstance(self.CONNECTION, str):
                conn = dsnparse.parse(self.CONNECTION)

                class Connection(redis.Connection):
                    MASTER = {'host': conn.host, 'port': conn.port, 'db': conn.paths[0]}
                self._connection = Connection
            elif issubclass(self.CONNECTION, redisext.backend.abc.IConnection):
                self._connection = self.CONNECTION
            else:
                raise ValueError
        return self._connection

    def connect_to_master(self):
        if not self.CONNECTION_REUSE:
            return self.connection.connect_to_master()
        if not self._master:
            self._master = self.connection.connect_to_master()
        return self._master

    def connect_to_slave(self):
        if not self.CONNECTION_REUSE:
            return self.connection.connect_to_slave()
        if not self._slave:
            self._slave = self.connection.connect_to_slave()
        return self._slave
