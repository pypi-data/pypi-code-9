'''shove_lmdb tests'''

from stuf.six import unittest

from shove.test.test_store import Store


class TestLMDBStore(Store, unittest.TestCase):

    initstring = 'lmdb://test'

    def tearDown(self):
        self.store.close()
        from shutil import rmtree
        rmtree('test')