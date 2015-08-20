import functools

from tingyun.api.objects.object_wrapper import FunctionWrapper, wrap_object
from tingyun.api.transaction.base import current_transaction


class ErrorTrace(object):
    def __init__(self, transaction, ignore_errors=None):
        self._transaction = transaction
        self._ignore_errors = ignore_errors

    def __enter__(self):
        return self

    def __exit__(self, exc, value, tb):
        if exc is None or value is None or tb is None:
            return

        if self._transaction is None:
            return

        self._transaction.record_exception(exc=exc, value=value, tb=tb, ignore_errors=self._ignore_errors)


def error_trace_wrapper(wrapped, ignore_errors=None):

    def wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        with ErrorTrace(transaction, ignore_errors):
            return wrapped(*args, **kwargs)

    return FunctionWrapper(wrapped, wrapper)


def wrap_error_trace(module, object_path, ignore_errors=None):
    wrap_object(module, object_path, error_trace_wrapper, (ignore_errors, ))
