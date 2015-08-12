# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Interceptor for Flask framework.

"""

import sys

from appdynamics.agent.interceptor.frameworks.wsgi import WSGIInterceptor


class FlaskInterceptor(WSGIInterceptor):
    def _handle_exception(self, handle_exception, flask, e):
        with self.log_exceptions():
            bt = self.bt
            if bt:
                bt.add_exception(*sys.exc_info())

        return handle_exception(flask, e)


def intercept_flask(agent, mod):
    interceptor = FlaskInterceptor(agent, mod.Flask)
    interceptor.attach('wsgi_app', patched_method_name='application_callable')
    interceptor.attach('handle_exception')
