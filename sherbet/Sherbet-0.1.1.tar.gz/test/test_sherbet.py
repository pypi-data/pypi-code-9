import unittest

from sherbet import _parse_expression, _parse_format, _analyse, sweeten

class TestSherbet(unittest.TestCase):
    def assertExpressions(self, sample, expected, msg=None):
        def get_optional_fields(item, names):
            names = iter(names[::-1])
            for name in names:
                try:
                    value = getattr(item, name)
                except AttributeError:
                    continue
                else:
                    break
            else:
                return tuple()

            fields = (value,)
            for name in names:
                value = getattr(item, name, None)
                fields = (value,) + fields 

            return fields

        def expression_mapper(item):
            fields = (item.expression, item.positions)
            optional_fields = get_optional_fields(item, ['name', 'value',
                                                         'plural_expression',
                                                         'plural_options',
                                                         'plural_subject'])
            if optional_fields is None:
                return fields

            return fields + optional_fields

        def expressions_mapper(item):
            expression, item = item
            return expression, expression_mapper(item)

        self.assertEqual(dict(map(expressions_mapper, sample.iteritems())),
                         expected, msg)

    def test__parse_expression_no_match(self):
        self.assertEqual(_parse_expression('x_suffix<s>'), (None, None))
        self.assertEqual(_parse_expression('_plural<s>'), (None, None))
        self.assertEqual(_parse_expression('x_plural<>'), (None, None))
        self.assertEqual(_parse_expression('x_plural<s>>'), (None, None))

    def test__parse_expression_default(self):
        self.assertEqual(_parse_expression('x_plural'), ('x', ['s']))

    def test__parse_expression_single(self):
        self.assertEqual(_parse_expression('x_plural<es>'), ('x', ['es']))

    def test__parse_expression_multiple(self):
        self.assertEqual(_parse_expression('x_plural<s|ve>'),
                         ('x', ['s', 've']))

    def test__parse_format(self):
        sequence, expressions = \
            _parse_format('XXX: {x}, YYY: {y}, ZZZ: {z}, N: {}, TTT: {x}, ' \
                          'M: {}, END',
                          ('test',), {'x': 1, 'y': 2})

        self.assertEqual(sequence,
                         ['XXX: ', None,
                          ', YYY: ', None,
                          ', ZZZ: ', None,
                          ', N: ', None,
                          ', TTT: ', None,
                          ', M: ', None,
                          ', END'])

        self.assertExpressions(expressions,
                               {'0': ('0', {7: ('', None)}, 0L, 'test'),
                                '1': ('1', {11: ('', None)}),
                                'x': ('x', {1: ('', None),
                                            9: ('', None)}, 'x', 1),
                                'y': ('y', {3: ('', None)}, 'y', 2),
                                'z': ('z', {5: ('', None)})})

    def test__analyse(self):
        sequence, expressions = \
            _parse_format('XXX: {x}, YYY: {y}, N: {}, ZZZ: {z}, TTT: {x}, ' \
                          '{x_plural}, {z_plural}, {0_plural}, END',
                          tuple(), {'x': 1, 'y': 2})

        x = expressions['x']

        _analyse(expressions)
        self.assertExpressions(expressions,
                               {'x': ('x', {1: ('', None),
                                            9: ('', None)}, 'x', 1),
                                'y': ('y', {3: ('', None)}, 'y', 2),
                                '0': ('0', {5: ('', None)}),
                                'z': ('z', {7: ('', None)}),
                                'x_plural': ('x_plural', {11: ('', None)},
                                             None, None, 'x', ['s'], x),
                                'z_plural': ('z_plural', {13: ('', None)},
                                             None, None, 'z', ['s']),
                                '0_plural': ('0_plural', {15: ('', None)},
                                             None, None, '0', ['s'])})

    def test_sweeten(self):
        self.assertEqual(sweeten('Found {x} file{x_plural}.', x=1),
                         'Found 1 file.')
        self.assertEqual(sweeten('Found {x} file{x_plural}.', x=5),
                         'Found 5 files.')

test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSherbet)

if __name__ == '__main__':
    unittest.main()
