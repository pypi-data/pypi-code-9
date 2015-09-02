import os
from functools import partial
import datetime
import unittest

from mock import patch

from ..api_client import ApiClient
from ..configuration import ApiConfiguration
from .. import models

test_dict = {
    'name': 'Test Name',
    'display_name': 'Test Display Name',
    'data_format': 'Test Format',
}


class TestModel(object):
    def __init__(self):
        self.swagger_types = {
            'display_name': 'str',
            'name': 'str',
            'data_format': 'str',
        }
        self.attribute_map = {
            'display_name': 'display_name',
            'name': 'name',
            'data_format': 'data_format',
        }
        self.display_name = None
        self.name = None
        self.data_format = None
        self.some_other_attribute = None


class ApiClientTest(unittest.TestCase):
    def setUp(self):
        host = 'http://example.com'
        api_key = 'keyboardcat'
        configuration = ApiConfiguration(host, api_key)
        self.client = ApiClient(configuration=configuration)
        self.base_expected_headers = {
            'Authorization': 'Token keyboardcat',
            'User-Agent': 'Python-Swagger',
        }

    def test_sanitization_for_serialization(self):
        """
        Verify that data are normalized
        """
        model = TestModel()
        for key in test_dict.keys():
            setattr(model, key, test_dict[key])
        sanitized_model = self.client.sanitize_for_serialization(model)
        self.assertEqual(sanitized_model, test_dict)

    def test_deserialization(self):
        obj = [{'foo': 'bar'}, {'baz': 'qux'}]
        deserialized = self.client.deserialize(obj, 'list[dict]')
        self.assertEqual(obj, deserialized)
        obj = 1
        deserialized = self.client.deserialize(obj, 'dict')
        self.assertEqual(deserialized, obj)
        # deserialize model from dict that doesn't have all model attributes
        models.TestModel = TestModel
        obj = {'name': 'some name'}
        deserialized = self.client.deserialize(obj, 'TestModel')
        self.assertIsNone(deserialized.display_name)
        self.assertIsNone(deserialized.data_format)
        # deserialize datetimes
        now = datetime.datetime.now()
        deserialized = self.client.deserialize(now.isoformat(), 'datetime')
        self.assertEqual(now, deserialized)

    @patch('ambition.api_client.RESTClient.GET')
    @patch('ambition.api_client.RESTClient.HEAD')
    @patch('ambition.api_client.RESTClient.POST')
    @patch('ambition.api_client.RESTClient.PATCH')
    @patch('ambition.api_client.RESTClient.PUT')
    @patch('ambition.api_client.RESTClient.DELETE')
    def test_request_method(self, delete, put, patch, post, head, get):
        """
        Verify that the correct client method is called with the right kwargs
        """
        query_params = {'query': 'query_param'}
        post_params = {'post': 'post_param'}
        body = 'body'
        self.client.request(
            'GET', 'some_url', query_params=query_params, body=body,
            post_params=post_params, headers=self.base_expected_headers)
        self.client.request(
            'HEAD', 'some_url', query_params=query_params, body=body,
            post_params=post_params, headers=self.base_expected_headers)
        self.client.request(
            'POST', 'some_url', query_params=query_params, body=body,
            post_params=post_params, headers=self.base_expected_headers)
        self.client.request(
            'PATCH', 'some_url', query_params=query_params, body=body,
            post_params=post_params, headers=self.base_expected_headers)
        self.client.request(
            'PUT', 'some_url', query_params=query_params, body=body,
            post_params=post_params, headers=self.base_expected_headers)
        self.client.request(
            'DELETE', 'some_url', query_params=query_params, body=body,
            post_params=post_params, headers=self.base_expected_headers)
        delete.assert_called_with(
            'some_url', query_params=query_params,
            headers=self.base_expected_headers)
        put.assert_called_with(
            'some_url', post_params=post_params, body=body,
            headers=self.base_expected_headers)
        patch.assert_called_with(
            'some_url', post_params=post_params, body=body,
            headers=self.base_expected_headers)
        post.assert_called_with(
            'some_url', post_params=post_params, body=body,
            headers=self.base_expected_headers)
        head.assert_called_with(
            'some_url', query_params=query_params,
            headers=self.base_expected_headers)
        get.assert_called_with(
            'some_url', query_params=query_params,
            headers=self.base_expected_headers)
        n = ['NOT_A_METHOD', 'some_url']
        self.assertRaises(ValueError, partial(self.client.request, *n))

    def test_files(self):
        """
        Verifies that the files are included in post params
        """
        file_path = os.path.abspath(__file__)
        files = {
            'this_file': file_path
        }
        post_params = self.client.prepare_post_parameters(files=files)
        self.assertIn('this_file', post_params)

    def test_select_accepts(self):
        """
        Verifies that the accept header is correctly selected (or not)
        from a list
        """
        self.assertIsNone(self.client.select_header_accept([]))
        accepts = ['application/vnd.ms-excel', 'application/json']
        self.assertEqual('application/json', self.client.select_header_accept(accepts))
        accepts = ['application/vnd.ms-excel', 'text/csv']
        self.assertEqual(', '.join(accepts), self.client.select_header_accept(accepts))

    def test_select_content_type(self):
        """
        Verifies that the content type header is correctly selected
        """
        self.assertEqual('application/json', self.client.select_header_content_type([]))
        content_types = ['application/vnd.ms-excel', 'application/json']
        self.assertEqual('application/json', self.client.select_header_content_type(content_types))
        content_types = ['application/vnd.ms-excel', 'text/csv']
        self.assertEqual('application/vnd.ms-excel', self.client.select_header_content_type(content_types))

    @patch('ambition.api_client.models')
    @patch('ambition.api_client.RESTClient.GET')
    def test_deserialization_single_model(self, rest_get, models):
        """
        Verify that api responses are cast as the right model type
        """
        rest_get.return_value = test_dict
        models.TestModel = TestModel
        model = self.client.call_api('/fake', 'GET', response='TestModel')
        self.assertIsInstance(model, TestModel)
        self.assertEqual(model.display_name, test_dict.get('display_name'))
        self.assertEqual(model.name, test_dict.get('name'))
        self.assertEqual(model.data_format, test_dict.get('data_format'))

    @patch('ambition.api_client.models')
    @patch('ambition.api_client.RESTClient.GET')
    def test_deserialization_multiple_models(self, rest_get, models):
        """
        Verify that list api responses are model iterators
        """
        serialized_response = [test_dict, test_dict]
        rest_get.return_value = serialized_response
        models.TestModel = TestModel
        response = self.client.call_api('/fake', 'GET', response='TestModel')
        self.assertEqual(len(list(response)), 2)
        for model in response:
            self.assertIsInstance(model, TestModel)

    @patch('ambition.api_client.ApiClient.request')
    def test_path_params(self, request_mock):
        """
        Verify that path parameters are constructed properly
        """
        path_params = {
            'foo': 'f',
            'bar': 'b',
        }
        self.client.call_api('/{foo}/{bar}/', 'GET', path_params=path_params)
        expected_url = 'http://example.com/f/b/'
        request_mock.assert_called_with(
            'GET', expected_url, body=None,
            headers=self.base_expected_headers,
            post_params=None, query_params=None)

    @patch('ambition.api_client.ApiClient.request')
    def test_query_params(self, request_mock):
        """
        Verify that query parameters are normalized
        """
        today = datetime.datetime.now().date()
        query_params = {
            'today': today,
            'users': ['Marty McFly', 'H. G. Wells'],
            'none_thing': None,
        }
        self.client.call_api('/stuff/', 'GET', query_params=query_params)
        expected_query_params = {
            'today': datetime.datetime.now().date().isoformat(),
            'users': 'Marty McFly,H. G. Wells',
            'none_thing': 'None',
        }
        request_mock.assert_called_with(
            'GET', 'http://example.com/stuff/', body=None,
            headers=self.base_expected_headers,
            post_params=None, query_params=expected_query_params)

    @patch('ambition.api_client.ApiClient.request')
    def test_post_params(self, request_mock):
        """
        Verify that post parameters are normalized
        """
        today = datetime.datetime.now().date()
        post_params = {
            'today': today,
        }
        self.client.call_api('/stuff/', 'POST', post_params=post_params)
        expected_post_params = {
            'today': datetime.datetime.now().date().isoformat()
        }
        request_mock.assert_called_with(
            'POST', 'http://example.com/stuff/', body=None,
            headers=self.base_expected_headers,
            post_params=expected_post_params, query_params=None)

    @patch('ambition.api_client.ApiClient.request')
    def test_body_normalization(self, request_mock):
        """
        Verify that body is normalized
        """
        today = datetime.datetime.now().date()
        body = today
        self.client.call_api('/stuff/', 'POST', body=body)
        request_mock.assert_called_with(
            'POST', 'http://example.com/stuff/', body=today.isoformat(),
            headers=self.base_expected_headers,
            post_params=None, query_params=None)

    def test_update_params_for_auth(self):
        """
        Verify that authentication is defined correctly
        """
        auth_settings = None
        headers = {}
        query_params = {}
        self.client.update_params_for_auth(headers, query_params, auth_settings)
        # confirm that neither dict was modified
        self.assertEqual({}, headers)
        self.assertEqual({}, query_params)

    def test_user_agent(self):
        """
        Verifies that clients are being constructed with user agent
        """
        self.assertEqual('Python-Swagger', self.client.user_agent)

    def test_deserialize_model_gracefully_handles_bad_input(self):
        """
        Verifies that we won't try to enumerate an object not of list/dict type
        when trying to cast it to a model type
        """
        from ambition.models import PublicApiDataListResponse
        model = self.client.deserialize_model(PublicApiDataListResponse, None)
        self.assertIsInstance(model, PublicApiDataListResponse)
        for attribute in model.attribute_map:
            self.assertIsNone(getattr(model, attribute))

    def test_deserialize_datetimes(self):
        """
        Verifies that datetimes are deserialized
        """
        now = datetime.datetime.now()
        now_deserialized = self.client.deserialize(now.isoformat(), 'datetime')
        self.assertEqual(now, now_deserialized)
