import unittest
import quicktable


class TestSchema(unittest.TestCase):
    def test_schema_is_sequence(self):
        """A TypeError is raised if a schema definition is not a sequence."""
        with self.assertRaisesRegex(TypeError, 'Schema definition must be a sequence.'):
            quicktable.Table(None)

    def test_schema_element_is_sequence(self):
        """A TypeError is raised if a column definition is not a sequence."""
        with self.assertRaisesRegex(TypeError, 'Column definition must be a sequence containing two items.'):
            quicktable.Table([None])

    def test_schema_element_length(self):
        """A TypeError is raised if a column definition is not length 2."""
        with self.assertRaisesRegex(TypeError, 'Column definition must be a sequence containing two items.'):
            quicktable.Table([('This', 'Has', 'Three')])

    def test_schema_elements_valid_names(self):
        """Schema element names must be strings."""
        with self.assertRaisesRegex(TypeError, 'Column name must be a string.'):
            quicktable.Table([(6, 'string')])
