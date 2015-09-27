import itsdangerous
from seamless.signer import Signer


class SeamlessMiddleware(object):
    def __init__(self, app, secret, max_age=60, realm=''):
        self.app = app
        self.signer = Signer(secret)
        self.max_age = max_age
        self.realm = realm

    def _not_authorized(self, environ, start_response, error=''):
        start_response('401 Not Authorized', [
            ('WWW-Authenticate', 'seamless realm="{}"'.format(self.realm)),
        ])
        return error

    def __call__(self, environ, start_response):
        auth = environ.get('HTTP_AUTHORIZATION', '')
        if not auth.startswith('seamless '):
            print auth
            print environ
            return self._not_authorized(environ, start_response, 'bad authorization header format\n')
        token = auth.split(' ', 1)[1]
        try:
            user = self.signer.unsign(token, max_age=self.max_age)
        except itsdangerous.SignatureExpired as e:
            return self._not_authorized(environ, start_response, 'token expired\n')
        except itsdangerous.BadData as e:
            print e
            return self._not_authorized(environ, start_response, 'invalid token\n')
        environ['HTTP_X_SEAMLESS_USER'] = user
        return self.app(environ, start_response)
