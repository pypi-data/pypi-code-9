import json
from functools import partial
import unittest
from mock import patch, MagicMock

from ambition.rest import ApiException


class RestClientObjectTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('ambition.rest.RESTClientObject.agent')
    def test_content_types(self, rest_agent):
        """
        Verify that the rest client supports the extended set of content types
        """
        request_mock = MagicMock(return_value=MagicMock(status=200, data=b''))
        rest_agent.return_value.request = request_mock
        from ..rest import RESTClient
        test_headers = {
            'Content-Type': 'application/vnd.ms-excel'
        }
        RESTClient.POST('fake_url', headers=test_headers)
        request_mock.assert_called_with(
            'POST', 'fake_url', body=None, headers=test_headers)

    @patch('ambition.rest.RESTClientObject.agent')
    def test_get_query_params(self, rest_agent):
        """
        Verify that the rest client passes along query params to transport
        """
        request_mock = MagicMock(return_value=MagicMock(status=200, data=b''))
        rest_agent.return_value.request = request_mock
        from ..rest import RESTClient
        query_params = {'foo': 'bar'}
        RESTClient.GET('fake_url', query_params=query_params)
        request_kwargs = {
            'fields': query_params,
            'headers': {
                'Content-Type': 'application/json',
            },
        }
        request_mock.assert_called_with('GET', 'fake_url', **request_kwargs)

    @patch('ambition.rest.RESTClientObject.agent')
    def test_form_params(self, rest_agent):
        """
        Verify that the rest client passes along form params to transport
        """
        request_mock = MagicMock(return_value=MagicMock(status=200, data=b''))
        rest_agent.return_value.request = request_mock
        from ..rest import RESTClient
        post_params = {'foo': 'bar'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        RESTClient.POST('fake_url', post_params=post_params, headers=headers)
        request_kwargs = {
            'fields': post_params,
            'headers': headers,
            'encode_multipart': False,
        }
        request_mock.assert_called_with('POST', 'fake_url', **request_kwargs)

    def test_agent_selector(self):
        """
        Verifies that the pool with the right scheme is returned
        """
        from ..rest import RESTClientObject
        client = RESTClientObject()
        http_url = 'http://www.google.com'
        self.assertIsNone(client.agent(http_url).connection_pool_kw.get('cert_reqs'))
        https_url = 'https://www.google.com'
        self.assertIsNotNone(client.agent(https_url).connection_pool_kw.get('cert_reqs'))

    @patch('ambition.rest.RESTClientObject.request')
    def test_put(self, request_mock):
        """
        Verifies that put correctly wraps the request method
        """
        from ..rest import RESTClient
        client = RESTClient()
        url = 'http://www.example.com'
        client.PUT(url)
        request_mock.assert_called_with(
            'PUT', url, headers=None, post_params=None, body=None)

    @patch('ambition.rest.RESTClientObject.request')
    def test_patch(self, request_mock):
        """
        Verifies that patch correctly wraps the request method
        """
        from ..rest import RESTClientObject
        client = RESTClientObject()
        url = 'http://www.example.com'
        client.PATCH(url)
        request_mock.assert_called_with(
            'PATCH', url, headers=None, post_params=None, body=None)

    @patch('ambition.rest.RESTClientObject.request')
    def test_head(self, request_mock):
        """
        Verifies that head correctly wraps the request method
        """
        from ..rest import RESTClient
        client = RESTClient()
        url = 'http://www.example.com'
        client.HEAD(url)
        request_mock.assert_called_with(
            'HEAD', url, headers=None, query_params=None)

    @patch('ambition.rest.RESTClientObject.request')
    def test_delete(self, request_mock):
        """
        Verifies that delete correctly wraps the request method
        """
        from ..rest import RESTClientObject
        client = RESTClientObject()
        url = 'http://www.example.com'
        client.DELETE(url)
        request_mock.assert_called_with(
            'DELETE', url, headers=None, query_params=None)

    def test_error_response(self):
        """
        Verifies that API errors result in well constructed objects
        """
        from ..rest import ApiException
        response = {
            'status': 500,
            'reason': 'just because',
            'data': b'not}{json',
            'headers': []
        }
        exception = ApiException(MagicMock(**response))
        self.assertEqual(type(str(exception)), str)

    @patch('ambition.rest.RESTClientObject.PATCH')
    def test_rest_client_patch(self, patch):
        """
        Verifies that the patch method invokes the corresponding method on the
        rest client object
        """
        from ..rest import RESTClient
        client = RESTClient()
        client.PATCH()
        patch.assert_called_with()

    @patch('ambition.rest.RESTClientObject.DELETE')
    def test_rest_client_delete(self, delete):
        """
        Verifies that the delete method invokes the corresponding method on the
        rest client object
        """
        from ..rest import RESTClient
        client = RESTClient()
        client.DELETE()
        delete.assert_called_with()

    @patch('ambition.rest.RESTClientObject.agent')
    def test_multipart_boundary_allowed(self, rest_agent):
        """
        Verifies that the API client doesn't override urllib's definition of
        the multipart form boundary
        """
        request_mock = MagicMock(return_value=MagicMock(status=200, data=b''))
        rest_agent.return_value.request = request_mock
        from ..rest import RESTClientObject
        client = RESTClientObject()
        post_params = {'foo': 'bar'}
        headers = {'Content-Type': 'multipart/form-data'}
        client.request(
            'POST', 'http://example.com/', post_params=post_params,
            headers=headers)
        request_mock.assert_called_with(
            'POST', 'http://example.com/', fields=post_params,
            encode_multipart=True, headers={}
        )

    @patch('ambition.rest.RESTClientObject.agent')
    def test_query_params_are_added_to_url(self, rest_agent):
        """
        Verify that query params are appended to the url correctly
        """
        request_mock = MagicMock(return_value=MagicMock(status=200, data=b''))
        rest_agent.return_value.request = request_mock
        from ..rest import RESTClientObject
        client = RESTClientObject()
        query_params = {'foo': 'bar'}
        client.request(
            'POST', 'http://example.com/', query_params=query_params,
            body=query_params
        )
        expected_headers = {'Content-Type': 'application/json'}
        request_mock.assert_called_with(
            'POST', 'http://example.com/?foo=bar', body=json.dumps(query_params),
            headers=expected_headers
        )

    @patch('ambition.rest.RESTClientObject.agent')
    def test_api_error_raises_exception(self, rest_agent):
        """
        Verify that an api error response will raise an exception
        """
        request_mock = MagicMock(return_value=MagicMock(status=500, data=b''))
        rest_agent.return_value.request = request_mock
        from ..rest import RESTClientObject
        client = RESTClientObject()
        query_params = {'foo': 'bar'}
        request = partial(
            client.request, 'POST', 'http://example.com/',
            query_params=query_params, body='')
        self.assertRaises(ApiException, request)
