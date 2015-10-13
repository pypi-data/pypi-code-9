
"""this module is implement some wrapper for trace the tornado module

"""

import logging
import weakref
import sys

from tingyun.logistics.object_name import callable_name
from tingyun.battlefield.proxy import proxy_instance
from tingyun.battlefield.tracer import Tracer
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.armoury.trigger.wsgi_tornado import process_environ
from tingyun.armoury.ammunition.function_tracker import FunctionTracker
from tingyun.logistics.basic_wrapper import FunctionWrapper


console = logging.getLogger(__name__)


def connection_on_headers_wrapper(wrapped, framework="Tornado", version='0'):
    """This is entrance for handle the request. so we start our tracer from here.
    :param wrapped:
    :return:
    """
    def wrapper(wrapped, connection, args, kwargs):
        """At this wrapper. we only init some environment for agent.nothing need to be done.
        :param wrapped:wrapped func
        :param connection: connection instance for current request
        :param args:
        :param kwargs:
        :return:
        """
        # add some ensurence for potential error, if this occurred, that indicate some wrong with last trace.
        # Then we drop the last trace and ignore this trace now.
        tracer = current_tracker()
        if tracer:
            console.warning("Unexpected situation arise, but no side effect to use the agent. That's only indicate "
                            "some illogicality trace in tracer. if this continue, please report to us, thank u.")
            tracer.drop_tracker()
            return wrapped(*args, **kwargs)

        # check the request status.
        if connection.stream.closed() or connection._request_finished:
            console.info("stream closed(%s). or connection finished(%s).", connection.stream.closed(), connection._request_finished)
            return

        wrapped(*args, **kwargs)

        # Because of the asynchronous and single thread feature. we store the tracer in the request.
        # we use _self_ to prevent conflict to the wrapped func namespace.
        request = connection._request
        if not request or hasattr(request, '_self_tracer'):
            console.info("request(%s) or has _self_tracer(%s)", request, hasattr(request, '_self_tracer'))
            return

        tracer = Tracer(proxy_instance(), process_environ({}, request), framework)
        tracer.start_work()
        request._self_tracer = tracer
        tracer.set_tracker_name(callable_name(tracer))
        try:
            # between header and body maybe blocked. so we calculate the block time.
            # if some code blocked. the http server will deal the other request, so will should drop the tracer from
            # thread cache.
            request._self_request_finished = False
            tracer._self_request = weakref.ref(request)
            tracer.drop_tracker()
        except Exception as err:
            request._self_tracer = None
            tracer.__exit__(*sys.exc_info())
            console.exception("Tornado raise error in HTTPConnection on_headers. %s", err)
            raise

    return FunctionWrapper(wrapped, wrapper)


def connection_on_request_body_wrapper(wrapped):
    """
    :param wrapped:
    :return:
    """
    def wrapper(wrapped, connection, args, kwargs):
        """
        :param wrapped:
        :param connection:
        :param args:
        :param kwargs:
        :return:
        """
        request = connection._request
        if not hasattr(request, '_self_tracer') or not request._self_tracer:
            console.info("body do not get the tracer...")
            return wrapped(*args, **kwargs)

        # We can not the tracer at the tracert of the user application. so we should restore to the thread cache.
        tracer = request._self_tracer
        tracer.save_tracker()

        try:
            console.info("execute the body...")
            return wrapped(*args, **kwargs)
        except Exception as err:
            tracer.__exit__(*sys.exc_info())
            console.exception("Tornado raise error in HTTPConnection on_request_body. %s", err)
            raise

    return FunctionWrapper(wrapped, wrapper)


def http_request_finish_wrapper(wrapped):
    """
    :param wrapped:
    :return:
    """
    def wrapper(wrapped, request, args, kwargs):
        """
        :param wrapped:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tracer = getattr(request, '_self_tracer', None)
        if not tracer:
            return wrapped(*args, **kwargs)

        current_tracer = current_tracker()
        if current_tracer:
            console.info("got the tracker is not equal to current.")
            if tracer != current_tracer:
                try:
                    current_tracer.drop_transaction()
                    return wrapper(wrapped, request, args, kwargs)
                finally:
                    current_tracer.save_transaction()
            else:
                return wrapped(*args, **kwargs)

        tracer.save_tracker()

        try:
            if not request.connection.stream.writing():
                tracer.__exit__(None, None, None)
                request._self_tracer = None
            else:
                tracer.drop_transaction()
        except Exception as err:
            tracer.__exit__(*sys.exc_info())
            console.exception("Tornado raise error in HTTPRequest finish. %s", err)
            raise

    return FunctionWrapper(wrapped, wrapper)


def connection_finish_wrapper(wrapped):
    """
    :param wrapped:
    :return:
    """
    def wrapper(wrapped, connection, args, kwargs):
        """
        :param wrapped:
        :param connection:
        :param args:
        :param kwargs:
        :return:
        """
        request = connection._request
        tracer = current_tracker()

        if tracer:
            return wrapped(*args, **kwargs)
        else:
            if not hasattr(request, '_self_tracer'):
                return wrapped(*args, **kwargs)

            tracer = request._self_tracer
            tracer.save_tracker()
            console.info("get unfinished tracker.")

            try:
                result = wrapped(*args, **kwargs)
                tracer.__exit__(None, None, None)
            except Exception as err:
                tracer.__exit__(*sys.exc_info())
                console.exception("Tornado raise error in HTTPConnection finish. %s", err)
                raise
            finally:
                request._self_tracer = None

            return result

    return FunctionWrapper(wrapped, wrapper)
