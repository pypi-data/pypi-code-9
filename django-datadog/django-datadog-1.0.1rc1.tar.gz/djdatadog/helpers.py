import socket
from functools import partial

from datadog import statsd

# django
from django.conf import settings

# datadog
from datadog import initialize, api, statsd


class Stats(object):
    """
    Base object that establishes a DataDog statsd and api connection
    from Django settings.

    Enforces that calls to statd metrics include the DATADOG_APP_NAME as a tag.

    Exposes relevant `<Statsd methods>`_

    .. _Statsd methods : http://datadogpy.readthedocs.org/en/latest/#datadog-dogstatsd-module
    """
    def __init__(self):
        self.app_name = settings.DATADOG_APP_NAME
        self.api_key = settings.DATADOG_API_KEY
        self.app_key = settings.DATADOG_APP_KEY
        self.statsd_host = settings.DATADOG_HOST
        try:
            self.statsd_port = int(settings.DATADOG_PORT)
        except AttributeError:
            self.statsd_port = 8125
        self.host_name = socket.gethostname()
        self._setup_datadog()
        self.ALLOWED_METHODS = [
            'decrement',
            'event',
            'gauge',
            'histogram',
            'increment',
            'service_check',
            'set',
            'timed',
            'timing',
        ]

    def _setup_datadog(self):
        initialize(
            api_key=self.api_key,
            app_key=self.app_key,
            statsd_host=self.statsd_host,
            statsd_port=self.statsd_port,
            host_name=self.host_name,
        )
        self.api, self.statsd = api, statsd
        return self.api, self.statsd

    def call_with_standards(self, method, *args, **kwargs):
        tags = self.standardize_tags(kwargs.get('tags'))
        kwargs['tags'] = tags
        return method(*args, **kwargs)

    def standardize_tags(self, tags):
        if tags is None:
            tags = [self.app_name, ]
        elif self.app_name not in tags:
            tags.append(self.app_name)

        return tags

    def _find_statsd_method(self, name):
        if name in self.ALLOWED_METHODS:
            method = getattr(self.statsd, name)

            def _wrapped_statsd_method(*args, **kwargs):
                return self.call_with_standards(method, *args, **kwargs)
            return _wrapped_statsd_method
        else:
            raise AttributeError(' %s has no method named "%s" ' % (type(self).__name__, name))

    def __getattr__(self, name):
        try:
            return self._find_statsd_method(name)
        except AttributeError:
            return object.__getattribute__(self, name)
