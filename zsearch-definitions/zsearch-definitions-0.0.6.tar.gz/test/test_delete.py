import zdb
import itertools
from zsearch_definitions import hoststore_pb2, common_pb2
import time
import unittest

import testcase


class DeleteTest(testcase.ZDBTestCase):

    TIMEOUT = 3

    def setUp(self):
        super(DeleteTest, self).setUp()
        self.service = self.query_grpc.service

    def test_insert_delete_one(self):
        record = zdb.get_ipv4_record(0x01020304, 443, 80, 5)
        delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
        self.assertIsNotNone(delta)
        hq = zdb.host_query_from_record(record)
        delta = self.service.DelHostIPv4Record(hq, self.TIMEOUT)
        self.assertIsNotNone(delta)
        self.assertDeltaMatchesHostQuery(delta, hq)
        self.assertDeltaMatchesRecord(delta, record)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_DELETE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_HOST)


if __name__ == "__main__":
    unittest.main()
