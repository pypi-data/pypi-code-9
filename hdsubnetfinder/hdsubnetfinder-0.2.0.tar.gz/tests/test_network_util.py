# -*- coding: utf-8 -*-
import unittest
import pandas as pd
import json

small_network = 'https://s3-us-west-2.amazonaws.com/ci-service-data/small.sif'


class NetworkUtilTests(unittest.TestCase):

    def test_read_sif(self):
        import hdsubnetfinder.subnetwork.network_util as util
        df = pd.read_csv(small_network, sep='\t', names=['source', 'interaction', 'target'])
        print(df.shape)

        triples = util.read_sif(small_network)
        self.assertIsNotNone(triples)
        self.assertEqual(df.shape[0], len(triples))

    def test_sif2cx(self):
        import hdsubnetfinder.subnetwork.network_util as util
        triples = util.read_sif(small_network)
        cx = util.sif2cx(triples)
        print(json.dumps(cx, indent=4))

        self.assertEqual(list, type(cx))
        # Add more tests here...
