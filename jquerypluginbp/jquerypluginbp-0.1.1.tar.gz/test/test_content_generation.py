from jquerypluginbp.core import substitute
import unittest

class TestContentGeneration(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_substitute(self):
        result = substitute('function {{plugin_name}} ( element, options )',
            {'plugin_name' : 'myawesomeplugin'})
        self.assertEqual(result, 'function myawesomeplugin ( element, options )')
