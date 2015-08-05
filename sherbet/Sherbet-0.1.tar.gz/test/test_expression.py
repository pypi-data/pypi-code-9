import unittest

from sherbet import _Expression

class TestExpression(unittest.TestCase):
    def test_expression_init(self):
        expression = _Expression('x', 0, '', None, tuple(), {})
        self.assertEqual(expression.expression, 'x')
        self.assertEqual(expression.positions, {0: ('', None)})
        self.assertFalse(hasattr(expression, 'name'))
        self.assertFalse(hasattr(expression, 'value'))

    def test_expression_init_with_value(self):
        expression = _Expression('0', 0, '', None, ('test',), {})
        self.assertEqual(expression.expression, '0')
        self.assertEqual(expression.positions, {0: ('', None)})
        self.assertTrue(hasattr(expression, 'name'))
        self.assertEqual(expression.name, 0)
        self.assertTrue(hasattr(expression, 'value'))
        self.assertEqual(expression.value, 'test')

    def test_expression_add_position(self):
        expression = _Expression('x', 0, '', None, tuple(), {})
        self.assertEqual(expression.positions, {0: ('', None)})

        expression.add_position(1, 'd', 's')
        self.assertEqual(expression.positions, {0: ('', None),
                                                1: ('d', 's')})

    def test_expression_try_set_plural_with_value(self):
        expression = _Expression('x_plural', 0, '', None,
                                 tuple(), {'x_plural': 'test'})
        self.assertFalse(expression.try_set_plural())

    def test_expression_try_set_plural_no_match(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': 'test'})
        self.assertFalse(expression.try_set_plural())

    def test_expression_try_set_plural(self):
        expression = _Expression('x_plural<s|ve>', 0, '', None, tuple(), {})
        self.assertTrue(expression.try_set_plural())
        self.assertTrue(hasattr(expression, 'plural_expression'))
        self.assertEqual(expression.plural_expression, 'x')
        self.assertTrue(hasattr(expression, 'plural_options'))
        self.assertEqual(expression.plural_options, ['s', 've'])

    def test_expression_assign_subject_no_subject(self):
        plural = _Expression('x_plural<s|ve>', 0, '', None, tuple(), {})
        plural.try_set_plural()
        expression = _Expression('y', 0, '', None, tuple(), {'y': 'test'})
        expressions = {expression.expression: expression}

        plural.assign_subject(expressions)
        self.assertFalse(hasattr(plural, 'plural_subject'))

    def test_expression_assign_subject_no_value(self):
        plural = _Expression('x_plural<s|ve>', 0, '', None, tuple(), {})
        plural.try_set_plural()
        expression = _Expression('x', 0, '', None, tuple(), {})
        expressions = {expression.expression: expression}

        plural.assign_subject(expressions)
        self.assertFalse(hasattr(plural, 'plural_subject'))

    def test_expression_assign_subject_wrong_type(self):
        plural = _Expression('x_plural<s|ve>', 0, '', None, tuple(), {})
        plural.try_set_plural()
        expression = _Expression('x', 0, '', None, tuple(), {'x': 'test'})
        expressions = {expression.expression: expression}

        plural.assign_subject(expressions)
        self.assertFalse(hasattr(plural, 'plural_subject'))

    def test_expression_assign_subject(self):
        plural = _Expression('x_plural<s|ve>', 0, '', None, tuple(), {})
        plural.try_set_plural()
        expression = _Expression('x', 0, '', None, tuple(), {'x': 0})
        expressions = {expression.expression: expression}

        plural.assign_subject(expressions)
        self.assertTrue(hasattr(plural, 'plural_subject'))
        self.assertEqual(plural.plural_subject, expression)

    def test_expression_restore_field(self):
        expression = _Expression('x', 0, 'd', 's', tuple(), {})
        self.assertEqual(expression.restore_field(0), '{x!s:d}')

    def test_expression_format_standard(self):
        expression = _Expression('x', 0, '>10s', 'r', tuple(), {})
        self.assertEqual(expression.format_standard('test', 0), '    \'test\'')

    def test_expression_format_standard_no_conversion(self):
        expression = _Expression('x', 0, '>10s', None, tuple(), {})
        self.assertEqual(expression.format_standard('test', 0), '      test')

    def test_expression_format_standard_wrong_conversion(self):
        expression = _Expression('x', 0, '', 'z', tuple(), {})
        self.assertEqual(expression.format_standard('test', 0), '{x!z}')

    def test_expression_format_standard_wrong_format(self):
        expression = _Expression('x', 0, ' 10s', None, tuple(), {})
        self.assertEqual(expression.format_standard('test', 0), '{x: 10s}')

    def test_expression_format_list(self):
        expression = _Expression('x', 0, '', None, tuple(), {})
        self.assertEqual(expression.format_list(['xxx', 'yyy', 'zzz'], 0),
                         '"xxx", "yyy" and "zzz"')

    def test_expression_format_list_repr_conversion(self):
        expression = _Expression('x', 0, '', 'r', tuple(), {})
        self.assertEqual(expression.format_list(['xxx', 'yyy', 'zzz'], 0),
                         '[\'xxx\', \'yyy\', \'zzz\']')

    def test_expression_format_list_of_different_types(self):
        class A(object):
            pass

        first_item = 5
        second_item = 'test'
        third_item = {1: 'a', 2: 'b', 3: 'c'}
        forth_item = A
        fifth_itme = A()

        expression = _Expression('x', 0, '', None, tuple(), {})
        value = [first_item, second_item, third_item, forth_item, fifth_itme]
        self.assertEqual(expression.format_list(value, 0),
                         '"5", "test", "{1: \'a\', 2: \'b\', 3: \'c\'}", ' \
                         '"%s" and "%s"' % (str(forth_item), str(fifth_itme)))

    def test_expression_format_list_single_item(self):
        expression = _Expression('x', 0, '', None, tuple(), {})
        self.assertEqual(expression.format_list(['test'], 0), 'test')

    def test_expression_format_list_wrong_format(self):
        expression = _Expression('x', 0, '=10s', None, tuple(), {})
        self.assertEqual(expression.format_list(['test'], 0), '{x:=10s}') 

    def test_expression_format_plural(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': 1})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural', 1, '', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(plural.format_plural(1), '')

    def test_expression_format_plural_zero(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': 0})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural', 1, '', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(plural.format_plural(1), 's')

    def test_expression_format_plural_choice(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': 1})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural<ve|s>', 1, '', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(plural.format_plural(1), 's')

    def test_expression_format_plural_list(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': [1, 2, 3]})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural<ve|s>', 1, '', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(plural.format_plural(1), 've')

    def test_expression_format_plural_wrong_format(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': 1})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural<ve|s>', 1, '=10s', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(plural.format_plural(1), '{x_plural<ve|s>:=10s}')

    def test_expression_format_field(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': 1})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural<ve|s>', 1, '', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(expression.format_field(0), '1')
        self.assertEqual(plural.format_field(1), 's')

    def test_expression_format_field_list(self):
        expression = _Expression('x', 0, '', None, tuple(), {'x': [1, 2, 3]})
        expressions = {expression.expression: expression}

        plural = _Expression('x_plural<ve|s>', 1, '', None, tuple(), {})
        plural.try_set_plural()
        plural.assign_subject(expressions)

        self.assertEqual(expression.format_field(0), '"1", "2" and "3"')

    def test_expression_format_field_plural_no_subject(self):
        plural = _Expression('x_plural<ve|s>', 0, '', None, tuple(), {})
        plural.try_set_plural()

        self.assertEqual(plural.format_field(0), '{x_plural<ve|s>}')

    def test_expression_substitute(self):
        expressions = {}

        expression = _Expression('x', 0, '', None, tuple(), {'x': 1})
        expression.add_position(2, '', None)
        expressions[expression.expression] = expression

        expression = _Expression('y', 1, '', None, tuple(), {'y': 'test'})
        expression.add_position(3, '', None)
        expressions[expression.expression] = expression

        sequence = 4*[None]

        expressions['x'].substitute(sequence)
        self.assertEqual(sequence, ['1', None, '1', None])

        expressions['y'].substitute(sequence)
        self.assertEqual(sequence, ['1', 'test', '1', 'test'])

test_suite = unittest.TestSuite((TestExpression('test_expression_init'),))

if __name__ == '__main__':
    unittest.main()

