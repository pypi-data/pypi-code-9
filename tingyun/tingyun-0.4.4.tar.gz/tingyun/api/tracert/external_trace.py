import logging
from tingyun.api.tracert.time_trace import TimeTrace
from tingyun.api.tracert.external_node import ExternalNode
from tingyun.api.transaction.base import current_transaction
from tingyun.api.objects.object_wrapper import FunctionWrapper, wrap_object

_logger = logging.getLogger(__name__)


class ExternalTrace(TimeTrace):
    """define the external trace common api.

    """
    def __init__(self, transaction, library, url):
        super(ExternalTrace, self).__init__(transaction)

        self.library = library
        self.url = url

    def create_node(self):
        return ExternalNode(library=self.library, url=self.url, children=self.children,
                            start_time=self.start_time, end_time=self.end_time, duration=self.duration,
                            exclusive=self.exclusive)

    def terminal_node(self):
        return True


def external_trace_wrapper(wrapped, library, url):

    def dynamic_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        _url = url
        if callable(url):
            if instance is not None:
                _url = url(instance, *args, **kwargs)
            else:
                _url = url(*args, **kwargs)

        with ExternalTrace(transaction, library, _url):
            return wrapped(*args, **kwargs)

    def literal_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        with ExternalTrace(transaction, library, url):
            return wrapped(*args, **kwargs)

    if callable(url):
        return FunctionWrapper(wrapped, dynamic_wrapper)

    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_external_trace(module, object_path, library, url):
    wrap_object(module, object_path, external_trace_wrapper, (library, url))
