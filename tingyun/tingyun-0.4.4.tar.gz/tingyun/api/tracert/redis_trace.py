"""this module used to wrap the specify method to RedisTrace

"""

from tingyun.api.tracert.time_trace import TimeTrace
from tingyun.api.transaction.base import current_transaction
from tingyun.api.objects.object_wrapper import wrap_object, FunctionWrapper
from tingyun.api.tracert.redis_node import RedisNode


class RedisTrace(TimeTrace):
    """
    """
    def __init__(self, transaction, command):
        """
        :return:
        """
        super(RedisTrace, self).__init__(transaction)
        self.command = command

    def create_node(self):
        """
        :return:
        """
        return RedisNode(command=self.command, children=self.children, start_time=self.start_time,
                         end_time=self.end_time, duration=self.duration, exclusive=self.exclusive)

    def terminal_node(self):
        return True


def redis_trace_wrapper(wrapped, command):
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

        with RedisTrace(transaction, _command):
            return wrapped(*args, **kwargs)

    def literal_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()
        if transaction is None:
            return wrapped(*args, **kwargs)

        with RedisTrace(transaction, command):
            return wrapped(*args, **kwargs)

    if callable(command):
        return FunctionWrapper(wrapped, dynamic_wrapper)

    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_redis_trace(module, object_path, command):
    wrap_object(module, object_path, redis_trace_wrapper, (command,))
