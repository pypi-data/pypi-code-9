# std lib
import logging
import socket
import time
import traceback

from collections import namedtuple

# django
from django.conf import settings

# datadog
from datadog import initialize, api, statsd

logger = logging.getLogger('datadog.DatadogMiddleware')

ExceptionReport = namedtuple(
    "ExceptionReport",
    ["title", "text", "aggregation_key", "tags", "alert_type"]
)


class DatadogMiddleware(object):
    DD_TIMING_ATTRIBUTE = '_dd_start_time'

    def __init__(self):
        self.app_name = settings.DATADOG_APP_NAME
        self.exception_metric = '{0}.errors.500'.format(self.app_name)
        self.timing_metric = '{0}.request_time'.format(self.app_name)
        self.exception_tags = [self.app_name, 'exception']

        self.api_key = settings.DATADOG_API_KEY
        self.app_key = settings.DATADOG_APP_KEY
        self.statsd_host = settings.DATADOG_HOST
        self.statsd_port = int(settings.DATADOG_PORT)
        self.host_name = socket.gethostname()
        self._setup_datadog()

    def _setup_datadog(self):
        initialize(
            api_key=self.api_key,
            app_key=self.app_key,
            statsd_host=self.statsd_host,
            statsd_port=self.statsd_port,
            host_name=self.host_name,
        )
        self.api = api
        self.statsd = statsd

    def process_request(self, request):
        setattr(request, self.DD_TIMING_ATTRIBUTE, time.time())
        return None

    def process_response(self, request, response):
        """ Submit timing metrics from the current request """
        if hasattr(request, self.DD_TIMING_ATTRIBUTE):
            # Calculate request time and submit to Datadog
            start_time = getattr(request, self.DD_TIMING_ATTRIBUTE)
            request_time = self.time_diff(start_time, time.time())
            tags = self._get_metric_tags(request)
            statsd.histogram(self.timing_metric, request_time, tags=tags)

        metric, tags = self.check_for_error(request, response)
        if metric:
            statsd.increment(metric, tags=tags)
        return response

    def process_exception(self, request, exception):
        """ Captures Django view exceptions as Datadog events """

        report = self.exception_report(request, exception)

        # Submit the exception to Datadog
        api.Event.create(
            title=report.title,
            text=report.text,
            tags=report.tags,
            aggregation_key=report.aggregation_key,
            alert_type=report.alert_type
        )

        # Increment our errors metric
        tags = self._get_metric_tags(request)
        statsd.increment(self.exception_metric, tags=tags)
        return None

    def check_for_error(self, request, response):
        if str(response.status_code).startswith("4"):
            metric = '{0}.errors.{1}'.format(self.app_name, response.status_code)
            return metric, self._get_metric_tags(request)
        return ["", ""]

    def exception_report(self, request, exception):
        # Get a formatted version of the traceback.
        exc = traceback.format_exc()

        title = 'Exception from {0}'.format(request.path)
        text = "Traceback:\n@@@\n{0}\n@@@" \
            .format(exc)

        aggregation_key = request.path
        alert_type = 'error'

        r = ExceptionReport(
            title,
            text,
            aggregation_key,
            self.exception_tags,
            alert_type,
        )
        return r

    def time_diff(self, start_time, end_time):
        return end_time - start_time

    def _get_metric_tags(self, request):
        return ['path:{0}'.format(request.path)]
