"""this module define the web framework basic entrance

"""
import logging
import sys

from tingyun.api.objects.object_wrapper import wrap_object, FunctionWrapper
from tingyun.api.transaction.base import current_transaction
from tingyun.api.transaction.web_transaction import WebTransaction
from tingyun.api.tracert.proxy import proxy_instance
from tingyun.api.tracert.function_trace import FunctionTrace, FunctionTraceWrapper
from tingyun.api.objects.wsgi_wrapper import WSGIInputWrapper, WSGIApplicationIterable
from tingyun.api.objects.object_name import callable_name


_logger = logging.getLogger(__name__)


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

        transaction = current_transaction()
        if transaction:
            return wrapped(environ, start_response)

        transaction = WebTransaction(proxy_instance(), environ, framework)
        transaction.__enter__()
        transaction.set_transaction_name(callable_name(wrapped), priority=1)

        # respect the wsgi protocol
        def _start_response(status, response_headers, *args):
            # deal the response data
            transaction.deal_response(status, response_headers, *args)
            _write = start_response(status, response_headers, *args)

            def write(data):
                ret = _write(data)
                return ret

            return write

        result = []
        try:
            if 'wsgi.input' in environ:
                environ['wsgi.input'] = WSGIInputWrapper(transaction, environ['wsgi.input'])

            application = FunctionTraceWrapper(wrapped)
            with FunctionTrace(transaction, name='Application', group='Python.WSGI'):
                result = application(environ, _start_response)
        except:
            _logger.warning("Errors occurred, when do the transaction. %s", sys.exc_info())
            transaction.__exit__(*sys.exc_info())
            raise

        return WSGIApplicationIterable(transaction, result)

    return FunctionWrapper(wrapped, wrapper)


def wsgi_application_wrapper(module, object_path, *framework):
    """
    :param module:
    :param object_path:
    :return:
    """
    wrap_object(module, object_path, wsgi_wrapper_inline, *framework)