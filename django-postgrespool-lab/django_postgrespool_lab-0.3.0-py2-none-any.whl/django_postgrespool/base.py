# -*- coding: utf-8 -*-

import logging
from functools import partial

from sqlalchemy import event
from sqlalchemy.pool import manage, QueuePool
from psycopg2 import InterfaceError, ProgrammingError, OperationalError

# from django.db import transaction

from django.conf import settings
from django.db.backends.postgresql_psycopg2.base import *
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as Psycopg2DatabaseWrapper
from django.db.backends.postgresql_psycopg2.creation import DatabaseCreation as Psycopg2DatabaseCreation

POOL_SETTINGS = 'DATABASE_POOL_ARGS'

# DATABASE_POOL_ARGS should be something like:
# {'max_overflow':10, 'pool_size':5, 'recycle':300}
pool_args = getattr(settings, POOL_SETTINGS, {})
db_pool = manage(Database, **pool_args)

log = logging.getLogger('z.pool')

def _log(message, *args):
    log.debug(message)

# Only hook up the listeners if we are in debug mode.
if settings.DEBUG:
    event.listen(QueuePool, 'checkout', partial(_log, 'retrieved from pool'))
    event.listen(QueuePool, 'checkin', partial(_log, 'returned to pool'))
    event.listen(QueuePool, 'connect', partial(_log, 'new connection'))


def is_disconnect(e, connection, cursor):
    """
    Connection state check from SQLAlchemy:
    https://bitbucket.org/sqlalchemy/sqlalchemy/src/tip/lib/sqlalchemy/dialects/postgresql/psycopg2.py
    """
    if isinstance(e, OperationalError):
        # these error messages from libpq: interfaces/libpq/fe-misc.c.
        # TODO: these are sent through gettext in libpq and we can't
        # check within other locales - consider using connection.closed
        return 'terminating connection' in str(e) or \
                'closed the connection' in str(e) or \
                'connection not open' in str(e) or \
                'could not receive data from server' in str(e)
    elif isinstance(e, InterfaceError):
        # psycopg2 client errors, psycopg2/conenction.h, psycopg2/cursor.h
        return 'connection already closed' in str(e) or \
                'cursor already closed' in str(e)
    elif isinstance(e, ProgrammingError):
        # not sure where this path is originally from, it may
        # be obsolete.   It really says "losed", not "closed".
        return "closed the connection unexpectedly" in str(e)
    else:
        return False


class DatabaseCreation(Psycopg2DatabaseCreation):
    def destroy_test_db(self, *args, **kw):
        """Ensure connection pool is disposed before trying to drop database."""
        self.connection._dispose()
        super(DatabaseCreation, self).destroy_test_db(*args, **kw)


class DatabaseWrapper(Psycopg2DatabaseWrapper):
    """SQLAlchemy FTW."""

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.creation = DatabaseCreation(self)

    def _commit(self):
        if self.connection is not None and self.is_usable():
            with self.wrap_database_errors:
                return self.connection.commit()

    def _rollback(self):
        if self.connection is not None and self.is_usable():
            with self.wrap_database_errors:
                return self.connection.rollback()

    def _dispose(self):
        """Dispose of the pool for this instance, closing all connections."""
        self.close()
        # _DBProxy.dispose doesn't actually call dispose on the pool
        conn_params = self.get_connection_params()
        key = db_pool._serialize(**conn_params)
        try:
            pool = db_pool.pools[key]
        except KeyError:
            pass
        else:
            pool.dispose()
            del db_pool.pools[key]

    def get_new_connection(self, conn_params):
        # get new connection through pool, not creating a new one outside.
        connection = db_pool.connect(**conn_params)
        return connection

    def _set_autocommit(self, autocommit):
        # fix autocommit setting not working in proxied connection
        with self.wrap_database_errors:
            if self.psycopg2_version >= (2, 4, 2):
                self.connection.connection.autocommit = autocommit
            else:
                if autocommit:
                    level = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
                else:
                    level = self.isolation_level
                self.connection.connection.set_isolation_level(level)
