from unittest import TestCase
import mock
from .plugin import JSCS


class JSCSTest(TestCase):
    def test_command_returns_airbnb_if_no_config(self):
        plugin = JSCS(None)
        with mock.patch('os.path') as mock_op:
            mock_op.join.return_value = '/tmp/foo.js'
            mock_op.exists.return_value = False
            cmd = plugin.get_command('/tmp')
            self.assertEqual('jscs -r inline -p airbnb', cmd)

    def test_command_returns_config_if_available(self):
        plugin = JSCS(None)
        with mock.patch('os.path') as mock_op:
            path = '/tmp/.jscsrc'
            mock_op.join.return_value = path
            mock_op.exists.return_value = True
            cmd = plugin.get_command('/tmp')

            self.assertEqual('jscs -r inline -c /tmp/.jscsrc', cmd)
