import logging

from tingyun.api.tracert.memcache_node import MemcacheNode
from tingyun.api.objects.object_wrapper import wrap_object, FunctionWrapper
from tingyun.api.tracert.time_trace import TimeTrace
from tingyun.api.transaction.base import current_transaction

_logger = logging.getLogger(__name__)


class MemcacheTrace(TimeTrace):
    def __init__(self, transaction, command):
        super(MemcacheTrace, self).__init__(transaction)
        self.command = command

    def create_node(self):
        return MemcacheNode(command=self.command, children=self.children, start_time=self.start_time,
                            end_time=self.end_time, duration=self.duration, exclusive=self.exclusive)

    def terminal_node(self):
        return True


def memcached_trace_wrapper(wrapped, command):
    """
    :return:
    """
    def dynamic_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()
        if transaction is None:
            return wrapped(*args, **kwargs)

        if instance is not None:
            _command = command(instance, *args, **kwargs)
        else:
            _command = command(*args, **kwargs)

        with MemcacheTrace(transaction, _command):
            return wrapped(*args, **kwargs)

    def literal_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()
        if transaction is None:
            return wrapped(*args, **kwargs)

        with MemcacheTrace(transaction, command):
            return wrapped(*args, **kwargs)

    if callable(command):
        return FunctionWrapper(wrapped, dynamic_wrapper)

    return FunctionWrapper(wrapped, literal_wrapper)


# egg: (memcached, Client.append, get)
def wrap_memcache_trace(module, object_path, command):
    wrap_object(module, object_path, memcached_trace_wrapper, (command,))
