
""" define this module used to define the wrapper for django

"""
import logging
import threading

from tingyun.api.tracert.function_trace import FunctionTrace
from tingyun.api.transaction.base import current_transaction
from tingyun.api.objects.object_name import callable_name
from tingyun.api.objects.object_wrapper import FunctionWrapper, wrap_middle_function_trace

_logger = logging.getLogger(__name__)
middleware_detect_lock = threading.Lock()


def should_ignore(exc, value, tb, ignore_status_code=[]):
    from django.http import Http404

    if isinstance(value, Http404) and 404 in ignore_status_code:
        return True

    return False


def wrap_view_dispatch(wrapped):
    """ wrap the inline view class
    :param wrapped: the method need to be wrapped
    :return:
    """
    def wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        def _args(request, *args, **kwargs):
            """acquire the http request from parameters passed to Views.dispatch() function
            """
            return request

        view = instance
        request = _args(*args, **kwargs)

        if request.method.lower() in view.http_method_names:
            handler = getattr(view, request.method.lower(), view.http_method_not_allowed)
        else:
            handler = view.http_method_not_allowed

        name = callable_name(handler)
        transaction.set_transaction_name(name)

        with FunctionTrace(transaction, name=name):
            return wrapped(*args, **kwargs)

    return FunctionWrapper(wrapped, wrapper)


def wrap_template_block(wrapped):
    """ Note: template is the last step for response http request. we do not use the name as transaction name
    :param wrapped: function/method need to be wrapt
    :return: wrapper function/method object
    """

    def wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        with FunctionTrace(transaction, name=instance.name, group='Template.Block'):
            return wrapped(*args, **kwargs)

    return FunctionWrapper(wrapped, wrapper)


def wrap_view_handler(wrapped, priority=3):
    """
    :param wrapped:
    :param priority:
    :return:
    """
    # views handler maybe called twice on same ResolverMatch. so mark it
    if hasattr(wrapped, '_self_django_view_handler_wrap_status'):
        return wrapped

    name = callable_name(wrapped)

    def wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        transaction.set_transaction_name(name, priority=priority)
        with FunctionTrace(transaction, name=name):
            try:
                return wrapped(*args, **kwargs)
            except:  # Catch all
                transaction.record_exception(ignore_errors=should_ignore)
                raise

    result = FunctionWrapper(wrapped, wrapper)
    result._self_django_view_handler_wrap_status = True

    return result


def wrap_url_resolver(wrapped):
    """
    :param wrapped:
    :return:
    """
    name = callable_name(wrapped)

    def wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        if hasattr(transaction, '_self_django_url_resolver_wrap_status'):
            return wrapped(*args, **kwargs)

        # mark the top level(views maybe has inline local url resolver operate) url resolver. and use it as the
        transaction._self_django_url_resolver_wrap_status = True

        def _wrapped(path):
            with FunctionTrace(transaction, name=name, label=path):
                result = wrapped(path)

                if isinstance(type(result), tuple):
                    callback, callback_args, callback_kwargs = result
                    result = (wrap_view_handler(callback, priority=4), callback_args, callback_kwargs)
                else:
                    result.func = wrap_view_handler(result.func, priority=4)

                return result

        try:
            return _wrapped(*args, **kwargs)
        finally:
            del transaction._self_django_url_resolver_wrap_status

    return FunctionWrapper(wrapped, wrapper)


def wrap_url_resolver_nnn(wrapped, priority=1):
    """
    :param wrapped:
    :param priority:
    :return:
    """
    name = callable_name(wrapped)

    def wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        with FunctionTrace(transaction, name=name):
            callback, param_dict = wrapped(*args, **kwargs)
            return wrap_view_handler(callback, priority=priority), param_dict

    return FunctionWrapper(wrapped, wrapper)


def _do_wrap_middleware(middleware, detect_name=False):
    """
    :param middleware: the middleware list in django setting
    :return:
    """
    def wrapper(wrapped):
        name = callable_name(wrapped)

        def wrapper(wrapped, instance, args, kwargs):
            transaction = current_transaction()
            if transaction is None:
                return wrapped(*args, **kwargs)

            before_name = "%s.%s" % (transaction.name, transaction.group)
            with FunctionTrace(transaction, name=name):
                try:
                    return wrapped(*args, **kwargs)
                finally:
                    after_name = "%s.%s" % (transaction.name, transaction.group)
                    if before_name == after_name and detect_name:
                        transaction.set_transaction_name(name, priority=2)

        return FunctionWrapper(wrapped, wrapper)

    for wrapped in middleware:
        yield wrapper(wrapped)


def wrap_middleware(handler, *args, **kwargs):
    """
    :param handler: the base handler of http
    :return:
    """
    # avoiding two threads deal it in same time
    global middleware_detect_lock
    if not middleware_detect_lock:
        return

    lock = middleware_detect_lock
    lock.acquire()
    if not middleware_detect_lock:
        lock.release()
        return

    middleware_detect_lock = None

    try:
        # for inserting RUM header and footer. indicate it's wrapped and timed as well
        if hasattr(handler, '_response_middleware'):
            pass

        if hasattr(handler, '_request_middleware'):
            handler._request_middleware = list(_do_wrap_middleware(handler._request_middleware, True))

        if hasattr(handler, '_view_middleware'):
            handler._view_middleware = list(_do_wrap_middleware(handler._view_middleware, True))

        if hasattr(handler, '_template_response_middleware'):
            handler._template_response_middleware = list(_do_wrap_middleware(handler._template_response_middleware))

        if hasattr(handler, '_response_middleware'):
            handler._response_middleware = list(_do_wrap_middleware(handler._response_middleware))

        if hasattr(handler, '_exception_middleware'):
            handler._exception_middleware = list(_do_wrap_middleware(handler._exception_middleware))
    finally:
        lock.release()


def middleware_trace_wrapper(wrapped, wrapper_function):
    """
    :return:
    """
    def dynamic_wrapper(wrapped, instance, args, kwargs):
        """
        """
        result = wrapped(*args, **kwargs)

        if instance is not None:
            wrapper_function(instance, *args, **kwargs)
        else:
            wrapper_function(*args, **kwargs)
        return result

    return FunctionWrapper(wrapped, dynamic_wrapper)


def wrap_middleware_trace(module, object_path):
    """
    :return:
    """
    return wrap_middle_function_trace(module, object_path, middleware_trace_wrapper, wrap_middleware)

