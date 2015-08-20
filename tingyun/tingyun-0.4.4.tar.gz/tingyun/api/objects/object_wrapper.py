
import logging

from tingyun.api.wrapt.wrappers import (FunctionWrapper as _FunctionWrapper)
from tingyun.api.wrapt.wrappers import BoundFunctionWrapper as _BoundFunctionWrapper

from tingyun.api.wrapt.wrappers import wrap_object as _wrap_object, wrap_function_wrapper as _wrap_function_wrapper
from tingyun.api.wrapt.wrappers import function_wrapper as _function_wrapper

_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# following method are used the wrapt module instead.
# all methods would send from this module, not use the wrapt package directly

# egg: (memcached, Client.append, MemcacheTraceWrapper(), get)
wrap_object = _wrap_object

# for wrap the function(bound/unbound)
FunctionWrapper = _FunctionWrapper
BoundFunctionWrapper = _BoundFunctionWrapper

wrap_function_wrapper = _wrap_function_wrapper

function_wrapper = _function_wrapper

# -----------------------------------------------------------------------------


def wrap_middle_function_trace(module, object_path, middle_wrapper, function):
    """
    :param module: the module need to be wrapped
    :param object_path: the patched method.
    :param middle_wrapper: middle wrapper, used to execute wrapper
    :param function: wrapper to target module.
    :return:
    """
    return wrap_object(module, object_path, middle_wrapper, (function,))
