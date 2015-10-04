# pylint: disable=no-self-use

import unittest
import logging

from curmit.curmit import main, urltext


SAMPLE_URL = "https://docs.google.com/document/d/1UamfLkA-DvIVXPKoFQpSQDIUDANPTfyyXYMlUHmKpp4/pub?embedded=True"


class TestCLI(unittest.TestCase):  # pylint: disable=R0904
    """Integration tests for the 'curmit' command."""

    def test_no_update(self):
        """Verify 'curmit --no-update' can be called."""
        self.assertIs(None, main(['--no-update']))

    def test_no_commit(self):
        """Verify 'curmit --no-commit' can be called."""
        self.assertIs(None, main(['--no-commit']))


class TestUrlText(unittest.TestCase):
    """Integration tests for getting URL text."""

    def test_sample(self):
        """Verify text is grabbed from a URL."""
        lines = urltext(SAMPLE_URL)
        for line in lines:
            logging.debug(line)
        self.assertIn("Sample File", lines[0])

    def test_invalid(self):
        """Verify an exception is raised on an invalid URL."""
        self.assertRaises(IOError, urltext, "")
