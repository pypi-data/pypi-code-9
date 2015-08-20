import logging
from tingyun.api.tracert.time_trace import TimeTrace
from tingyun.api.tracert.function_node import FunctionNode
from tingyun.api.transaction.base import current_transaction
from tingyun.api.objects.object_name import callable_name
from tingyun.api.objects.object_wrapper import FunctionWrapper
from tingyun.api.objects.object_wrapper import wrap_object

_logger = logging.getLogger(__name__)


class FunctionTrace(TimeTrace):
    """
    """
    def __init__(self, transaction, name, group=None, label=None, params=None):
        super(FunctionTrace, self).__init__(transaction)

        self.name = name
        self.group = group or 'Function'
        self.label = label
        self.params = params

    def create_node(self):
        """create function trace node
        """
        return FunctionNode(group=self.group, name=self.name, children=self.children, start_time=self.start_time,
                            end_time=self.end_time, duration=self.duration, exclusive=self.exclusive, label=self.label,
                            params=self.params)

    def finalize_data(self):
        """create all the data if need
        :return:
        """
        pass


def FunctionTraceWrapper(wrapped, name=None, group=None, label=None, params=None):

    def dynamic_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        if callable(name):
            if instance is not None:
                _name = name(instance, *args, **kwargs)
            else:
                _name = name(*args, **kwargs)

        elif name is None:
            _name = callable_name(wrapped)

        else:
            _name = name

        if callable(group):
            if instance is not None:
                _group = group(instance, *args, **kwargs)
            else:
                _group = group(*args, **kwargs)

        else:
            _group = group

        if callable(label):
            if instance is not None:
                _label = label(instance, *args, **kwargs)
            else:
                _label = label(*args, **kwargs)

        else:
            _label = label

        if callable(params):
            if instance is not None:
                _params = params(instance, *args, **kwargs)
            else:
                _params = params(*args, **kwargs)

        else:
            _params = params

        with FunctionTrace(transaction, _name, _group, _label, _params):
            return wrapped(*args, **kwargs)

    def literal_wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        _name = name or callable_name(wrapped)

        with FunctionTrace(transaction, _name, group, label, params):
            return wrapped(*args, **kwargs)

    if callable(name) or callable(group) or callable(label) or callable(params):
        return FunctionWrapper(wrapped, dynamic_wrapper)

    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_function_trace(module, object_path, name=None, group=None, label=None, params=None):
    return wrap_object(module, object_path, FunctionTraceWrapper, (name, group, label, params))
