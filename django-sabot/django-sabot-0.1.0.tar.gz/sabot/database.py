from __future__ import unicode_literals

from django.db import connection

from .classes import Patcher

__all__ = ('ConnectPatcher', 'CursorPatcher')


class DatabasePatcher(Patcher):
    """
    Base class that allow monkey patching parts of Django database backends
    system.
    """

    def __init__(self, error_producer, kwargs):
        self.error_producer = error_producer
        self.kwargs = kwargs

    def return_patched(self, old_method):
        error_producer_instance = self.error_producer(**self.kwargs)

        def inner(self, *args, **kwargs):
            error_producer_instance.check(*args, **kwargs)
            return old_method(self, *args, **kwargs)

        return inner

    def post_patch(self):
        connection.cursor().close()
        connection.close()


class ConnectPatcher(DatabasePatcher):
    """
    DatabasePatcher subclass that allow monkey patching the connect method of
    the django.db.backends.BaseDatabaseWrapper
    """

    path = 'django.db.backends.BaseDatabaseWrapper'
    method_name = 'connect'

    def post_patch(self):
        connection.cursor().close()
        connection.close()


class CursorPatcher(DatabasePatcher):
    """
    DatabasePatcher subclass that allow monkey patching the cursor method of
    the django.db.backends.BaseDatabaseWrapper
    """

    path = 'django.db.backends.BaseDatabaseWrapper'
    method_name = 'cursor'
