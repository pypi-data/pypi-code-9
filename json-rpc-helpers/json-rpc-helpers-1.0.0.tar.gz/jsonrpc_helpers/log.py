import time
import inspect
import functools
from logging import getLogger, LoggerAdapter


class EnchantedLoggerAdapter(LoggerAdapter):
    """
    More useful logger adapter.
    Unlike logging.LoggerAdapter doesn't replace `extra` in kwargs
    with stored context, but merge these.
    """
    def process(self, msg, kwargs):
        kwargs.setdefault('extra', {})
        if self.extra:
            kwargs['extra'].update(self.extra)
        return msg, kwargs


class LoggedDecorator(object):
    def __init__(self, setup_logger, logger=None, logger_name=None,
                 adapter_cls=EnchantedLoggerAdapter, strip_self=False):
        """
        :param setup_logger: callable which accepts
            (f, logger, context, args, kwargs);
        :param logger: logger instance;
        :param logger_name: logger name (will be used if logger not specified);
        :param adapter_cls: class which will be used as LoggerAdapter;
        :param strip_self: if set to True - first argument will be removed.
        """
        self.setup_logger = setup_logger
        self.logger_adapter_cls = adapter_cls
        self.strip_self = strip_self
        if logger:
            self.logger = logger
        else:
            self.logger = getLogger(logger_name or __name__)

    def __call__(self, args_to_skip=None, response_mapper=None,
                 func_name=None, tag=None):
        """
        :param args_to_skip: names of arguments which must not be logged
            (you may need this if one of arguments is for example image);
        :param response_mapper: function to map response before log it
            (you may need this if your function returns very large response,
            for example list of 100 dicts);
        :param func_name: alias for method name in log,
            if not specified - method/function name will be used instead;
        :param tag: some arbitrary tag to mark this method/function.
        :return: function
        """
        if not args_to_skip:
            args_to_skip = []

        def decorator(f):
            fname = func_name or self._get_func_name(f)
            args_to_skip_mask = [
                a not in args_to_skip for a in inspect.getargspec(f).args]

            def wrapper(*args, **kwargs):

                start_time = time.time()
                context = {
                    'method': fname,
                    'tag': tag
                }
                logger = self.logger_adapter_cls(self.logger, context)
                self.setup_logger(f, logger, context, args, kwargs)
                filtered_args = self._filter_args(args, args_to_skip_mask)
                filtered_kwargs = self._filter_kwargs(kwargs, args_to_skip)

                logger.info('Method {} called'.format(fname), extra={
                    'params': filtered_args or filtered_kwargs
                })
                try:
                    result = f(*args, **kwargs)
                    result_to_log = result
                    if response_mapper:
                        result_to_log = response_mapper(result)
                    logger.info('OK', extra={
                        'response': result_to_log
                    })
                except Exception:
                    logger.exception('Internal error!')
                    raise
                finally:
                    # used to collect metrics by method names
                    logger.info('Execution time', extra={
                        'time': time.time() - start_time
                    })
                return result
            functools.update_wrapper(wrapper, f)
            return wrapper
        return decorator

    @staticmethod
    def _get_func_name(f):
        if hasattr(f, 'im_func'):
            f = getattr(f, 'im_func')
        return f.__name__

    def _filter_args(self, args, skip_mask):
        if self.strip_self:
            args = args[1:]
        if not skip_mask:
            return args
        return [
            arg if skip_mask[i] else 'skipped'
            for i, arg in enumerate(args)
        ]

    def _filter_kwargs(self, kwargs, args_to_skip):
        if self.strip_self:
            kwargs.pop('self', None)
        if not args_to_skip:
            return kwargs
        return {
            k: v for k, v in kwargs.items()
            if k not in args_to_skip
        }


def build_flask_decorator(**kwargs):
    """
    Flask uses thread local global variables to handle context passing.
    This builder assumes usage of `flask.g` variable to get context from
    and to set logger to.
    It assumes that context is stored as `g.context` attribute,
    and it sets logger to `g.logger` attribute.
    :param kwargs: kwargs to pass to LoggedDecorator constructor.
    :return: `LoggedDecorator`
    """
    from flask import g

    def setup_logger(f, logger, context, args, kwargs):
        context.update(g.get('context', {}))
        setattr(g, 'logger', logger)

    kwargs['setup_logger'] = setup_logger
    return LoggedDecorator(**kwargs)


def build_instance_method_decorator(**kwargs):
    """
    When instance used - context and logger can be stored on it.
    This builder assumes that context available as `self.context`
    and sets logger to `self.logger`.
    :param kwargs: kwargs to pass to LoggedDecorator constructor.
    :return: `LoggedDecorator`
    """
    def setup_logger(f, logger, context, args, kwargs):
        self = args[0]
        context.update(getattr(self, 'context', {}))
        self.logger = logger

    kwargs['setup_logger'] = setup_logger
    kwargs['strip_self'] = True
    return LoggedDecorator(**kwargs)


def response_to_len_mapper(response):
    """Return only length of the response."""
    return 'response length is {}'.format(len(response))


def empty_mapper(response):
    """Return only 'Ok' message."""
    return 'Ok'
