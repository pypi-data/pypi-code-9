from __future__ import unicode_literals
import unittest

from trait_documenter.tests import test_file, test_file2
from trait_documenter.tests.testing import expected_failure_when, is_python_26
from trait_documenter.tests.test_file import Dummy, dummy_function
from trait_documenter.util import get_trait_definition, DefinitionError


class TestGetTraitDefinition(unittest.TestCase):

    def test_get_simple_module_trait_definition(self):
        # given
        parent = test_file
        object_name = 'module_trait'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, 'Float')

    def test_get_inavlid_module_trait_definition(self):
        # given
        parent = test_file
        object_name = 'invalid_trait'

        # when/then
        self.assertRaises(
            DefinitionError,
            get_trait_definition,
            parent, object_name)

    @expected_failure_when(is_python_26())
    def test_get_multi_line_module_trait_definition(self):
        # given
        parent = test_file
        object_name = 'long_module_trait'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Range(low=0.2, high=34)")

    def test_get_simple_class_trait_definition(self):
        # given
        parent = Dummy
        object_name = 'trait_1'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, 'Float')

    def test_get_trait_definition_from_function(self):

        object_name = 'trait_1'

        # when/then
        self.assertRaises(
            DefinitionError,
            get_trait_definition,
            dummy_function, object_name)

    def test_get_simple_class_trait_definition_with_comments(self):
        # given
        parent = Dummy
        object_name = 'trait_4'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, 'Float')

    def test_get_multi_line_class_trait_definition(self):
        # given
        parent = Dummy
        object_name = 'trait_2'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Property(Float, depends_on='trait_1')")

    def test_get_trait_definition_over_horrible_assigment(self):
        # given
        parent = test_file2
        object_name = 'trait_1'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Event")

    def test_get_trait_definition_inside_if_block(self):
        # given
        parent = test_file2
        object_name = 'trait_2'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "List(Int)")

    def test_get_multi_line_class_trait_definition_with_comment(self):
        # given
        parent = Dummy
        object_name = 'trait_3'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Property(Float, depends_on='trait_4')")


if __name__ == '__main__':
    unittest.main()
