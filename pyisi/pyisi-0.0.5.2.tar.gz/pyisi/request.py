import requests
import exceptions
from endpoint import endpoint
import json


class APIRequest:
    def __init__(self, base_url, verify_ssl):
        self.ssl_verify = verify_ssl
        self.base_url = base_url
        self.s = None

    exception_map = {
        "AEC_NOT_FOUND": exceptions.AEC_NOT_FOUND,
        "AEC_UNAUTHORIZED": exceptions.AEC_UNAUTHORIZED,
        "AEC_FORBIDDEN": exceptions.AEC_FORBIDDEN,
        "AEC_SYSTEM_INTERNAL_ERROR": exceptions.AEC_SYSTEM_INTERNAL_ERROR
    }

    def make_request(self, req_method, req_uri, **kwargs):
        r = req_method(url=self.base_url + req_uri, verify=self.ssl_verify, **kwargs)
        self.handle_response(r)
        return r

    def handle_response(self, resp):
        if resp.status_code < 300:
            return
        try:
            j = json.loads(resp.text)['errors']
        except (KeyError, ValueError):
            raise exceptions.AEC_ERROR("Error: {:d} unknown reason".format(resp.status_code))
        for e in j:
            c, m = e.get('code', None), e['message']
            exc = self.exception_map.get(c, exceptions.AEC_ERROR)
            raise exc(m)

    def create_session(self, username, password, services):
        """
        Get a session from the Isilon API
        returns (session, response)
        Where response is the response from the authenticaion request
        :return requests.Session
        :return requests.Response
        """

        s = requests.Session()
        r = s.post(url=self.base_url + endpoint('session'),
                   headers={"Content-Type": "application/json"},
                   data=json.dumps({"username": username,
                                    "password": password,
                                    "services": services}),
                   verify=self.ssl_verify)

        self.handle_response(r)
        self.s = s

    def get(self, uri, **kwargs):
        return self.make_request(self.s.get, uri, **kwargs)

    def put(self, uri, **kwargs):
        return self.make_request(self.s.put, uri, **kwargs)

    def post(self, uri, **kwargs):
        return self.make_request(self.s.post, uri, **kwargs)

    def head(self, uri, **kwargs):
        return self.make_request(self.s.head, uri, **kwargs)

    def delete(self, uri, **kwargs):
        return self.make_request(self.s.delete, uri, **kwargs)
