# -*- coding: utf-8 -*-
# ATENCAO: nao chame este arquivo de redis. Vai entrar em conflito com o modulo redis do sistema

import redis
import os

class RedisConnect(object):

    @classmethod
    def __init__(self, host=None, port=None, db=None):

        if host is None:
            host = os.environ.get('REDIS_HOST')

        if port is None:
            port = os.environ.get('REDIS_PORT')

        if db is None:
            db = os.environ.get('REDIS_DB')

        if hasattr(self,'redis_pool') is False:
            self.redis_pool = redis.ConnectionPool(
                    host=host, port=port, db=db,
                    max_connections=10)
            self.server = redis.StrictRedis(connection_pool=self.redis_pool)
        else:
           pass

    def get(self, key):
        return self.server.get(key)

    def set(self, key, value):
        return self.server.set(key, value)

    def setex(self, key, ttl, value):
        return self.server.setex(key, ttl, value)

    def getset(self, key, value):
        return self.server.getset(key, value)

    def expire(self, key, value):
        return self.server.expire(key, value)

    def exists(self, key):
        return self.server.exists(key)
