from tingyun.api.transaction.base import current_transaction
from tingyun.api.tracert.database_trace import DatabaseTrace
from tingyun.api.tracert.function_trace import wrap_function_trace
import logging

_logger = logging.getLogger(__name__)


def detect(module):

    class CursorWrapper(object):

        def __init__(self, cursor, connect_params=None, cursor_params=None):
            object.__setattr__(self, '_ty_cursor', cursor)
            object.__setattr__(self, '_ty_connect_params', connect_params)
            object.__setattr__(self, '_ty_cursor_params', cursor_params)
            object.__setattr__(self, 'fetchone', cursor.fetchone)
            object.__setattr__(self, 'fetchmany', cursor.fetchmany)
            object.__setattr__(self, 'fetchall', cursor.fetchall)
            # self._ty_cursor = cursor
            # self._ty_connect_params = connect_params
            # self._ty_cursor_params = cursor_params

        def __setattr__(self, name, value):
            setattr(self._ty_cursor, name, value)

        def __getattr__(self, name):
            return getattr(self._ty_cursor, name)

        def __iter__(self):
            return iter(self._ty_cursor)

        def execute(self, sql, *args, **kwargs):
            transaction = current_transaction()
            if not transaction:
                return self._ty_cursor.execute(sql, *args, **kwargs)

            with DatabaseTrace(transaction, sql, module, self._ty_connect_params, self._ty_cursor_params,
                               (args, kwargs)):
                return self._ty_cursor.execute(sql, *args, **kwargs)

        def executemany(self, sql, *args, **kwargs):
            transaction = current_transaction()
            if not transaction:
                return self._ty_cursor.executemany(sql, *args, **kwargs)

            with DatabaseTrace(transaction, sql, module):
                return self._ty_cursor.executemany(sql, *args, **kwargs)

        def callproc(self, procname, *args, **kwargs):
            transaction = current_transaction()
            if not transaction:
                return self._ty_cursor.callproc(procname, *args, **kwargs)
            with DatabaseTrace(transaction, 'CALL %s' % procname):
                return self._ty_cursor.callproc(procname, *args, **kwargs)

    class ConnectionWrapper(object):

        def __init__(self, connection, connect_params=None):
            object.__setattr__(self, '_ty_connection', connection)
            object.__setattr__(self, '_ty_connect_params', connect_params)

        def __setattr__(self, name, value):
            setattr(self._ty_connection, name, value)

        def __getattr__(self, name):
            return getattr(self._ty_connection, name)

        def cursor(self, *args, **kwargs):
            return CursorWrapper(self._ty_connection.cursor(*args, **kwargs), self._ty_connect_params, (args, kwargs))

        def commit(self):
            transaction = current_transaction()
            if not transaction:
                return self._ty_connection.commit()

            with DatabaseTrace(transaction, 'COMMIT', module):
                return self._ty_connection.commit()

        def rollback(self):
            transaction = current_transaction()
            if not transaction:
                return self._ty_connection.rollback()

            with DatabaseTrace(transaction, 'ROLLBACK', module):
                return self._ty_connection.rollback()

    class ConnectionFactory(object):

        def __init__(self, connect):
            self.__connect = connect

        def __call__(self, *args, **kwargs):
            return ConnectionWrapper(self.__connect(*args, **kwargs), (args, kwargs))

    # Check if module is already wrapped by tingyun
    if hasattr(module, '_ty_dbapi2_wrapped'):
        return

    # equal to import the mysql.Connect.connect object
    wrap_function_trace(module, 'connect', name='%s:%s' % (module.__name__, 'connect'))

    module.connect = ConnectionFactory(module.connect)
    module._ty_dbapi2_wrapped = True
