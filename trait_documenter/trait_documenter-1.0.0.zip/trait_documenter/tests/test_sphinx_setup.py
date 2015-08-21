import unittest

import mock

from trait_documenter import setup
from trait_documenter.class_trait_documenter import ClassTraitDocumenter
from trait_documenter.module_trait_documenter import ModuleTraitDocumenter


class TestSphinxSetup(unittest.TestCase):

    def test_setup(self):
        app = mock.Mock()
        setup(app)
        expected = app.add_autodocumenter.call_args_list
        calls = [
            mock.call(ModuleTraitDocumenter), mock.call(ClassTraitDocumenter)]
        self.assertEqual(expected, calls)

if __name__ == '__main__':
    unittest.main()
