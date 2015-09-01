from jquerypluginbp.core import install_dependencies
import unittest
from mock import patch

class TestInstallDependencies(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('jquerypluginbp.core.os')
    def test_execute_dependencies_install_commands(self, mock_os):
        install_dependencies('build')
        self.assertEqual(mock_os.system.call_count, 3)
