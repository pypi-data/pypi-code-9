import unittest

from libsousou import module_loading


class ModuleLoadingTestCase(unittest.TestCase):

    def test_import_string_raises_importerror_on_invalid_path(self):
        # Provide an invalid module path to import_string().
        self.assertRaises(ImportError, module_loading.import_string, 'foo')

    def test_import_string_raises_importerror_on_nonexisting_path(self):
        # Provide a non existent module path to import_string().
        self.assertRaises(ImportError, module_loading.import_string, 'os.foo')


if __name__ == '__main__':
    unittest.main()
