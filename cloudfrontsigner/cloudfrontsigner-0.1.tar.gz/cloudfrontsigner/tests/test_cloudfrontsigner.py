# -*- coding: utf-8 -*-

import mock
import os
import unittest


here = os.path.abspath(os.path.dirname(__file__))


class ExpiringSignerTestCase(unittest.TestCase):

    def test_policy1(self):
        from .. import CannedPolicySigner
        signer = CannedPolicySigner(
            key_pair_id='test',
            key_path=os.path.join(here, 'testkey1.pem'),
            expire_seconds=600,
        )
        ret = signer.gen_policy('https://hogehoge.com/fugafuga.txt',
                                expired_at=98765)
        self.assertDictEqual(ret, {'Statement': [{
            'Resource': 'https://hogehoge.com/fugafuga.txt',
            'Condition': {'DateLessThan': {'AWS:EpochTime': 98765}}
        }]})

    @mock.patch('time.time')
    def test_sign1(self, mocked_time):
        mocked_time.return_value = 12345

        from .. import CannedPolicySigner
        signer = CannedPolicySigner(
            key_pair_id='test',
            key_path=os.path.join(here, 'testkey1.pem'),
            expire_seconds=600,
        )
        ret = signer.sign('https://hogehoge.com/fugafuga.txt')

        from ..compat import parse_qs, urlparse
        parts = urlparse(ret)
        self.assertEqual(parts.scheme, 'https')
        self.assertEqual(parts.netloc, 'hogehoge.com')
        self.assertEqual(parts.path, '/fugafuga.txt')
        q = parse_qs(parts.query)
        self.assertListEqual(q.get('Expires'), ['12945'])
        self.assertListEqual(q.get('Key-Pair-Id'), ['test'])
        self.assertEqual(len(q.get('Signature', [])), 1)
