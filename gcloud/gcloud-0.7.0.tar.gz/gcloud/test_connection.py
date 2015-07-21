# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.connection import Connection
        return Connection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        conn = self._makeOne()
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        creds = object()
        conn = self._makeOne(creds)
        self.assertTrue(conn.credentials is creds)
        self.assertEqual(conn._http, None)

    def test_ctor_explicit_http(self):
        http = object()
        conn = self._makeOne(http=http)
        self.assertEqual(conn.credentials, None)
        self.assertTrue(conn.http is http)

    def test_http_w_existing(self):
        conn = self._makeOne()
        conn._http = http = object()
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        import httplib2
        conn = self._makeOne()
        self.assertTrue(isinstance(conn.http, httplib2.Http))

    def test_http_w_creds(self):
        import httplib2

        authorized = object()

        class Creds(object):
            def authorize(self, http):
                self._called_with = http
                return authorized
        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, httplib2.Http))

    def test_user_agent_format(self):
        from pkg_resources import get_distribution
        expected_ua = 'gcloud-python/{0}'.format(
            get_distribution('gcloud').version)
        conn = self._makeOne()
        self.assertEqual(conn.USER_AGENT, expected_ua)

    def _from_service_account_json_helper(self, **kwargs):
        from gcloud._testing import _Monkey
        from gcloud import connection

        KLASS = self._getTargetClass()
        CREDS = object()
        _CALLED = []

        def mock_creds(arg1):
            _CALLED.append((arg1,))
            return CREDS

        FOO = object()
        with _Monkey(connection, get_for_service_account_json=mock_creds):
            conn = KLASS.from_service_account_json(FOO, **kwargs)

        self.assertTrue(conn.credentials is CREDS)
        self.assertEqual(_CALLED, [(FOO,)])

    def test_from_service_account_json(self):
        self._from_service_account_json_helper()

    def test_from_service_account_json_fail(self):
        with self.assertRaises(TypeError):
            self._from_service_account_json_helper(credentials=None)

    def _from_service_account_p12_helper(self, **kwargs):
        from gcloud._testing import _Monkey
        from gcloud import connection

        KLASS = self._getTargetClass()
        CREDS = object()
        _CALLED = []

        def mock_creds(arg1, arg2):
            _CALLED.append((arg1, arg2))
            return CREDS

        FOO = object()
        BAR = object()
        with _Monkey(connection, get_for_service_account_p12=mock_creds):
            conn = KLASS.from_service_account_p12(FOO, BAR, **kwargs)

        self.assertTrue(conn.credentials is CREDS)
        self.assertEqual(_CALLED, [(FOO, BAR)])

    def test_from_service_account_p12(self):
        self._from_service_account_p12_helper()

    def test_from_service_account_p12_fail(self):
        with self.assertRaises(TypeError):
            self._from_service_account_p12_helper(credentials=None)

    def _from_environment_helper(self, **kwargs):
        from gcloud._testing import _Monkey
        from gcloud import connection

        KLASS = self._getTargetClass()
        CREDS = object()

        def mock_creds():
            return CREDS

        with _Monkey(connection, get_credentials=mock_creds):
            conn = KLASS.from_environment(**kwargs)

        self.assertTrue(conn.credentials is CREDS)

    def test_from_environment(self):
        self._from_environment_helper()

    def test_from_environment_fail(self):
        with self.assertRaises(TypeError):
            self._from_environment_helper(credentials=None)


class TestJSONConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.connection import JSONConnection
        return JSONConnection

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeMockOne(self, *args, **kw):
        class MockConnection(self._getTargetClass()):
            API_URL_TEMPLATE = '{api_base_url}/mock/{api_version}{path}'
            API_BASE_URL = 'http://mock'
            API_VERSION = 'vMOCK'
        return MockConnection(*args, **kw)

    def test_class_defaults(self):
        klass = self._getTargetClass()
        self.assertIsNone(klass.API_URL_TEMPLATE)
        self.assertIsNone(klass.API_BASE_URL)
        self.assertIsNone(klass.API_VERSION)

    def test_ctor_defaults(self):
        conn = self._makeOne()
        self.assertEqual(conn.credentials, None)

    def test_ctor_explicit(self):
        creds = object()
        conn = self._makeOne(creds)
        self.assertTrue(conn.credentials is creds)

    def test_http_w_existing(self):
        conn = self._makeOne()
        conn._http = http = object()
        self.assertTrue(conn.http is http)

    def test_http_wo_creds(self):
        import httplib2
        conn = self._makeOne()
        self.assertTrue(isinstance(conn.http, httplib2.Http))

    def test_http_w_creds(self):
        import httplib2
        authorized = object()

        class Creds(object):
            def authorize(self, http):
                self._called_with = http
                return authorized
        creds = Creds()
        conn = self._makeOne(creds)
        self.assertTrue(conn.http is authorized)
        self.assertTrue(isinstance(creds._called_with, httplib2.Http))

    def test_build_api_url_no_extra_query_params(self):
        conn = self._makeMockOne()
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(conn.build_api_url('/foo'), URI)

    def test_build_api_url_w_extra_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        conn = self._makeMockOne()
        uri = conn.build_api_url('/foo', {'bar': 'baz'})

        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate mock_template
        PATH = '/'.join([
            '',
            'mock',
            conn.API_VERSION,
            'foo',
        ])
        self.assertEqual(path, PATH)
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['bar'], 'baz')

    def test__make_request_no_data_no_content_type_no_headers(self):
        conn = self._makeOne()
        URI = 'http://example.com/test'
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
        headers, content = conn._make_request('GET', URI)
        self.assertEqual(headers['status'], '200')
        self.assertEqual(headers['content-type'], 'text/plain')
        self.assertEqual(content, b'')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test__make_request_w_data_no_extra_headers(self):
        conn = self._makeOne()
        URI = 'http://example.com/test'
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
        conn._make_request('GET', URI, {}, 'application/json')
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], {})
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'Content-Type': 'application/json',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test__make_request_w_extra_headers(self):
        conn = self._makeOne()
        URI = 'http://example.com/test'
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'',
        )
        conn._make_request('GET', URI, headers={'X-Foo': 'foo'})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'X-Foo': 'foo',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_defaults(self):
        PATH = '/path/required'
        conn = self._makeMockOne()
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            '%s%s' % (conn.API_VERSION, PATH),
        ])
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        self.assertEqual(conn.api_request('GET', PATH), {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_non_json_response(self):
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'CONTENT',
        )

        self.assertRaises(TypeError, conn.api_request, 'GET', '/')

    def test_api_request_wo_json_expected(self):
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '200', 'content-type': 'text/plain'},
            b'CONTENT',
        )
        self.assertEqual(conn.api_request('GET', '/', expect_json=False),
                         b'CONTENT')

    def test_api_request_w_query_params(self):
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        conn = self._makeMockOne()
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        self.assertEqual(conn.api_request('GET', '/', {'foo': 'bar'}), {})
        self.assertEqual(http._called_with['method'], 'GET')
        uri = http._called_with['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual('%s://%s' % (scheme, netloc), conn.API_BASE_URL)
        # Intended to emulate self.mock_template
        PATH = '/'.join([
            '',
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(path, PATH)
        parms = dict(parse_qsl(qs))
        self.assertEqual(parms['foo'], 'bar')
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_data(self):
        import json
        DATA = {'foo': 'bar'}
        DATAJ = json.dumps(DATA)
        conn = self._makeMockOne()
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            '',
        ])
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            b'{}',
        )
        self.assertEqual(conn.api_request('POST', '/', data=DATA), {})
        self.assertEqual(http._called_with['method'], 'POST')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], DATAJ)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': len(DATAJ),
            'Content-Type': 'application/json',
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)

    def test_api_request_w_404(self):
        from gcloud.exceptions import NotFound
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '404', 'content-type': 'text/plain'},
            b'{}'
        )
        self.assertRaises(NotFound, conn.api_request, 'GET', '/')

    def test_api_request_w_500(self):
        from gcloud.exceptions import InternalServerError
        conn = self._makeMockOne()
        conn._http = _Http(
            {'status': '500', 'content-type': 'text/plain'},
            b'{}',
        )
        self.assertRaises(InternalServerError, conn.api_request, 'GET', '/')

    def test_api_request_non_binary_response(self):
        conn = self._makeMockOne()
        http = conn._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            u'{}',
        )
        result = conn.api_request('GET', '/')
        # Intended to emulate self.mock_template
        URI = '/'.join([
            conn.API_BASE_URL,
            'mock',
            conn.API_VERSION,
            '',
        ])
        self.assertEqual(result, {})
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)
        self.assertEqual(http._called_with['body'], None)
        expected_headers = {
            'Accept-Encoding': 'gzip',
            'Content-Length': 0,
            'User-Agent': conn.USER_AGENT,
        }
        self.assertEqual(http._called_with['headers'], expected_headers)


class _Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
