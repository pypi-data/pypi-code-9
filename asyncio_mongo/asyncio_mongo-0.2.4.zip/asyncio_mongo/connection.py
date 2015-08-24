import logging
from asyncio_mongo.auth import CredentialsAuthenticator
from asyncio_mongo.log import logger
from asyncio_mongo.database import Database
from .protocol import MongoProtocol
import asyncio

__all__ = ['Connection']


class Connection:
    """
    Wrapper around the protocol and transport which takes care of establishing
    the connection and reconnecting it.

    ::

        connection = yield from Connection.create(host='localhost', port=6379)
        result = yield from connection.set('key', 'value')
    """
    protocol = MongoProtocol
    """
    The :class:`MongoProtocol` class to be used this connection.
    """

    @classmethod
    @asyncio.coroutine
    def create(cls, host='localhost', port=27017, db=None, username=None, password=None, loop=None,
               auto_reconnect=True):
        connection = cls()

        connection.host = host

        connection.port = port
        connection._loop = loop
        connection._retry_interval = .5

        # Create protocol instance
        def connection_lost(exc):
            if auto_reconnect:
                logger.info("Connection lost, attempting to reconnect")
                asyncio.Task(connection._reconnect())

        connection._authenticators = {}
        connection._db_name = db
        if db and username:
            connection._authenticators[db] = CredentialsAuthenticator(username, password)

        connection.protocol = MongoProtocol(connection_lost_callback=connection_lost)

        # Connect
        if auto_reconnect:
            yield from connection._reconnect()
        else:
            yield from connection._connect_once()

        return connection

    @asyncio.coroutine
    def disconnect(self):
        yield from self.protocol.disconnect()

    @property
    def default_database(self):
        return self[self._db_name]

    @property
    def transport(self):
        """ The transport instance that the protocol is currently using. """
        return self.protocol.transport

    def _get_retry_interval(self):
        """ Time to wait for a reconnect in seconds. """
        return self._retry_interval

    def _reset_retry_interval(self):
        """ Set the initial retry interval. """
        self._retry_interval = .5

    def _increase_retry_interval(self):
        """ When a connection failed. Increase the interval."""
        self._retry_interval = min(60, 1.5 * self._retry_interval)

    def _connect_once(self):
        """
        If auto_reconnect is False try to connect just once. Raise exception if server is unavailable
        """
        loop = self._loop or asyncio.get_event_loop()
        try:
            logger.log(logging.INFO, 'Connecting to mongo without auto reconnect')
            yield from loop.create_connection(lambda: self.protocol, self.host, self.port)
        except ConnectionError as e:
            logging.log(logging.ERROR, 'Check if mongo server is running')
            raise e

    def _reconnect(self):
        """
        Set up Mongo connection.
        """
        loop = self._loop or asyncio.get_event_loop()
        while True:
            try:
                logger.log(logging.INFO, 'Connecting to mongo at {host}:{port}'.format(host=self.host, port=self.port))
                yield from loop.create_connection(lambda: self.protocol, self.host, self.port)
                self._reset_retry_interval()
                for name, auth in self._authenticators.items():
                    yield from auth.authenticate(Database(self.protocol, name))
                    logger.log(logging.INFO, 'Authenticated to database {name}'.format(name=name))
                return
            except OSError:
                # Sleep and try again
                self._increase_retry_interval()
                interval = self._get_retry_interval()
                logger.log(logging.INFO, 'Connecting to mongo failed. Retrying in %i seconds' % interval)
                yield from asyncio.sleep(interval)

    def __getitem__(self, database_name):
        return Database(self.protocol, database_name)

    def __getattr__(self, database_name):
        return self[database_name]

    def __repr__(self):
        return 'Connection(host=%r, port=%r)' % (self.host, self.port)
