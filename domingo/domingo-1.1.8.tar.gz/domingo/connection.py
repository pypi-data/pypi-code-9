from .backends.mongo_backend import MongoStore
from .backends.redis_backend import RedisStore
from .backends.mock_backend import MockStore


class DatabaseCache(object):

    __instance = None

    STORAGE_MAP = {
        'mongo': MongoStore,
        'redis': RedisStore,
        'mock': MockStore
    }

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.registry = {}
        return cls.__instance

    def __getitem__(self, val):
        if not hasattr(val, 'storage'):
            raise TypeError(
                'DatabaseCache only allows the use of Domingo models for the '
                'registration and acquisition of backend stores.'
            )
        if val not in self.registry:
            Store = self.STORAGE_MAP.get(val.storage)
            store = Store(val)
            self.registry[val] = store

        return self.registry[val]


databases = DatabaseCache()
