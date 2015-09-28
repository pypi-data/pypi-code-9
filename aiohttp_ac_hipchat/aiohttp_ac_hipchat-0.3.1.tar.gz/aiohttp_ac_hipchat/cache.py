import asyncio
from datetime import datetime
from abc import abstractmethod, ABC


class AbstractCache(ABC):

    @abstractmethod
    @asyncio.coroutine
    def get(self, key):
        pass

    @abstractmethod
    @asyncio.coroutine
    def setex(self, key, seconds, value):
        pass


class RedisCache(AbstractCache):

    def __init__(self, redis):
        super().__init__()
        self.redis = redis

    @asyncio.coroutine
    def setex(self, key, seconds, value):
        return (yield from self.redis.setex(key, seconds, value))

    @asyncio.coroutine
    def get(self, key):
        return (yield from self.redis.get(key))

class NoOpCache(AbstractCache):

    @asyncio.coroutine
    def setex(self, key, seconds, value):
        pass

    @asyncio.coroutine
    def get(self, key):
        return None

class InMemoryCache(AbstractCache):

    def __init__(self):
        super().__init__()
        self.cache = {}

    @asyncio.coroutine
    def setex(self, key, seconds, value):
        self.cache[key] = (datetime.now() + datetime.timedelta(seconds=seconds), value)

    @asyncio.coroutine
    def get(self, key):
        cached_value = self.cache.get(key)
        if cached_value is not None:
            if self.is_expired(cached_value):
                del self.cache[key]
            else:
                return cached_value

        return None

    @staticmethod
    def is_expired(cached_value):
        expired_date, value = cached_value
        return datetime.now() >= expired_date
