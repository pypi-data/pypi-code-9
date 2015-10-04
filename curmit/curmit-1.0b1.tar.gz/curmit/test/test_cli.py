import unittest
from unittest.mock import patch, Mock

from curmit.curmit import main


class TestCLI(unittest.TestCase):

    @patch('curmit.curmit._run', Mock(return_value=False))
    def test_exit(self):
        """Verify 'curmit' treats False as an error ."""
        self.assertRaises(SystemExit, main, [])

    @patch('curmit.curmit._run', Mock(side_effect=KeyboardInterrupt))
    def test_interrupt(self):
        """Verify 'curmit' treats KeyboardInterrupt as an error."""
        self.assertRaises(SystemExit, main, [])


@patch('curmit.curmit._run', Mock(return_value=True))
class TestLogging(unittest.TestCase):

    def test_verbose_1(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main(['-v']))

    def test_verbose_2(self):
        """Verify verbose level 2 can be set."""
        self.assertIs(None, main(['-vv']))

    def test_verbose_3(self):
        """Verify verbose level 3 can be set."""
        self.assertIs(None, main(['-vvv']))
