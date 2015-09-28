"""
    flaskext.restpoints
    ~~~~~~~~~~~~~~~~~~~
    An extension to Flask that adds some simple REST health check endpoints.
    :copyright: (c) 2015 by Justin Wilson <restpoints@minty.io>.
    :license: BSD, see LICENSE for more details.
"""

from flask_restpoints.handlers import ping, epoch, status


class RestPoints(object):
    """Adds/manages healh-check endpoints (ping, epoch, status).

    Numerous status jobs may be registered, and are invoked during a call to
    the `status` endpoint.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize a :class:`~flask.Flask` application for use with
        this extension.
        """
        self._jobs = []

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['restpoints'] = self
        app.restpoints_instance = self
        app.add_url_rule('/ping', 'ping', ping)
        app.add_url_rule('/epoch', 'epoch', epoch)
        app.add_url_rule('/status', 'status', status(self._jobs))

    def add_status_job(self, job_func, name=None, timeout=3):
        """Adds a job to be included during calls to the `/status` endpoint.

        :param job_func: the status function.
        :param name: the name used in the JSON response for the given status
                     function. The name of the function is the default.
        :param timeout: the time limit before the job status is set to
                        "timeout exceeded".
        """
        job_name = job_func.__name__ if name is None else name
        job = (job_name, timeout, job_func)
        self._jobs.append(job)

    def status_job(self, fn=None, name=None, timeout=3):
        """Decorator that invokes `add_status_job`.

        ::

            @app.status_job
            def postgresql():
                # query/ping postgres

            @app.status_job(name="Active Directory")
            def active_directory():
                # query active directory

            @app.status_job(timeout=5)
            def paypal():
                # query paypal, timeout after 5 seconds

        """
        if fn is None:
            def decorator(fn):
                self.add_status_job(fn, name, timeout)
            return decorator
        else:
            self.add_status_job(fn, name, timeout)
