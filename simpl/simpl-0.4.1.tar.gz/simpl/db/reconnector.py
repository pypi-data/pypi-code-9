"""Copyright 2013 Gustav Arngarden.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# pylint: disable=R0903,C0103

import time

import pymongo

DEFAULT_WAIT_TIME = 15


def get_methods(*objs):
    """Get public callables for an object."""
    return set(
        attr
        for obj in objs
        for attr in dir(obj)
        if (not attr.startswith('_')
            and hasattr(getattr(obj, attr), '__call__'))
    )

try:
    # will fail to import from older versions of pymongo
    import pymongo.MongoClient as MongoClient
    import pymongo.MongoReplicaSetClient as MongoReplicaSetClient
except ImportError:
    MongoClient, MongoReplicaSetClient = None, None

EXECUTABLE_MONGO_METHODS = get_methods(pymongo.collection.Collection,
                                       pymongo.database.Database,
                                       pymongo.Connection,
                                       pymongo.ReplicaSetConnection,
                                       MongoClient,
                                       MongoReplicaSetClient,
                                       pymongo)


def wrap(item, key, logger, wait_time):
    """Wrap mongo object in the correct AutoReconnect proxy."""
    if (hasattr(item, '__call__') and not
            isinstance(item, (Executable, MongoProxy))):
        if key in EXECUTABLE_MONGO_METHODS:
            return Executable(item, logger, wait_time)
        else:
            return MongoProxy(item, logger, wait_time)
    return item


class Executable(object):

    """Wrap a MongoDB-method and handle AutoReconnect-exceptions."""

    def __init__(self, method, logger, wait_time=None):
        """Init the mongo driver method wrapper."""
        self.method = method
        self.logger = logger
        self.wait_time = wait_time or DEFAULT_WAIT_TIME

    def __call__(self, *args, **kwargs):
        """Automatic handling of AutoReconnect-exceptions."""
        start = time.time()
        i = 0
        while True:
            try:
                return wrap(self.method(*args, **kwargs), None, self.logger,
                            self.wait_time)
            except pymongo.errors.AutoReconnect:
                end = time.time()
                delta = end - start
                if delta >= self.wait_time:
                    i = -i
                    break
                self.logger.warning('AutoReconnecting, try %d (%.1f seconds)'
                                    % (i, delta))
                time.sleep(pow(2, i))
                i += 1
            finally:
                if i == 0:
                    pass  # No reconnection required
                elif i < 0:
                    self.logger.warning("Abort reconnect after %d tries", -i)
                elif i == 1:
                    self.logger.info("Reconnected in one try")
                elif i > 1:
                    self.logger.warning("Reconnected after %d tries", i)
        # Try one more time, but this time, if it fails, let the
        # exception bubble up to the caller.
        return wrap(self.method(*args, **kwargs), None, self.logger,
                    self.wait_time)

    def __dir__(self):
        """Dir, der."""
        return dir(self.method)

    def __str__(self):
        """Wrap the __str__ of the method."""
        return self.method.__str__()

    def __repr__(self):
        """Wrap the __repr__ of the method."""
        return self.method.__repr__()


class MongoProxy(object):

    """Proxy for MongoDB connection.

    Methods that are executable, i.e find, insert etc, get wrapped in an
    Executable-instance that handles AutoReconnect-exceptions transparently.
    """

    def __init__(self, conn, logger=None, wait_time=None):
        """conn is an ordinary MongoDB-connection."""
        if logger is None:
            import logging
            logger = logging.getLogger(__name__)

        self.conn = conn
        self.logger = logger
        self.wait_time = wait_time

    def __getitem__(self, key):
        """Create proxy around the method in the "key" connection."""
        return wrap(self.conn[key], key, self.logger, self.wait_time)

    def __getattr__(self, key):
        """Wrap method in class that handles AutoReconnect Exception.

        If key is the name of an executable method in the MongoDB connection,
        for instance find or insert.
        """
        return wrap(getattr(self.conn, key), key, self.logger, self.wait_time)

    def __call__(self, *args, **kwargs):
        """Execute when the instance is called."""
        return wrap(self.conn(*args, **kwargs), None, self.logger,
                    self.wait_time)

    def __dir__(self):
        """Override dir to make the proxy more transparent."""
        return dir(self.conn)

    def __str__(self):
        """Override str to make the proxy more transparent."""
        return self.conn.__str__()

    def __repr__(self):
        """Override repr to make the proxy more transparent."""
        return self.conn.__repr__()

    def __nonzero__(self):
        """."""
        return True
