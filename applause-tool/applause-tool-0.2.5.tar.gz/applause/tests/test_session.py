import json
import unittest2
import mock

from ..session import AuthSession

try:
    # Python2.X
    import __builtin__ as builtins
except ImportError:
    # Python3.X
    import builtins


class SessionTest(unittest2.TestCase):

    def setUp(self):
        pass

    @mock.patch.object(builtins, 'open')
    def test_store_cookie(self, open):
        file = mock.MagicMock()
        open.return_value = file

        auth = AuthSession(client_id='dummy', client_secret='dummy', load_cookie=False)
        auth.config_path = 'dummy_path'

        data = {'key': 'value'}
        auth._store_cookie(data)

        open.assert_called_once_with('dummy_path', 'w')
        file.__enter__().write.assert_called_once_with(json.dumps(data))

    # @mock.patch.object(builtins, 'open')
    # def test_load_cookie(self, open):
    #     file = mock.MagicMock()
    #     open.return_value = file
    #
    #     auth = AuthSession(client_id='dummy', client_secret='dummy', load_cookie=False)
    #     auth.config_path = 'dummy_path'
    #
    #     data = {'key': 'value'}
    #     auth._load_cookie()
    #
    #     open.assert_called_once_with('dummy_path', 'r')
    #     # file.__enter__().read.assert_called_once_with()