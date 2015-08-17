import os
import unittest
import pandas as pd

from hdsubnetfinder.kernel.kernel_generator import KernelGenerator
from hdsubnetfinder.kernel.kernel import Kernel
import hdsubnetfinder.kernel.kernel_util as util


class KernelGeneratorTests(unittest.TestCase):

    def test_kernel_generator_network(self):

        def run(network):
            generator = KernelGenerator()

            # First, read network file as table
            small_net_df = pd.read_csv(network, sep='\t',
                                       names=['source', 'interaction', 'target'])
            print(small_net_df.shape)

            sources = small_net_df['source']
            targets = small_net_df['target']
            merged = sources.append(targets)
            print(len(merged.unique()))

            # Calculate kernel
            small_kernel = generator.create_kernel(network)

            # Serialize file
            util.write_kernel(small_kernel, 'kernel_out.txt')

            # Get kernel as big string
            self.assertIsNotNone(small_kernel)
            self.assertTrue(isinstance(small_kernel, Kernel))

            self.assertIsNotNone(small_kernel.kernel)
            self.assertIsNotNone(small_kernel.labels)

            df = pd.read_csv('kernel_out.txt', sep='\t', index_col=0)

            self.assertIsNotNone(df)
            print(df.shape)
            # self.assertEqual(generator.num_nodes, df.shape[0])
            # self.assertEqual(generator.num_nodes, df.shape[1])

        print('\n---------- Kernel Generator tests start -----------\n')

        # Small network (takes about 10 seconds to compute)
        small_network_file = 'resource/small_network.sif'
        net_file = os.path.abspath(os.path.dirname(__file__)) + '/' + small_network_file
        small_network_url = 'file://' + net_file
        #small_network = 'https://s3-us-west-2.amazonaws.com/ci-service-data/small.sif'

        # Medium size network (takes about 5 minutes)
        med_network = 'https://s3-us-west-2.amazonaws.com/ci-service-data/yeastHighQuality.sif'

        run(small_network_url)
        #run(med_network)

        print('\n---------- Generator tests finished! -----------\n')
