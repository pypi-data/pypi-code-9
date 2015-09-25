"""
Contains the Flask extension for Stack Sentinel.

Installation is simple. The extension will register itself with the root logger.
app.config['STACKSENTINEL_ACCOUNT_TOKEN'] = 'YOUR ACCOUNT TOKEN'
app.config['STACKSENTINEL_PROJECT_TOKEN'] = 'YOUR PROJECT TOKEN'

>>> # app is a Flask app
>>> app.config['STACKSENTINEL_ACCOUNT_TOKEN'] = 'YOUR ACCOUNT TOKEN'
>>> app.config['STACKSENTINEL_PROJECT_TOKEN'] = 'YOUR PROJECT TOKEN'
>>> stacksentinel = flask.ext.stacksentinel.StackSentinelHandler(app)

By default, Stack Sentinel will install itself on the root log handler. To change that behavior,
pass a log handler you prefer to StackSentinelHandler:

>>> stacksentinel = flask.ext.stacksentinel.StackSentinelHandler(app, logger=app.logger)
"""

import logging
import sys
import flask

# Backwards compatability
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from StackSentinel import StackSentinelClient


class _StackSentinelLoggingHandler(logging.Handler):
    """
    Flask-specific log handler. Captures exception data, cookie data, etc.
    """
    def __init__(self, client, level=logging.ERROR):
        logging.Handler.__init__(self, level=level)

        self.client = client
        assert isinstance(self.client, StackSentinelClient)

    def emit(self, record):
        try:
            exc_info = sys.exc_info()
            if exc_info and exc_info != (None, None, None):
                state = {}
                if hasattr(flask, 'request'):
                    state['flask'] = {}
                    for attr in ('form', 'args', 'cookies', 'environ', 'method', 'path', 'script_root', 'headers',
                                 'url', 'base_url', 'url_root', 'is_xhr', 'blueprint', 'endpoint', 'json', 'module',
                                 'routing_exception', 'url_rule', 'view_args'):
                        try:
                            state['flask'][attr] = getattr(flask.request, attr, None)
                        except:
                            state['flask'][attr] = 'Error getting: %s'

                try:
                    state['flask']['headers'] = list(state['flask']['headers'])
                except:
                    pass

                logging.debug('Sending exception to Stack Sentinel: %r' % (exc_info,))
                response = self.client.handle_exception(exc_info, state=state)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class StackSentinelHandler(object):
    """
    Stack Sentinel Flask exception handler.
    """
    def __init__(self, app=None, logger=None):
        """
        :param app: Flask application
        :param logger: If specified, installs on this log handler. If unspecified, Python's root log handler is used.
        """
        self.app = app
        self.logger = logger or logging.root
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('STACKSENTINEL_ENDPOINT', "https://api.stacksentinel.com/api/v1/insert")
        app.config.setdefault('STACKSENTINEL_TAGS', "flask")
        app.config.setdefault('STACKSENTINEL_ENVIRONMENT', "unspecified")
        if "STACKSENTINEL_PROJECT_TOKEN" in app.config and 'STACKSENTINEL_ACCOUNT_TOKEN' in app.config:
            self.endpoint = app.config['STACKSENTINEL_ENDPOINT']
            self.tags = [x.strip() for x in app.config['STACKSENTINEL_TAGS'].split(',')]
            self.environment = app.config['STACKSENTINEL_ENVIRONMENT']
            self.account_token = app.config['STACKSENTINEL_ACCOUNT_TOKEN']
            self.project_token = app.config['STACKSENTINEL_PROJECT_TOKEN']

            self.client = StackSentinelClient(
                account_token=self.account_token,
                project_token=self.project_token,
                environment=self.environment,
                tags=self.tags,
                endpoint=self.endpoint
            )

            if 'stacksentinel' in app.extensions:
                app.logger.error('StackSentinel already installed as a Flask extension')
            else:
                app.extensions['stacksentinel'] = self

                self.log_handler = _StackSentinelLoggingHandler(self.client)
                self.log_handler.setLevel(logging.ERROR)
                self.logger.addHandler(self.log_handler)

        else:
            self.project_token = self.account_token = None
            app.logger.error('StackSentinel Flask Extension not configured: You must specify '
                'STACKSENTINEL_PROJECT_TOKEN and STACKSENTINEL_ACCOUNT_TOKEN in app.config')
