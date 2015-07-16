import unittest2
import mock
import requests_mock

from ..errors import InvalidLogin
from ..auth import ApplauseAuth

from applause import settings


class TestApplauseAuth(unittest2.TestCase):
    """
    Tests for the Applause OAuth handshake.
    """

    def setUp(self):
        self.auth = ApplauseAuth(client_id='dummy_id', client_secret='dummy_secret')

    def test_init_defaults(self):
        """
        Makes sure an ApplauseAuth object is initialized with defaults.
        """
        CLIENT_ID = 'dummy_ID'
        CLIENT_SECRET = 'dummy_secret'

        default_auth = ApplauseAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET)
        self.assertEqual(default_auth.client_id, CLIENT_ID)
        self.assertEqual(default_auth.client_secret, CLIENT_SECRET)
        self.assertEqual(default_auth.oauth_base_url, settings.OAUTH_BASE_URL)
        self.assertEqual(default_auth.platform_url, settings.PLATFORM_URL)

    def test_init_with_custom_url(self):
        """
        Makes sure an ApplauseAuth object accepts extra settings.
        """
        CLIENT_ID = 'dummy_ID'
        CLIENT_SECRET = 'dummy_secret'
        OAUTH_BASE_URL = 'dummy_base_url'
        PLATFORM_URL = 'dummy_platform_url'

        default_auth = ApplauseAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    oauth_base_url=OAUTH_BASE_URL,
                                    platform_url=PLATFORM_URL)
        self.assertEqual(default_auth.client_id, CLIENT_ID)
        self.assertEqual(default_auth.client_secret, CLIENT_SECRET)
        self.assertEqual(default_auth.oauth_base_url, OAUTH_BASE_URL)
        self.assertEqual(default_auth.platform_url, PLATFORM_URL)

    def test_create_session(self):
        """
        Makes sure proper client credentials are embedded in the generated
        HTTPS session.
        """
        self.assertEquals(self.auth.session.auth, ('dummy_id', 'dummy_secret'))

    @mock.patch('applause.auth.ApplauseAuth.get_platform_security_check_url')
    @mock.patch('applause.auth.ApplauseAuth.get_oauth_authorize_url')
    def test_get_code_success(self, get_oauth_authorize_url, get_platform_security_check_url):
        """
        Verifies the flow of exchanging client credentials for a OAuth
        authorization code.
        """
        get_oauth_authorize_url.return_value = 'oauth_authorize_url'
        get_platform_security_check_url.return_value = 'sec_check_url'

        cookies_response = mock.Mock()
        cookies_response.cookies = {'applause-platform': 'AUTHKEY'}
        self.auth.session = mock.Mock()
        self.auth.session.post = mock.Mock(return_value=cookies_response)

        code_response = mock.Mock()
        code_response.headers = {'location': 'https://example.com/foo/bar/?code=quux&other=param'}
        self.auth.session.get = mock.Mock(return_value=code_response)

        assert self.auth._get_code('joe', 's3cr3t') == 'quux'

        self.auth.session.post.assert_called_once_with('sec_check_url', data={
            'j_username': 'joe',
            'j_password': 's3cr3t',
        }, allow_redirects=False)

        self.auth.session.get.assert_called_once_with('oauth_authorize_url',
                                                      params={'client_id': 'dummy_id'},
                                                      allow_redirects=False,
                                                      cookies={'applause-platform': 'AUTHKEY'})

    def test_get_code_invalid_credentials(self):
        """
        PLATFORM_SECURITY_CHECK_URL does not respond with proper cookie headers.
        This happens when wrong credentials are provided.
        """
        with requests_mock.Mocker() as m:
            url = ApplauseAuth.get_platform_security_check_url(settings.PLATFORM_URL)
            m.post(url, headers={}, status_code=302)
            with self.assertRaises(InvalidLogin):
                self.auth._get_code(username='username', password='password')

    def test_fetch_tokens_valid_code(self):
        """
        In exchange for authorization code we should be able to obtain:
            * access_token
            * refresh_token
            * user_id
        """
        with requests_mock.Mocker() as m:
            url = ApplauseAuth.get_oauth_token_url(settings.OAUTH_BASE_URL)
            m.post(
                url,
                status_code=200,
                json={'access_token': 'AT', 'user_id': '1', 'refresh_token': 'RT'}
            )

            tokens = self.auth._fetch_tokens(code='dummy')
            self.assertEquals(tokens['access_token'], 'AT')
            self.assertEquals(tokens['refresh_token'], 'RT')
            self.assertEquals(tokens['user_id'], '1')

    def test_fetch_tokens_error(self):
        """
        Valid token information can't be obtained ATM.
        """
        with requests_mock.Mocker() as m:
            url = ApplauseAuth.get_oauth_token_url(settings.OAUTH_BASE_URL)
            m.post(url, status_code=400)
            with self.assertRaises(InvalidLogin):
                self.auth._fetch_tokens(code='dummy')

    def test_refresh_tokens_valid(self):
        """
        In exchange for current refresh token we should be able to obtain:
            * access_token
            * refresh_token
            * user_id
        """
        with requests_mock.Mocker() as m:
            url = ApplauseAuth.get_oauth_refresh_url(settings.OAUTH_BASE_URL)
            m.post(
                url,
                status_code=200,
                json={'access_token': 'AT', 'user_id': '1', 'refresh_token': 'RT'}
            )

            tokens = self.auth._refresh_token(token='dummy')
            self.assertEquals(tokens['access_token'], 'AT')
            self.assertEquals(tokens['refresh_token'], 'RT')
            self.assertEquals(tokens['user_id'], '1')

    def test_refresh_tokens_error(self):
        """
        Valid token information can't be obtained ATM.
        """
        with requests_mock.Mocker() as m:
            url = ApplauseAuth.get_oauth_refresh_url(settings.OAUTH_BASE_URL)
            m.post(url, status_code=400)
            with self.assertRaises(InvalidLogin):
                self.auth._refresh_token(token='dummy')

    def test_generate_session(self):
        """
        Make sure that proper headers are placed in a generated http session.
        """
        session = ApplauseAuth.generate_requests_session(access_token='dummy')

        self.assertIn('Authorization', session.headers)
        self.assertEquals(session.headers['Authorization'], 'Bearer {token}'.format(token='dummy'))

        self.assertIn('Accept', session.headers)
        self.assertEquals(session.headers['Accept'], 'application/json')

    @mock.patch.object(ApplauseAuth, '_get_code')
    @mock.patch.object(ApplauseAuth, '_fetch_tokens')
    def test_login_username_password(self, fetch_tokens, get_code):
        """
        Check the method execution flow for username+password login
        """
        get_code.return_value = 'XYZ'

        self.auth.login(username='username', password='password')
        get_code.assert_called_once_with('username', 'password')
        fetch_tokens.assert_called_once_with('XYZ')

    @mock.patch.object(ApplauseAuth, '_refresh_token')
    def test_login_refresh_token(self, refresh_token):
        """
        Check the method execution flow for refresh_token login
        """
        self.auth.login(refresh_token='dummy')
        refresh_token.assert_called_once_with(token='dummy')
