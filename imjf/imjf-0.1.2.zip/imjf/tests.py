
import unittest

from .client import ismyjsfucked
from .exceptions import IMJFException, ReportException

class TestIntegration(unittest.TestCase):
    def url(self, test_name):
        urltemplate = 'http://www.ismyjsfucked.com/tests/{name}.html'
        return urltemplate.format(name=test_name)

    def assert_exc_message(self, message, *args, **kw):
        with self.assertRaises(IMJFException) as context:
            ismyjsfucked(*args, **kw)

        if isinstance(context.exception, ReportException):
            assert isinstance(context.exception.data, dict)

        excmessage = str(context.exception)

        try:
            assert excmessage == message
        except AssertionError:
            print(excmessage, message)
            raise

    def assert_unknown_state_exc(self, *args, **kw):
        self.assert_exc_message("Some details couldn't be confirmed",
                                *args, **kw)

    def test_ok(self):
        assert ismyjsfucked(self.url('ok')) is False

    def test_exception(self):
        assert ismyjsfucked(self.url('exception')) is True

    def test_unknown(self):
        self.assert_unknown_state_exc(self.url('timeout'))

    def test_precedence(self):
        self.assert_unknown_state_exc([self.url('ok'),
                                       self.url('exception'),
                                       self.url('timeout')])

        assert ismyjsfucked([self.url('ok'), self.url('exception')]) is True

        self.assert_unknown_state_exc([self.url('ok'),
                                       self.url('timeout')])

    def test_invalid_url(self):
        self.assert_exc_message("Invalid URL 'not-a-valid-url'",
                                'not-a-valid-url')

    def test_404(self):
        url = 'http://www.ismyjsfucked.com/success-stories/'

        self.assert_unknown_state_exc(url)
        self.assert_unknown_state_exc(url, use_response_status_code=True)

        assert ismyjsfucked(url, False) is False
        assert ismyjsfucked(url, use_response_status_code=0) is False


