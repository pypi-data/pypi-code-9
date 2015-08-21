from __future__ import unicode_literals
import unittest

import mock
from sphinx.ext.autodoc import ModuleDocumenter, SUPPRESS

from trait_documenter.module_trait_documenter import ModuleTraitDocumenter
from trait_documenter.tests import test_file
from trait_documenter.tests.testing import expected_failure_when, is_python_26
from trait_documenter.tests.test_file import Dummy


class TestModuleTraitDocumenter(unittest.TestCase):

    def test_can_document_member(self):
        can_document_member = ModuleTraitDocumenter.can_document_member
        parent = ModuleDocumenter(mock.Mock(), 'test')

        # modules
        parent.object = test_file
        self.assertFalse(can_document_member(Dummy, 'Dummy', True, parent))
        self.assertFalse(can_document_member(Dummy, 'Dummy', False, parent))
        self.assertFalse(can_document_member(
            test_file.module_trait, 'module_trait', False, parent))
        self.assertTrue(can_document_member(
            test_file.module_trait, 'module_trait', True, parent))

        # class
        parent.object = Dummy
        self.assertFalse(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', False, parent))

    def test_import_object(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), 'test')
        documenter.env.config = mock.Mock(autodoc_mock_imports=[])
        documenter.modname = 'trait_documenter.tests.test_file'
        documenter.fullname = 'trait_documenter.tests.test_file.long_module_trait'  # noqa
        documenter.objpath = ['long_module_trait']

        # when
        result = documenter.import_object()

        # then
        self.assertTrue(result)
        self.assertEqual(documenter.object_name, 'long_module_trait')
        self.assertTrue(documenter.object is not None)
        self.assertEqual(documenter.parent, test_file)

    @expected_failure_when(is_python_26())
    def test_add_directive_header(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), 'test')
        documenter.parent = test_file
        documenter.options = mock.Mock(annotation=False)
        documenter.modname = 'trait_documenter.tests.test_file'
        documenter.get_sourcename = mock.Mock(return_value='<autodoc>')
        documenter.object_name = 'long_module_trait'
        documenter.objpath = ['long_module_trait']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # then
        expected = [
            ('.. py:data:: long_module_trait', '<autodoc>'),
            ('   :noindex:', '<autodoc>'),
            ('   :module: trait_documenter.tests.test_file', '<autodoc>'),
            ('   :annotation: = Range(low=0.2, high=34)', '<autodoc>')]
        calls = documenter.add_line.call_args_list
        for index, line in enumerate(expected):
            self.assertEqual(calls[index][0], line)

    def test_add_directive_header_with_annotation(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), 'test')
        documenter.parent = test_file
        documenter.options = mock.Mock(annotation='my annotation')
        documenter.modname = 'trait_documenter.tests.test_file'
        documenter.get_sourcename = mock.Mock(return_value='<autodoc>')
        documenter.object_name = 'long_module_trait'
        documenter.objpath = ['long_module_trait']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # then
        self.assertEqual(documenter.directive.warn.call_args_list, [])
        expected = [
            ('.. py:data:: long_module_trait', '<autodoc>'),
            ('   :noindex:', '<autodoc>'),
            ('   :module: trait_documenter.tests.test_file', '<autodoc>'),
            ('   :annotation: my annotation', '<autodoc>')]
        calls = documenter.add_line.call_args_list
        for index, line in enumerate(expected):
            self.assertEqual(calls[index][0], line)

    def test_add_directive_header_with_suppress(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), 'test')
        documenter.parent = test_file
        documenter.options = mock.Mock(annotation=SUPPRESS)
        documenter.modname = 'trait_documenter.tests.test_file'
        documenter.get_sourcename = mock.Mock(return_value='<autodoc>')
        documenter.object_name = 'long_module_trait'
        documenter.objpath = ['long_module_trait']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # then
        self.assertEqual(documenter.directive.warn.call_args_list, [])
        expected = [
            ('.. py:data:: long_module_trait', '<autodoc>'),
            ('   :noindex:', '<autodoc>'),
            ('   :module: trait_documenter.tests.test_file', '<autodoc>')]
        calls = documenter.add_line.call_args_list
        for index, line in enumerate(expected):
            self.assertEqual(calls[index][0], line)

    def test_add_directive_header_with_warning(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), 'test')
        documenter.parent = test_file
        documenter.options = mock.Mock(annotation=False)
        documenter.modname = 'trait_documenter.tests.test_file'
        documenter.get_sourcename = mock.Mock(return_value='<autodoc>')
        documenter.object_name = 'long_invalid_trait'
        documenter.objpath = ['long_module_trait']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # the
        self.assertEqual(documenter.directive.warn.call_count, 1)
        expected = [
            ('.. py:data:: long_module_trait', '<autodoc>'),
            ('   :noindex:', '<autodoc>'),
            ('   :module: trait_documenter.tests.test_file', '<autodoc>')]
        calls = documenter.add_line.call_args_list
        for index, line in enumerate(expected):
            self.assertEqual(calls[index][0], line)


if __name__ == '__main__':
    unittest.main()
