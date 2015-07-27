import zdb
import itertools
from zsearch_definitions import hoststore_pb2, common_pb2
import time
import unittest
import socket

import testcase


class DeltaTest(testcase.ZDBTestCase):

    TIMEOUT = 3

    def setUp(self):
        super(DeltaTest, self).setUp()
        self.service = self.query_grpc.service

    def test_new_hosts(self):
        start_ip = 0x01020304
        stop_ip = start_ip + 10
        records = list(zdb.iter_ipv4_record(
                start_ip, 443, 3, 2, ip_stop=stop_ip
        ))
        deltas = list()
        for record in records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_HOST)
            self.assertDeltaMatchesRecord(delta, record)
            self.assertDeltaHasMergedTagsAndMetadata(delta, [record])


    def test_identical_hosts(self):
        start_ip = 0x8dd47d89
        stop_ip = start_ip + 100
        records = list(zdb.iter_ipv4_record(
                start_ip, 80, 5, 4, ip_stop=stop_ip
        ))
        deltas = list()
        for record in records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
        for record in records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_NO_CHANGE)

    def test_metadata_tags_merge_host(self):
        start_ip = 0x8dd47d89
        stop_ip = start_ip + 100
        records = list(zdb.iter_ipv4_record(
                start_ip, 80, 5, 4, ip_stop=stop_ip
        ))
        deltas = list()
        for record in records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
        m = {
            "another_key": "another_value",
            "zed_key": "zed_value",
            "new_key": "new_value",
            "key": "not the original value",
        }
        metadata_list = itertools.cycle([m])
        atoms = zdb.iter_protocol_atom(metadata_list=metadata_list)
        more_records = list(zdb.iter_ipv4_record(
                start_ip, 443, 8, 6, ip_stop=stop_ip
        ))
        for record, new_record in itertools.izip(records, more_records):
            delta = self.service.PutHostIPv4Record(new_record, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertDeltaMatchesRecord(delta, new_record)
            self.assertDeltaHasMergedTagsAndMetadata(delta, [record, new_record])

    def test_overwrite_subprotocol(self):
        start_ip = 0x5601afb6
        stop_ip = start_ip + 10
        records = list(zdb.iter_ipv4_record(
            start_ip, 80, 5, 4, ip_stop=stop_ip
        ))
        original_atoms = [record.atom for record in records]
        for record in records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
        new_atoms = [hoststore_pb2.ProtocolAtom(
                data=atom.data,
                tags=["new_tag"],
                metadata=[common_pb2.Metadatum(
                        key="new_metdatum_key", value="value")
                ],
        ) for atom in original_atoms]
        new_records = list(zdb.iter_ipv4_record(
            start_ip, 80, 5, 4, ip_stop=stop_ip, atom_list=new_atoms,
        ))
        for record in new_records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_SUBPROTOCOL)
            self.assertDeltaHasMergedTagsAndMetadata(delta, [record])

    def test_metadata_tags_merge_protocol(self):
        start_ip = 0x8dd47d89
        stop_ip = start_ip + 5
        first_subproto = 3
        second_subproto = 4
        first_records = list(zdb.iter_ipv4_record(
                start_ip, 443, 5, first_subproto, ip_stop=stop_ip
        ))
        first_atoms = [record.atom for record in first_records]
        for record in first_records:
            delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_HOST)

        new_atoms = [hoststore_pb2.ProtocolAtom(
                data=atom.data,
                tags=["another_tag"],
                metadata=[common_pb2.Metadatum(
                        key="key",
                        value="new_value")
                ],
        ) for atom in first_atoms]
        second_records = list(zdb.iter_ipv4_record(
                start_ip, 443, 5, second_subproto, ip_stop=stop_ip
        ))
        for first, second in itertools.izip(first_records, second_records):
            delta = self.service.PutHostIPv4Record(second, self.TIMEOUT)
            self.assertIsNotNone(delta)
            self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
            self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_SUBPROTOCOL)
            self.assertDeltaHasMergedTagsAndMetadata(delta, [first, second])

        def test_metadata_tags_merge_port(self):
            first_proto = 5
            second_proto = 6
            first_subproto = 4
            second_subproto = 12
            tags = ["a", "b"]
            metadata = [
                common_pb2.Metadatum(key="k1", value="v1"),
                common_pb2.Metadataum(key="k2", value="v2"),
            ]
            first_atoms = zdb.iter_protocol_atom(
                tags_list=itertools.cycle([tags]),
                metadata_list=itertools.cycle([metadata])
            )
            start_ip = 0x18af03d8
            stop_ip = start_ip + 10*5
            first_records = list(zdb.iter_ipv4_record(
                    start_ip, 443, first_proto, first_subproto, ip_stop=stop_ip,
                    ip_step=5, atom_list=first_atoms
            ))
            for record in first_records:
                delta = self.service.PutHostIPv4Record(record, self.TIMEOUT)
                self.assertIsNotNone(delta)
            second_tags = ["b", "c"]
            second_metadata = [
                common_pb2.Metadataum(key="k2", value="v3"),
                common_pb2.Metadataum(key="k3", value="v3"),
            ]
            second_atoms = zdb.iter_protocol_atom(
                tags_list=itertools.cycle([second_tags]),
                metadata_list=itertools.cycle([second_metadata])
            )
            second_records = list(zdb.iter_ipv4_record(
                    start_ip, 443, second_proto, second_subproto, ip_stop=stop_ip,
                    ip_step=5, atom_list=second_atoms
            ))
            for first, second in itertools.izip(first_record, second_records):
                delta = self.service.PutHostIPv4Record(second, self.TIMEOUT)
                self.assertIsNotNone(delta)
                self.assertEqual(delta.delta_type, hoststore_pb2.Delta.DT_UPDATE)
                self.assertEqual(delta.delta_scope, hoststore_pb2.Delta.SCOPE_PROTOCOL)
                self.assertDeltaHasMergedTagsAndMetadata(delta, [first, second])

if __name__ == "__main__":
    unittest.main()
