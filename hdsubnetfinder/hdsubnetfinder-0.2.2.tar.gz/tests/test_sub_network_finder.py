# -*- coding: utf-8 -*-

import unittest
import os
from hdsubnetfinder.kernel.kernel_generator import KernelGenerator

KERNEL_LOCATION = 'resource/kernel.txt'
k_file = os.path.abspath(os.path.dirname(__file__)) + '/' + KERNEL_LOCATION
SAMPLE_KERNEL_URL = 'file://' + k_file

NETWORK_LOCATION = 'resource/small_network.sif'
net_file = os.path.abspath(os.path.dirname(__file__)) + '/' + NETWORK_LOCATION
NETWORK_URL = 'file://' + net_file
print(NETWORK_URL)


class SubNetworkFinderTests(unittest.TestCase):

    def test_find_sub_network(self):
        print('\n---------- Sub Network Finder tests start -----------\n')

        from hdsubnetfinder.subnetwork.sub_network_finder import SubNetworkFinder
        import hdsubnetfinder.subnetwork.network_util as util


        # Create kernel from pre-computed kernel file
        generator = KernelGenerator()
        small_kernel = generator.create_kernel_from_file(pre_computed_kernel_url=SAMPLE_KERNEL_URL)
        small_sif = util.read_sif(file_url=NETWORK_URL)

        finder = SubNetworkFinder(network=small_sif, kernel=small_kernel)

        identifiers = ["NRAS", "KRAS", "MAPK1"]

        result = finder.get_sub_network(identifiers)
        self.assertIsNotNone(result)

        print(len(result))

        self.assertEqual(list, type(result))

        print('\n---------- finder tests finished! -----------\n')

    def test_find_sub_network2(self):
        print('\n---------- Sub Network Finder tests 2 start -----------\n')

        from hdsubnetfinder.subnetwork.sub_network_finder import SubNetworkFinder
        import hdsubnetfinder.subnetwork.network_util as util
        from hdsubnetfinder.kernel.kernel_generator import KernelGenerator

        generator = KernelGenerator()
        small_kernel = generator.create_kernel(network_url=NETWORK_URL)
        small_sif = util.read_sif(file_url=NETWORK_URL)

        finder = SubNetworkFinder(network=small_sif, kernel=small_kernel)

        identifiers = ["NRAS", "KRAS", "MAPK1"]

        result = finder.get_sub_network(identifiers)
        self.assertIsNotNone(result)
        print(len(result))
        self.assertEqual(list, type(result))

        print('\n---------- finder tests2 finished! -----------\n')

    # def test_find_sub_network3(self):
    #     from hdsubnetfinder.subnetwork.sub_network_finder import SubNetworkFinder
    #     import hdsubnetfinder.subnetwork.network_util as util
    #     from hdsubnetfinder.kernel.kernel_generator import KernelGenerator
    #
    #     generator = KernelGenerator()
    #     med_network = 'https://s3-us-west-2.amazonaws.com/ci-service-data/yeastHighQuality.sif'
    #     med_kernel = generator.create_kernel(network_url=med_network)
    #     med_sif = util.read_sif(file_url=med_network)
    #
    #     finder = SubNetworkFinder(network=med_sif, kernel=med_kernel)
    #
    #     identifiers = ["YNL031C", "YNL145W"]
    #
    #     result = finder.get_sub_network(identifiers)
    #     self.assertIsNotNone(result)
    #     print(len(result))
    #     self.assertEqual(list, type(result))
    #
    #     print('\n---------- finder tests2 finished! -----------\n')
