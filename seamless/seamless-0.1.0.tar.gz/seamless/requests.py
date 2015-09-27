from __future__ import absolute_import

import re
import requests
import seamless


realm_re = re.compile('realm="[^"]+"')


class SeamlessAuth(requests.auth.AuthBase):
    def __init__(self, realm=None, retry_expired=True):
        self.realm = realm
        self.retry_expired = retry_expired
        self.token = None

    def get_authorization_header(self, refresh=False):
        if refresh or not self.token:
            self.token = seamless.get_token(self.realm)
        return 'seamless {}'.format(self.token)

    def __call__(self, r):
        r.headers['Authorization'] = self.get_authorization_header()
        if self.retry_expired:
            r.register_hook('response', self.handle_response)
        return r

    def handle_response(self, r, **kwargs):
        if r.status_code == 401:
            header = r.headers.get('WWW-Authenticate', '')
            if not header.startswith('seamless '):
                return r
            if 'expired' in r.text:
                r.content
                r.close()
                retry = r.request.copy()
                retry.headers['Authorization'] = self.get_authorization_header(refresh=True)
                retry_response = r.connection.send(retry, **kwargs)
                retry_response.history.append(r)
                retry_response.request = retry
                return retry_response
        return r
