import sendwithus as sendwithus_api
from flask import current_app, _app_ctx_stack

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class Sendwithus:
    API_ENDPOINT_BASE = 'https://api.sendwithus.com/api/v1'

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if 'SENDWITHUS_API_KEY' not in app.config:
            raise RuntimeError('SENDWITHUS_API_KEY must be configured.')

    def url(self, endpoint):
        return urljoin(self.API_ENDPOINT_BASE, endpoint)

    @property
    def api_key(self):
        return current_app.config['SENDWITHUS_API_KEY']

    @property
    def api(self):
        ctx = _app_ctx_stack.top
        if not hasattr(ctx, 'sendwithus_api'):
            ctx.sendwithus_api = sendwithus_api.api(api_key=self.api_key)
        return ctx.sendwithus_api

    def __getattr__(self, name):
        return getattr(self.api, name)
