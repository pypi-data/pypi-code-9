"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
try:
    import mock
except ImportError as exc:
    exc.args = ('The `mock` library is required for running tests',)
    raise
from easyconfig import Config

from confpages.token import make_token
from confpages.conf import settings
from .loaders import DummyLoader, DummyAPILoader

client = Client()


class DummyResponse(object):

    def __init__(self, content, status_code, headers):
        self.content = content
        self.status_code = status_code
        self.headers = headers


class ConfPagesTest(TestCase):

    @mock.patch('confpages.views.ConfPages.page_loader', DummyLoader())
    def test_get_base_page(self):
        response = client.get('/p/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'This is the Index page')

    @mock.patch('confpages.views.ConfPages.page_loader', DummyLoader())
    def test_get_index_page(self):
        response = client.get('/p/index/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'This is the Index page')

    def test_post_index_page_without_token(self):
        data = {'greeting': 'hello'}
        response = client.post('/p/index/', data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, 'Missing one-time token')

    def test_post_index_page_with_invalid_token(self):
        data = {'greeting': 'hello', '_onetimetoken': 'dummy_token'}
        response = client.post('/p/index/', data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, 'Invalid one-time token')

    def test_post_index_page_with_expired_token(self):
        token = make_token()
        data = {'greeting': 'hello', '_onetimetoken': token}
        mock_settings = Config(dict(
            PAGE_LOADER=settings.PAGE_LOADER,
            TOKEN_EXPIRES=0
        ))
        with mock.patch('confpages.token.settings', mock_settings):
            response = client.post('/p/index/', data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, 'Expired one-time token')

    def test_post_index_page_without_api_url(self):
        token = make_token()
        data = {'greeting': 'hello', '_onetimetoken': token}
        response = client.post('/p/index/', data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')

    @mock.patch('confpages.views.ConfPages.page_loader', DummyAPILoader())
    def test_post_index_page_with_nonexistent_api_url(self):
        token = make_token()
        data = {'greeting': 'hello', '_onetimetoken': token}
        response = client.post('/p/index/', data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, 'The backend API can not be found')

    @mock.patch('confpages.views.ConfPages.page_loader', DummyAPILoader())
    def test_post_index_page_successful(self):
        token = make_token()
        data = {'greeting': 'hello', '_onetimetoken': token}
        with mock.patch('confpages.views.ConfPages.client.request') \
                as mock_request:
            mock_request.return_value = DummyResponse(
                content='The form submission is successful',
                status_code=200,
                headers={'Content-Type': 'application/json'}
            )
            response = client.post('/p/index/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'The form submission is successful')
        self.assertEqual(response['Content-Type'], 'application/json')
