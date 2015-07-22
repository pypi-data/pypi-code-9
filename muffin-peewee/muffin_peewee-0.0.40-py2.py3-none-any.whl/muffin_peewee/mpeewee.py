import muffin
import peewee
import asyncio

from playhouse.db_url import parseresult_to_dict, urlparse, schemes
from playhouse.pool import PooledDatabase


class _ConnectionTaskLocal(peewee._BaseConnectionLocal, muffin.local):

    pass


class AsyncDatabase(peewee.Database):

    def async_init(self, loop):
        self.__local = _ConnectionTaskLocal(loop=loop)
        self.__async_lock = asyncio.Lock()

    def async(method):

        @asyncio.coroutine
        def wrapper(self):
            if self.deferred:
                raise Exception('Error, database not properly initialized before connect')

            with (yield from self.__async_lock):
                with self.exception_wrapper():
                    method(self)

        return wrapper

    @async
    def async_connect(self):
        self.__local.conn = self._connect(self.database, **self.connect_kwargs)
        self.__local.closed = False
        self.initialize_connection(self.__local.conn)
        return self.__local.conn

    @async
    def async_close(self):
        self._close(self.__local.conn)
        self.__local.closed = True


class AsyncPooledDatabase(PooledDatabase):
    pass


schemes['sqlite'] = type('SqliteDatabase', (peewee.SqliteDatabase, AsyncDatabase), {})
schemes['mysql'] = type('MySQLDatabase', (peewee.MySQLDatabase, AsyncDatabase), {})
schemes['postgres'] = schemes['postgresql'] = type(
    'PostgresqlDatabase', (peewee.PostgresqlDatabase, AsyncDatabase), {})
schemes['mysql+pool'] = type(
    'PooledMySQLDatabase', (peewee.MySQLDatabase, AsyncPooledDatabase), {})
schemes['posgres+pool'] = schemes['postgresql+pool'] = type(
    'PooledPostgresqlDatabase', (peewee.PostgresqlDatabase, AsyncPooledDatabase), {})


def connect(url, **connect_params):
    parsed = urlparse(url)
    connect_kwargs = parseresult_to_dict(parsed)
    connect_kwargs.update(connect_params)
    database_class = schemes.get(parsed.scheme)

    if database_class is None:
        if database_class in schemes:
            raise RuntimeError('Attempted to use "%s" but a required library '
                               'could not be imported.' % parsed.scheme)
        raise RuntimeError('Unrecognized or unsupported scheme: "%s".' % parsed.scheme)

    return database_class(**connect_kwargs)
