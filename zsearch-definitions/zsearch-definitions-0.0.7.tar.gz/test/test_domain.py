import zdb
import itertools
from zsearch_definitions import hoststore_pb2, common_pb2
import time
import unittest

import testcase


class DomainTest(testcase.ZDBTestCase):

    TIMEOUT = 3

    DOMAINS = ["davidadrian.org", "zakird.com", "umich.edu", "google.com"]

    def setUp(self):
        super(DomainTest, self).setUp()
        self.service = self.query_grpc.service

    def test_insert_host_same_tags_metdata(self):
        domain = "davidadrian.org"
        ip = 0x8dd47859
        records = list()
        first = True
        for port in range(1, 10):
            record = zdb.get_domain_record(domain, port, 20, 5)
            records.append(record)
            delta = self.service.PutHostDomainRecord(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertDeltaMatchesRecord(delta, record)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            if first:
                expected_scope = hoststore_pb2.Delta.SCOPE_HOST
                first = False
            else:
                expected_scope = hoststore_pb2.Delta.SCOPE_PORT
            self.assertEqual(delta.delta_scope, expected_scope)
            self.assertDeltaHasMergedTagsAndMetadata(delta, records)

    def test_insert_multiple_host(self):
        for domain in self.DOMAINS:
            record = zdb.get_domain_record(domain, 443, 5, 6)
            delta = self.service.PutHostDomainRecord(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertDeltaMatchesRecord(delta, record)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_HOST)

    def test_scopes(self):
        domain = "davidadrian.org"
        first = zdb.get_domain_record(domain, 443, 5, 6)
        delta = self.service.PutHostDomainRecord(first, self.TIMEOUT)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_HOST)
        self.assertDeltaMatchesRecord(delta, first)
        second = zdb.get_domain_record(domain, 80, 5, 6)
        delta = self.service.PutHostDomainRecord(second, self.TIMEOUT)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_PORT)
        self.assertDeltaMatchesRecord(delta, second)
        third = zdb.get_domain_record(domain, 443, 10, 4)
        delta = self.service.PutHostDomainRecord(third, self.TIMEOUT)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_PROTOCOL)
        self.assertDeltaMatchesRecord(delta, third)
        fourth = zdb.get_domain_record(domain, 443, 10, 6)
        delta = self.service.PutHostDomainRecord(fourth, self.TIMEOUT)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_SUBPROTOCOL)
        self.assertDeltaMatchesRecord(delta, fourth)
        fifth = zdb.get_domain_record(domain, 443, 12, 6)
        delta = self.service.PutHostDomainRecord(fifth, self.TIMEOUT)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_PROTOCOL)
        self.assertDeltaMatchesRecord(delta, fifth)
        sixth = zdb.get_domain_record("yolo.swag", 443, 12, 6)
        delta = self.service.PutHostDomainRecord(sixth, self.TIMEOUT)
        self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
        self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_HOST)
        self.assertDeltaMatchesRecord(delta, sixth)



if __name__ == "__main__":
    unittest.main()
