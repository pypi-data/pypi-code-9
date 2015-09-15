import requests
import exceptions
from endpoint import endpoint
import json
import time


class APIRequest:
    def __init__(self, base_url, username, password, services=(), verify_ssl=False):
        self.ssl_verify = verify_ssl
        self.base_url = base_url

        self.s = requests.session()
        self.username = username
        self.password = password
        self.services = services
        self.session_expires = None
        self._create_session()

    api_exception_map = {
        "AEC_NOT_FOUND": exceptions.AEC_NOT_FOUND,
        "AEC_UNAUTHORIZED": exceptions.AEC_UNAUTHORIZED,
        "AEC_FORBIDDEN": exceptions.AEC_FORBIDDEN,
        "AEC_SYSTEM_INTERNAL_ERROR": exceptions.AEC_SYSTEM_INTERNAL_ERROR
    }

    http_exception_map = {
        401: exceptions.AEC_UNAUTHORIZED,
        500: exceptions.AEC_SYSTEM_INTERNAL_ERROR,
        403: exceptions.AEC_FORBIDDEN,
        404: exceptions.AEC_NOT_FOUND
    }

    def _session_keepalive(self):
        if self.session_expires is None:
            self._create_session()
        elif self.session_expires >= time.time():
            self._create_session()

    def _make_request(self, req_method, req_uri, **kwargs):
        self._session_keepalive()
        try:
            r = req_method(url=self.base_url + req_uri, verify=self.ssl_verify, **kwargs)
        except requests.ConnectionError:
            raise exceptions.AEC_CONNECTION_ERROR
        self._handle_response(r)
        return r

    def _handle_response(self, resp):
        if resp.status_code < 300:
            return
        try:
            j = json.loads(resp.text)['errors']
        except (KeyError, ValueError):
            # If we cant decode the response as JSON then raise a more generic error
            exc = self.http_exception_map.get(resp.status_code, exceptions.AEC_ERROR)
            raise exc(str(resp.status_code))
        for e in j:
            c, m = e.get('code', None), e.get('message', 'Unknown error')
            exc = self.api_exception_map.get(c, exceptions.AEC_ERROR)
            raise exc(m)

    def _create_session(self):
        """
        Make a POST request to the session endpoint to retrieve authentication cookie
        """
        try:
            r = self.s.post(url=self.base_url + endpoint('session'),
                            headers={"Content-Type": "application/json"},
                            data=json.dumps({"username": self.username,
                                             "password": self.password,
                                             "services": self.services}),
                            verify=self.ssl_verify)
        except requests.ConnectionError:
            raise exceptions.AEC_CONNECTION_ERROR
        self._handle_response(r)

        timeout = r.json().get('timeout_inactive')
        if timeout is not None:
            self.session_expires = time.time() + timeout

    def get(self, uri, **kwargs):
        return self._make_request(self.s.get, uri, **kwargs)

    def put(self, uri, **kwargs):
        return self._make_request(self.s.put, uri, **kwargs)

    def post(self, uri, **kwargs):
        return self._make_request(self.s.post, uri, **kwargs)

    def head(self, uri, **kwargs):
        return self._make_request(self.s.head, uri, **kwargs)

    def delete(self, uri, **kwargs):
        return self._make_request(self.s.delete, uri, **kwargs)
