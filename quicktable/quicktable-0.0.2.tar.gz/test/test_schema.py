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

    def test_schema_elements_invalid_names(self):
        """Schema element names must be strings."""
        with self.assertRaisesRegex(TypeError, 'Column name must be a string.'):
            quicktable.Table([(6, 'string')])

    def test_schema_elements_some_valid_names(self):
        """Schema element names must be strings."""
        with self.assertRaisesRegex(TypeError, 'Column name must be a string.'):
            quicktable.Table([('Name', 'string'), (4, 'string')])

    def test_valid_column_types(self):
        """Correctly show valid column types."""
        self.assertEqual(('string',), quicktable.Table.COLUMN_TYPES)

    def test_schema_elements_valid_types(self):
        """Schema element types must be one of quicktable.Table.COLUMN_TYPES."""
        with self.assertRaisesRegex(TypeError, 'Column type must be one of quicktable.Table.COLUMN_TYPES.'):
            quicktable.Table([('Name', 'Foo')])

    def test_schema_elements_some_valid_types(self):
        """Schema element types must be one of quicktable.Table.COLUMN_TYPES."""
        with self.assertRaisesRegex(TypeError, 'Column type must be one of quicktable.Table.COLUMN_TYPES.'):
            quicktable.Table([('Name', 'string'), ('Age', 'Foo')])

    def test_valid_schema(self):
        """No exception is raised for a valid schema."""
        quicktable.Table([('Name', 'string'), ('Age', 'string')])

    def test_column_names(self):
        table = quicktable.Table([('Name', 'string'), ('Age', 'string')])
        self.assertEqual(('Name', 'Age'), table.column_names)

    def test_column_types(self):
        table = quicktable.Table([('Name', 'string'), ('Age', 'string')])
        self.assertEqual(('string', 'string'), table.column_types)

    def test_schema(self):
        table = quicktable.Table([('Name', 'string'), ('Age', 'string')])
        self.assertEqual([('Name', 'string'), ('Age', 'string')], table.schema)
