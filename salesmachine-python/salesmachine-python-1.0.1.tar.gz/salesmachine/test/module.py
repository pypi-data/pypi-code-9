import unittest

import salesmachine


class TestModule(unittest.TestCase):

    def failed(self):
        self.failed = True

    def setUp(self):
        self.failed = False
        salesmachine.key = 'testkey'
        salesmachine.secret = 'testsecret'
        salesmachine.on_error = self.failed
        salesmachine.debug = True

    def test_set_contact(self):
      salesmachine.set_contact('contact_uid')
      salesmachine.flush()

    def test_set_account(self):
      salesmachine.set_account('account_uid')
      salesmachine.flush()

    def test_track_event(self):
      salesmachine.track_event('contact_uid', 'event_uid')
      salesmachine.flush()

    def test_track_pageview(self):
      salesmachine.track_pageview('contact_uid')
      salesmachine.flush()

    def test_flush(self):
        salesmachine.flush()
