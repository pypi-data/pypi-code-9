import hashlib
from collections import OrderedDict
import json

import requests

from okapi.settings import settings
from okapi.core.utils import format_json


class Request(object):
    def __init__(self, method, url, headers, payload, tests):
        """
        :type method: str
        :type url: str
        :type headers: dict[str, str]
        :type payload: str
        :type tests: list[okapi.core.tests.Test]
        """
        self.method = method.lower()
        self.url = url
        self.headers = headers
        self.payload = payload.strip()
        self.tests = tests
        self.status = True
        self.cached = False
        self.log = ''

        self._response = None
        self._payload = None
        self._guid = None

        if self.guid in settings.cache.get():
            self.cached = True
            self._response = settings.cache.get()[self.guid]

    @property
    def absolute_url(self):
        """
        Absolute url for request.
        """
        return settings.url + self.url

    @property
    def guid(self):
        """
        Generates GUID for request based on method, url, payload,
        headers and tests. GUID is used for this cases:

        - as ID in HTML elements to use it in links
        - as key in cache dictionary

        :return: generated guid
        :rtype: str
        """
        if not self._guid:
            data = [
                self.method, self.url, self.payload,
                str(self.get_all_headers()), str(self.tests)
            ]

            h = hashlib.md5()
            h.update(','.join(data).encode('utf-8'))
            self._guid = h.hexdigest()

        return self._guid

    @property
    def response(self):
        """
        Create HTTP request and return response.

        :return: HTTP response
        :rtype: requests.Response
        """
        if self._response is None:
            self._response = requests.request(
                self.method, 
                self.absolute_url,
                data=self.payload, 
                headers=self.get_all_headers(),
                allow_redirects=False,
            )

        try:
            self._response.body = format_json(self._response.json())
        except ValueError:
            self._response.body = self._response.text

        return self._response

    def get_headers(self):
        """
        Request headers + global headers. Ordered by key.
        """
        headers = dict(settings.headers.visible)
        headers.update(self.headers)
        return OrderedDict(sorted(headers.items()))

    def get_all_headers(self):
        """
        Request headers + global headers + CLI headers. Ordered by key.
        """
        headers = self.get_headers()
        headers.update(settings.headers.hidden)
        return OrderedDict(sorted(headers.items()))

    def run_tests(self):
        """
        Run tests and log results.

        :return: Test results.
        :rtype: bool
        """
        if not self.tests:
            self.log += '\t\t[WARN] Request has no tests\n'
            return False

        variables = self.get_test_variables()

        for test in self.tests:
            if not test.run(variables):
                self.status = False
            self.log += test.log

        if not self.status:
            return False

        settings.cache.get()[self.guid] = self._response
        return True

    def get_test_variables(self):
        """
        Converts response variables to dictionary used in test assertion
        and pdb debugger.

        :return: Dictionary with variables.
        :rtype: dict
        """

        variables = {}

        for x in dir(self.response):
            if x.startswith('_'):
                continue
            variables[x] = getattr(self.response, x)

        return variables


class PrototypeRequest(Request):
    def __init__(self, *args, **kwargs):
        super(PrototypeRequest, self).__init__(*args, **kwargs)
        self.cached = False

    @property
    def response(self):
        return DummyResponse()

    def run_tests(self):
        return True


class DummyResponse(object):
    def __init__(self, **kwargs):
        self.content = ''
        self.headers = {}
        self.status_code = 200

        self.__dict__.update(kwargs)

    def json(self):
        return json.loads(self.content)

    @property
    def text(self):
        return self.content
