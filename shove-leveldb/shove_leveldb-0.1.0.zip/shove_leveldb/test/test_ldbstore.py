'''shove-leveldb tests'''

from stuf.six import unittest

from shove.test.test_store import Store


class TestLevelDBStore(Store, unittest.TestCase):

    initstring = 'leveldb://test'

    def tearDown(self):
        import leveldb
        del self.store
        leveldb.DestroyDB('test')