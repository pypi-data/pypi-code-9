'''shove-leveldb tests'''

import gc

from stuf.six import unittest

from shove.test.test_store import Store


class TestLevelDBStore(Store, unittest.TestCase):

    initstring = 'leveldb://test'

    def tearDown(self):
        import leveldb
        del self.store
        gc.collect()
        leveldb.DestroyDB('test')