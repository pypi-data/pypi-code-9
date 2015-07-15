from .backends.mongo_backend import MongoStore
from .backends.redis_backend import RedisStore
from .backends.mock_backend import MockStore
# from .backends.rethink_backend import RethinkStore


def get_database(storage, model):

    if storage == 'mongo':
        return MongoStore(model)
    if storage == 'redis':
        return RedisStore(model)
    if storage == 'mock':
        return MockStore(model)
    # if storage == 'rethink':
        # return RethinkStore(namespace)
