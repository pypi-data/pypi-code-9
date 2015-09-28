import logging
import os
import rethinkdb as rethink
from .base import DatabaseBackendBase

logger = logging.getLogger(__name__)


try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    has_django = True
except ImportError, e:
    has_django = False


if has_django:
    try:
        RETHINK_HOST = getattr(settings, 'DOMINGO_RETHINK_HOST', 'localhost')
        RETHINK_PORT = getattr(settings, 'DOMINGO_RETHINK_PORT', '28015')
        RETHINK_DB = getattr(settings, 'DOMINGO_RETHINK_DB', 'rethink_domingo_test')
    except ImproperlyConfigured, e:
        has_django = False


if not has_django:
    RETHINK_HOST = os.environ.get('DOMINGO_RETHINK_HOST', 'localhost')
    RETHINK_PORT = os.environ.get('DOMINGO_RETHINK_PORT', '28015')
    RETHINK_DB = os.environ.get('DOMINGO_RETHINK_DB', 'rethink_domingo_test')

rtconnection = rethink.connect(
    host=RETHINK_HOST, port=RETHINK_PORT
)
try:
    rethink.db_create(RETHINK_DB).run(rtconnection)
except rethink.RqlRuntimeError:
    pass
    # rtconnection.close()


def connect(f):
    def wrapper(self, *args, **kwargs):
        self._setup_connection()
        return f(self, *args, **kwargs)
    return wrapper


class RethinkStore(DatabaseBackendBase):

    tables = {}

    def __init__(self, namespace, **kwargs):
        self.namespace = namespace
        self._setup_connection()
        try:
            rethink.db(settings.RETHINK_DB).table_create(
                self.namespace, primary_key='outlet_token'
            ).run(self.connection)
        except rethink.RqlRuntimeError:
            logger.debug('table %s already exists', self.namespace)
        try:
            rethink.db(settings.RETHINK_DB).table_create(
                self.namespace+'_scores'
            ).run(self.connection)
            rethink.db(settings.RETHINK_DB).table(
                self.namespace+'_scores'
            ).index_create('outlet_token').run(self.connection)
        except rethink.RqlRuntimeError:
            logger.debug('table %s already exists', self.namespace)

    def _setup_connection(self):
        self.connection = rethink.connect(
            host=settings.RETHINK_HOST, port=settings.RETHINK_PORT
        )

    @connect
    def commit_bulk_save(self):

        rethink.db(settings.RETHINK_DB).table(self.namespace).insert(
            [data.as_dict() for id, data in self.bulk_query],
            upsert=True
            ).run(self.connection)

        rethink.db(settings.RETHINK_DB).table(self.namespace+'_scores').insert(
            [data.as_dict() for id, data in self.bulk_query],
            # durability='soft',
            ).run(self.connection)

        self.connection.close()

    @connect
    def commit_bulk_get(self, time_series=0):
        if not len(self.bulk_query):
            return []

        query = rethink.db(settings.RETHINK_DB).table(
            self.namespace).get_all(
                *[k.split('.')[-1] for k in self.bulk_query]
            ).eq_join(
                'outlet_token', rethink.db(
                    settings.RETHINK_DB
                ).table(self.namespace+'_scores')
            ).distinct().zip().order_by(rethink.desc('time'))

        data = query.run(self.connection)
        self.connection.close()
        return data

    @connect
    def get(self, key):
        key = key.split('.')[-1]
        data = rethink.db(settings.RETHINK_DB).table(
            self.namespace+'_scores').filter(
                'outlet_token', key).eq_join(
                    'outlet_token',
                    rethink.db(settings.RETHINK_DB).table(
                        self.namespace)
                    ).order_by(
                        rethink.desc('time')
                    ).limit(1).zip().run(self.connection)
        if data:
            return data[0]
