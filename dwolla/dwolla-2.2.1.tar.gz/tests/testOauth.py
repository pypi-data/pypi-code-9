import unittest
from dwolla import oauth, constants
from mock import MagicMock


class OAuthTest(unittest.TestCase):
    def setUp(self):
        oauth.r._get = MagicMock()
        oauth.r._post = MagicMock()
        constants.client_id = "SOME ID"
        constants.client_secret = "SOME SECRET"
        constants.access_token = "AN OAUTH TOKEN"
        constants.oauth_scope = "Balance|AccountInfo"

    def testgenauthurl(self):
        self.assertEqual(oauth.genauthurl(), 'https://uat.dwolla.com/oauth/v2/authenticate?client_id=SOME%20ID&response_type=code&scope=Balance|AccountInfo')

    def testget(self):
        oauth.get('CODE')
        oauth.r._post.assert_any_call('/token/', {'code': 'CODE', 'client_secret': 'SOME SECRET', 'grant_type': 'authorization_code', 'client_id': 'SOME ID'}, '/oauth/v2', 'dict')

    def testrefresh(self):
        oauth.refresh('REFRESH')
        oauth.r._post.assert_any_call('/token/', {'client_secret': 'SOME SECRET', 'grant_type': 'refresh_token', 'refresh_token': 'REFRESH', 'client_id': 'SOME ID'}, '/oauth/v2', 'dict')

    def testcatalog(self):
        oauth.catalog(alternate_token='CATALOG TOKEN')
        oauth.r._get.assert_any_call('/catalog', dwollaparse='dict', params={'oauth_token': 'CATALOG TOKEN'})

if __name__ == '__main__':
    unittest.main()