
"""Define this module for basic armory for flask

"""

from tingyun.armoury.trigger.wsgi_django import wsgi_application_wrapper
from tingyun.armoury.ammunition.function_tracker import wrap_function_trace
from tingyun.armoury.ammunition.flask_tracker import add_url_rule_wrapper, handle_exception_wrapper
from tingyun.logistics.basic_wrapper import wrap_function_wrapper


def detect_wsgi_entrance(module):
    """
    :param module:
    :return:
    """
    wsgi_application_wrapper(module.Flask, '__call__', ('flask', ))


def detect_app_entrance(module):
    """
    :param module:
    :return:
    """
    # trace the views function call metric
    wrap_function_wrapper(module.Flask, 'add_url_rule', add_url_rule_wrapper)
    wrap_function_wrapper(module.Flask, 'handle_exception', handle_exception_wrapper)

    # new feature form flask 0.7
    if hasattr(module.Flask, 'handle_user_exception'):
        wrap_function_wrapper(module.Flask, 'handle_user_exception', handle_exception_wrapper)

    # new feature form flask 0.7
    if hasattr(module.Flask, 'full_dispatch_request'):
        wrap_function_trace(module.Flask, 'full_dispatch_request')


def detect_templates(module):
    """
    :param module:
    :return:
    """
    wrap_function_trace(module, '_render')