# -*- coding: utf-8 -*-

import unittest

import json

from hdsubnetfinder.sub_network_finder import SubNetworkFinder


class SubNetworkFinderTests(unittest.TestCase):

    def setUp(self):
        self.finder = SubNetworkFinder()

    def test_find_sub_network(self):
        print('\n---------- Sub Network Finder tests start -----------\n')

        identifiers = ["NRAS", "KRAS", "MAPK1"]

        result = self.finder.get_sub_network(identifiers)
        self.assertIsNotNone(result)

        print(json.dumps(result, indent=4))
        self.assertEqual(list, type(result))

        print('\n---------- finder tests finished! -----------\n')
