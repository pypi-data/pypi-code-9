
"""
"""

import logging

from tingyun.armoury.trigger.wsgi_tornado import wsgi_application_wrapper, wsgi_container_wrapper
from tingyun.armoury.trigger.async_tornado import connection_on_headers_wrapper, connection_on_request_body_wrapper
from tingyun.armoury.trigger.async_tornado import http_request_finish_wrapper, connection_finish_wrapper


console = logging.getLogger(__name__)


def detect_wsgi_entrance(module):
    """
    :param module:
    :return:
    """
    import tornado
    version = tornado.version

    # new feature in tornado 4.x
    if hasattr(module, 'WSGIAdapter'):
        wsgi_application_wrapper(module.WSGIAdapter, "__call__", "Tornado", version)

    if hasattr(module, "WSGIApplication"):
        wsgi_application_wrapper(module.WSGIApplication, "__call__", "Tornado", version)

    if hasattr(module, "WSGIContainer"):
        wsgi_container_wrapper(module.WSGIApplication, "__call__", "Tornado", version)


# There is much different in tornado version 3.x and 4.x. So deal the two version separately
#
# detect the tornado 3.x

def detect_tornado3_main_process(module):
    """all of the data handled in HTTPConnection class, include build header/body/finish
    :param module:
    :return:
    """

    # first step for process
    if hasattr(module, 'HTTPConnection'):
        module.HTTPConnection._on_headers = connection_on_headers_wrapper(module.HTTPConnection._on_headers)

    # second step for process
    if hasattr(module, 'HTTPConnection'):
        module.HTTPConnection._on_request_body = connection_on_request_body_wrapper(module.HTTPConnection._on_request_body)

    # third step for process
    if hasattr(module, "HTTPRequest"):
        module.HTTPRequest.finish = http_request_finish_wrapper(module.HTTPRequest.finish)

    # fourth step for process
    if hasattr(module, "HTTPConnection"):
        module.HTTPConnection.finish = connection_finish_wrapper(module.HTTPConnection.finish)
