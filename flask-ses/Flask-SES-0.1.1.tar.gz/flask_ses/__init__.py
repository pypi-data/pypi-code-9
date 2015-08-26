import boto.ses

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class SESMailer(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.aws_region = self.app.config.get("AWS_REGION") or 'eu-west-1'
        self.aws_access_key_id = self.app.config.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = self.app.config.get("AWS_SECRET_ACCESS_KEY")
        self.ses_source_email = self.app.config.get("SES_SOURCE_EMAIL")

    def _connect(self):
        return boto.ses.connect_to_region(self.aws_region,
                                          aws_access_key_id=self.aws_access_key_id,
                                          aws_secret_access_key=self.aws_secret_access_key)

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'ses_connection'):
                ctx.ses_connection = self._connect()
            return ctx.ses_connection

    def send(self, subject, body, to_addresses, **kwargs):
        return self.connection.send_email(self.ses_source_email, subject, body, to_addresses, **kwargs)
