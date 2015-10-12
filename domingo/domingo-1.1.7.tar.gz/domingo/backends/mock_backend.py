
from .mongo_backend import MongoStore

import mongomock
from mongomock import Database

M = mongomock.Connection()

class MockStore(MongoStore):
    """
        this is awesome.
        By setting "M" to be the mongomock db, everything 'just' works...
    """