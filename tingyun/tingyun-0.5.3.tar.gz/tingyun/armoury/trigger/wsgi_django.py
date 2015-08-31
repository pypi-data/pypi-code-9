
"""define the trigger for the specified weapon

"""

import logging
import sys

from tingyun.logistics.basic_wrapper import wrap_object, FunctionWrapper
from tingyun.logistics.object_name import callable_name
from tingyun.armoury.ammunition.django_tracker import WSGIApplicationResponse
from tingyun.armoury.ammunition.function_tracker import FunctionTracker, function_trace_wrapper
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.battlefield.tracer import Tracer
from tingyun.battlefield.proxy import proxy_instance


console = logging.getLogger(__name__)


def wsgi_wrapper_inline(wrapped, framework, version):
    """ wrap the uwsgi application entrance
    :param wrapped: the method need to be wrapped
    :return:
    """

    # the wsgi.__call__ will passed two parameters with environ, and start_response
    def wrapper(wrapped, instance, args, kwargs):
        environ, start_response = args

        if isinstance(wrapped, tuple):
            (instance, wrapped) = wrapped

        tracker = current_tracker()
        if tracker:
            return wrapped(environ, start_response)

        tracker = Tracer(proxy_instance(), environ, framework)
        tracker.start_work()

        # respect the wsgi protocol
        def _start_response(status, response_headers, *args):
            # deal the response data
            tracker.deal_response(status, response_headers, *args)
            _write = start_response(status, response_headers, *args)

            def write(data):
                ret = _write(data)
                return ret

            return write

        result = []
        try:
            tracker.set_tracker_name(callable_name(wrapped), priority=1)
            application = function_trace_wrapper(wrapped)
            with FunctionTracker(tracker, name='Application', group='Python.WSGI'):
                result = application(environ, _start_response)
        except:
            console.warning("Errors occurred, when do the tracker. %s", sys.exc_info())
            tracker.finish_work(*sys.exc_info())
            raise

        return WSGIApplicationResponse(tracker, result)

    return FunctionWrapper(wrapped, wrapper)


def wsgi_application_wrapper(module, object_path, *framework):
    """
    :param module:
    :param object_path:
    :return:
    """
    wrap_object(module, object_path, wsgi_wrapper_inline, *framework)
