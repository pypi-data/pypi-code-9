""" Test utilities. """

import base64
import json

from requests_testadapter import TestAdapter, TestSession


class RecordingAdapter(TestAdapter):
    """ Record the request that was handled by the adapter.
    """
    request = None
    expected_auth_headers = None

    def set_expected_auth(self, username, password):
        auth_data = base64.b64encode('%s:%s' % (username, password))
        self.expected_auth_headers = {
            "Authorization": u'Basic %s' % auth_data,
        }

    def send(self, request, *args, **kw):
        self.request = request
        return super(RecordingAdapter, self).send(request, *args, **kw)


class ApiHelper(object):

    def __init__(self, test_case, api_url='http://example.com/api/v1'):
        self.test_case = test_case
        self.api_url = api_url
        self.session = TestSession()
        self._api_patches = []

    def tearDown(self):
        for obj, name, orig_api in reversed(self._api_patches):
            setattr(obj, name, orig_api)

    def patch_api(self, obj, name):
        def patched_api(*args, **kw):
            kw['session'] = self.session
            kw['api_url'] = self.api_url
            return orig_api(*args, **kw)
        orig_api = getattr(obj, name)
        self._api_patches.append((obj, name, orig_api))
        setattr(obj, name, patched_api)

    def check_response(self, adapter, method, data=None, headers=None):
        request = adapter.request
        auth_headers = adapter.expected_auth_headers
        self.test_case.assertEqual(request.method, method)
        if data is not None:
            self.test_case.assertEqual(json.loads(request.body), data)
        if headers is not None:
            for key, value in headers.items():
                self.test_case.assertEqual(request.headers[key], value)
        if auth_headers is not None:
            for key, value in auth_headers.items():
                self.test_case.assertEqual(request.headers[key], value)

    def add_send(self, account_key, conv_key, conv_token, data=None):
        adapter = RecordingAdapter(json.dumps(data))
        adapter.set_expected_auth(account_key, conv_token)
        self.session.mount(
            "%s/%s/messages.json" % (self.api_url, conv_key),
            adapter)
        return adapter
