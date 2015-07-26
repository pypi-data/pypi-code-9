import itertools
import unittest

import sh

import zdb

import zsearch_definitions.query
import zsearch_definitions.admin


class ZDBTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.c = zdb.get_zdb_test_config()

    def setUp(self):
        pkill = sh.Command("pkill")
        try:
            pkill("-9", "zdb")
        except sh.ErrorReturnCode:
            pass
        sh.rm("-rf", sh.glob("/tmp/zdb/*"))
        self.zdb_handle = self.c.zdb(_bg=True, _err="zdb_stderr.txt")
        
        self.query_grpc = zsearch_definitions.query.QueryService()
        self.admin_grpc = zsearch_definitions.admin.AdminService()
        
    def tearDown(self):
        if self.zdb_handle is not None:
            self.zdb_handle.terminate()

    def assertTagsEqual(self, a, b):
        self.assertEqual(len(a), len(b))
        for atag, btag in itertools.izip(a, b):
            self.assertEqual(atag, btag)

    def assertMetadatumEqual(self, a, b):
        self.assertEqual(a.key, b.key)
        self.assertEqual(a.value, b.value)

    def assertMetadataEqual(self, a, b):
        self.assertEqual(len(a), len(b))
        for am, bm in itertools.izip(a, b):
            self.assertMetadatumEqual(am, bm)

    def assertProtocolAtomEqual(self, a, b):
        # Check data
        self.assertEqual(a.data, b.data)

        # Check tags
        if a.tags is None:
            self.assertIsNone(b.tags)
        else:
            self.assertIsNotNone(b.tags)
            self.assertTagsEqual(a.tags, b.tags)

        # Check metadata
        if a.metadata is None:
            self.assertIsNone(b.metadata)
        else:
            self.assertIsNotNone(b.metadata)
            self.assertMetadataEqual(a.metadata, b.metadata)

    def assertRecordEqual(self, a, b,
                          check_scan_id=True, check_timestamp=True,
                          check_first_seen_at=True, check_last_seen_at=True):
        self.assertEqual(a.ip, b.ip)
        self.assertEqual(a.port, b.port)
        self.assertEqual(a.protocol, b.protocol)
        self.assertEqual(a.subprotocol, b.subprotocol)
        self.assertEqual(a.domain, b.domain)
        if check_timestamp:
            self.assertEqual(a.timestamp, b.timestamp)
        if check_scan_id:
            self.assertEqual(a.scanid, b.scanid)
        self.assertEqual(a.sha256fp, b.sha256fp)
        if check_first_seen_at:
            self.assertEqual(a.first_seen_at_scan_id, b.first_seen_at_scan_id)
        if check_last_seen_at:
            self.assertEqual(a.last_seen_at_scan_id, b.last_seen_at_scan_id)
        self.assertEqual(a.HasField("atom"), b.HasField("atom"))
        if a.HasField("atom"):
            self.assertProtocolAtomEqual(a.atom, b.atom)
        else:
            # Not yet implemented
            self.fail()

    def assertDeltaMatchesRecord(self, delta, record):
        self.assertEqual(delta.ip, record.ip)
        self.assertEqual(delta.protocol, record.protocol)
        self.assertEqual(delta.port, record.port)
        self.assertEqual(delta.subprotocol, record.subprotocol)
        self.assertEqual(delta.domain, record.domain)
        record_oneof = record.WhichOneof("data_oneof")
        if record_oneof == "atom":
            self.assertTrue(delta.HasField("data"))
            self.assertProtocolAtomEqual(delta.data, record.atom)
        else:
            # unimplemented
            self.fail()
