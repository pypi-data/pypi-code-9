
"""this module is implement the function detector for flask

"""
import logging
from tingyun.logistics.basic_wrapper import FunctionWrapper
from tingyun.logistics.object_name import callable_name
from tingyun.armoury.ammunition.function_tracker import FunctionTracker
from tingyun.armoury.ammunition.tracker import current_tracker

console = logging.getLogger(__name__)


def add_url_rule_wrapper(wrapped, instance, args, kwargs):
    """used to trace the views metric
    :param wrapped:
    :param instance:
    :return:
    """
    def parse_view_func(rule, endpoint=None, view_func=None, **options):
        return rule, endpoint, view_func, options

    rule, endpoint, view_func, options = parse_view_func(*args, **kwargs)

    def wrapper(wrapped, instance, args, kwargs):
        """
        :param wrapped:
        :param instance:
        :param args:
        :param kwargs:
        :return:
        """
        tracker = current_tracker()
        if not tracker:
            return wrapped(*args, **kwargs)

        tracker.set_tracker_name(callable_name(wrapped), 4)
        with FunctionTracker(tracker, callable_name(wrapped)):
            return wrapped(*args, **kwargs)

    return wrapped(rule, endpoint, FunctionWrapper(view_func, wrapper), **options)


def handle_exception_wrapper(wrapped, instance, args, kwargs):
    """used to trace the exception errors.
    :param wrapped:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    tracker = current_tracker()
    if not tracker:
        return wrapped(*args, **kwargs)

    # just record the exception info
    tracker.record_exception()

    return wrapped(*args, **kwargs)
