import unittest
from lifecycle import Lifecycle

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.lifecycle = Lifecycle('07fd3326118474520dc18baf')

    def test_initialize(self):
        self.assertEqual(self.lifecycle.getApiKey(), '07fd3326118474520dc18baf')

    def test_identify(self):
        params = {"unique_id": "1234",
                  "first_name": "Nathan",
                  "last_name": "Mooney",
                  "email_address": "someone@getvenn.io",
                  "phone_number": "12345678913"
        }
        response = self.lifecycle.identify(params)
        self.assertEqual(response.code, 200)

    def test_track(self):
        response = self.lifecycle.track("event", "5")
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()
