"""
    flaskext.tracy
    ~~~~~~~~~~~~~~~~~~~
    An extension for Flask for endpoint tracing.
"""


from logging import getLogger
from time import monotonic
from uuid import uuid1

from flask import request
from flask import abort
from flask import current_app


# function used to generate new transaction id's
new_id = uuid1
logger = getLogger("tracy")
trace_header_client = "Trace-Client"
trace_header_id = "Trace-ID"
trace_format = ("%(asctime)s"
                " %(status_code)s"
                " %(url)s"
                " %(client_ip)s"
                " %(trace_name)s"
                " %(trace_id)s"
                " %(trace_duration)f")


class Tracy(object):
    """Logs tracing information to the 'tracy' logger.

    Logs the time, url, client ip, trace header name, trace transaction id, and
    request duration as INFO.

    Configuration options:
        'TRACY_REQURE_CLIENT': Requires that a 'Trace-ID' header be present,
                               otherwise a 400 is returned.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Setup before_request, after_request handlers for tracing.
        """
        app.config.setdefault("TRACY_REQUIRE_CLIENT", False)
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['restpoints'] = self
        app.before_request(self._before)
        app.after_request(self._after)

    def _before(self):
        """Records the starting time of this reqeust.
        """
        request._tracy_start_time = monotonic()
        client = request.headers.get(trace_header_client, None)
        require_client = current_app.config.get("TRACY_REQUIRE_CLIENT", False)
        if client is None and require_client:
            abort(400, "Missing %s header" % trace_header_client)

        request._tracy_client = client
        request._tracy_id = request.headers.get(trace_header_id, new_id())

    def _after(self, response):
        """Calculates the request duration, and adds a transaction
        ID to the header.
        """
        duration = None
        if getattr(request, '_tracy_start_time', None):
            duration = monotonic() - request._tracy_start_time

        # Add Trace_ID header.
        trace_id = None
        if getattr(request, '_tracy_id', None):
            trace_id = request._tracy_id
            response.headers[trace_header_id] = trace_id

        # Get the invoking client.
        trace_client = None
        if getattr(request, '_tracy_client', None):
            trace_client = request._tracy_client

        # Extra log kwargs.
        d = {'status_code': response.status_code,
             'url': request.base_url,
             'client_ip': request.remote_addr,
             'trace_name': trace_client,
             'trace_id': trace_id,
             'trace_duration': duration}
        logger.info(None, extra=d)
        return response
