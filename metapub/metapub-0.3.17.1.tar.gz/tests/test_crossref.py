import os, unittest

from metapub import CrossRef


TEST_CACHEDIR = 'tests/testcachedir'

class TestCrossRef(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_configurable_cachedir(self):
        '''test that `cachedir` keyword argument is fully supported in modes:

        cachedir == 'default'   <-- assumed working since other tests use this.
        cachedir is None
        cachedir is 'some/path'
        cachedir is '~/path'
        '''

        cachedir = TEST_CACHEDIR
        # start with cachedir==None; test that no cachedir is created.
        cr = CrossRef(cachedir=None)
        assert not os.path.exists(cachedir)
        assert cr._cache_path is None

        cr = CrossRef(cachedir=cachedir)
        assert os.path.exists(cachedir)
        assert cr._cache_path is not None

        os.unlink(cr._cache_path)
        os.rmdir(cachedir)

        cr = CrossRef(cachedir='~/testcachedir')
        assert os.path.exists(os.path.expanduser('~/testcachedir'))
        assert cr._cache_path is not None

        os.unlink(cr._cache_path)
        os.rmdir(os.path.expanduser('~/testcachedir'))

