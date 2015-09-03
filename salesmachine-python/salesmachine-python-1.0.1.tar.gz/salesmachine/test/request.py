from datetime import datetime
import unittest
import json

from salesmachine.request import post, DatetimeSerializer


class TestRequests(unittest.TestCase):

    def test_valid_request(self):
        res = post('key', 'secret', debug=True, batch=[{
            'contact_uid': 'contact_uid',
            'method': 'set_contact'
        }])
        self.assertEqual(res.status_code, 201)

    def test_invalid_request_error(self):
        self.assertRaises(Exception, post, 'testsecret', '[{]')

    def test_datetime_serialization(self):
        data = { 'created': datetime(2012, 3, 4, 5, 6, 7, 891011) }
        result = json.dumps(data, cls=DatetimeSerializer)
        self.assertEqual(result, '{"created": "2012-03-04T05:06:07.891011"}')
