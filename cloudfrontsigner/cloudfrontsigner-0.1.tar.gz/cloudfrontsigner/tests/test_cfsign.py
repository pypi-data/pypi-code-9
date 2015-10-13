# -*- coding: utf-8 -*-

import os
import mock
import sys
import unittest


here = os.path.abspath(os.path.dirname(__file__))


class CFSignTestCase(unittest.TestCase):

    @mock.patch('cloudfrontsigner.CannedPolicySigner')
    def test(self, mocked_signer):
        mocked_sign = mock.Mock()
        mocked_sign.return_value = 'signed'
        mocked_signer.return_value.sign = mocked_sign

        tmp = sys.argv
        sys.argv = ['prog', 'keyid', 'pem', '1', 'url']
        try:
            from .. import cfsign
            cfsign.main()
        finally:
            sys.argv = tmp

        mocked_signer.assert_called_once_with(
            key_pair_id='keyid',
            key_path='pem',
            expire_seconds=1,
        )
        mocked_sign.assert_called_once_with('url')
