from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from unittest2 import TestCase
import json


class FtwJsondumpTestCase(TestCase):

    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def assert_structure_equal(self, expected, got, msg=None):
        got = json.dumps(got, sort_keys=True, indent=4)
        expected = json.dumps(expected, sort_keys=True, indent=4)
        self.maxDiff = None
        self.assertMultiLineEqual(got, expected, msg)
