# coding=utf-8
# django-simple-blacklist 6/23/15 4:24 PM by mnach #
import importlib
import datetime
from django.core.exceptions import PermissionDenied
import logging
logger = logging.getLogger(__name__)
request_logger = logging.getLogger('django.request')

def blacklisting(func=None, log_requests=False):
    """
    This decorator implements blacklist logic by using rules identified by BlockRules model and
    also do request logic functionality if its needed.
    :param func decorated function(used only if you don't need send parameters to this decorator
    :param log_requests log all request to RequestLog model
    :return decorator
    """
    class Decorator(object):
        def __init__(self, func):
            self.func = func

        def __call__(self, request, *args, **kwargs):
            from blacklist import models
            self.request = request
            self.args = args
            self.kwargs = kwargs

            # 1. Block request if it matches at least one of the block rules
            for rule in models.BlockRules.objects.filter(enabled=True).defer('enabled', 'created', 'updated'):
                if rule.match(request):
                    return self._forbidden_action(rule)
            # 2. It not blocked and log_requests is True add RequestLog object to database
            if log_requests:
                models.RequestLog.objects.log_request(request)

            response = self.func(request, *args, **kwargs)
            return response

        def _forbidden_action(self, rule):
            from blacklist import models
            if models.permission_denied_callback:
                if isinstance(models.permission_denied_callback, str):
                    module, function = models.permission_denied_callback.rsplit('.', 1)
                    module = importlib.import_module(module)
                    if hasattr(module, function):
                        return getattr(module, function)(rule, self.request)
                elif callable(models.permission_denied_callback):
                    return models.permission_denied_callback(rule, self.request)
            raise PermissionDenied

    return Decorator if not func else Decorator(func)

def permission_denied_default(rule, request):
    request_logger.warning('Forbidden (Block rule #{0}): {1}'.format(rule.id, request.path),
        extra={
            'status_code': 403,
            'request': request
        }
    )
    raise PermissionDenied


def dt_json_serializer(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return str(obj)
    return None
