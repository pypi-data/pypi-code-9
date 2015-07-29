# -*- encoding: utf-8 -*-
import unittest
import six
from any2 import recursive_getattr
from decimal import Decimal
from any2 import Listlike2List
from any2 import DictAdapter
from any2 import TypeTransformer
from any2 import IndexTransformer
from any2 import NameTransformer
from any2 import TransformationError
from any2 import ColumnMappingError
from any2 import Any2Base


class Foo(object):
    def __init__(self, value):
        self.field1 = 'foo1_%s' % value
        self.field2 = 'foo2_%s' % value


class Bar(object):
    def __init__(self, value):
        self.field1 = 'bar1_%s' % value
        self.field2 = 'bar2_%s' % value
        self.foo = Foo(value)


class Dummy(object):
    def __init__(self, value):
        self.field1 = 'dummy1_%s' % value
        self.field2 = 'dummy2_%s' % value
        self.bar = Bar(value)


class TestRecursiveGetter(unittest.TestCase):

    def test_001_firstlevel_field(self):
        dummy = Dummy('r1')
        res1 = recursive_getattr(dummy, 'field1')
        res2 = recursive_getattr(dummy, 'field2')

        assert res1 == 'dummy1_r1'
        assert res2 == 'dummy2_r1'

    def test_002_secondlevel_field(self):
        dummy = Dummy('r2')
        res1 = recursive_getattr(dummy, 'bar.field1')
        res2 = recursive_getattr(dummy, 'bar.field2')

        assert res1 == 'bar1_r2'
        assert res2 == 'bar2_r2'

    def test_003_thirdlevel_field(self):
        dummy = Dummy('r3')
        res1 = recursive_getattr(dummy, 'bar.foo.field1')
        res2 = recursive_getattr(dummy, 'bar.foo.field2')

        assert res1 == 'foo1_r3'
        assert res2 == 'foo2_r3'

    def test_004_missing_field_wdot(self):
        dummy = Dummy('r3')
        res1 = recursive_getattr(dummy, 'bar.foo.field1')
        res2 = recursive_getattr(dummy, 'bar.foo.XX.field2', default_value=42)

        assert res1 == 'foo1_r3'
        assert res2 == 42

    def test_004_missing_field_wodot(self):
        dummy = Dummy('r3')
        res1 = recursive_getattr(dummy, 'bar.foo.field1')
        res2 = recursive_getattr(dummy, 'XX', default_value=56)

        assert res1 == 'foo1_r3'
        assert res2 == 56


class MyObj(object):
    def __init__(self, row, names):
        self.row = row
        self.names = names

    def __iter__(self):
        for name in self.names:
            yield self.row[name]


class TestTransformersandList(unittest.TestCase):

    def setUp(self):
        self.row_iter = [
            {
                'name': u'Noël',
                'amount': Decimal('12.544'),
                'amount2': Decimal('12.544'),
                'go': True
            },
            {
                'name': u'Pentecôte',
                'amount': Decimal('145.233'),
                'amount2': Decimal('145.233'),
                'go': False
            },
        ]
        self.colnames = ['name', 'amount', 'amount2', 'go']
        self.objlist = [
            MyObj(row, self.colnames) for row in self.row_iter
        ]

    def test_001_listadapter(self):
        data = Listlike2List(self.objlist)
        for row in data:
            assert isinstance(row, list)

    def test_002_typetransformer(self):
        def bool2str(value):
            if value:
                return "Vrai"
            else:
                return "Faux"

        transformer = TypeTransformer()
        transformer.register_func(bool, bool2str)
        data = Listlike2List(self.objlist, transformer=transformer)

        for i, row in enumerate(data):
            if i == 0:
                assert row[3] == "Vrai"
            elif i == 1:
                assert row[3] == "Faux"

    def test_003_indextransformer(self):
        """in this test we ensure that the type is no more the criterion.
        Instead this is the index that determines which function is applied to
        your data
        """
        q1 = Decimal('0.1')
        q2 = Decimal('0.01')

        def quantize2(value):
            return value.quantize(q2)

        def quantize1(value):
            return value.quantize(q1)

        transformer = IndexTransformer()
        transformer.register_func(1, quantize1)
        transformer.register_func(2, quantize2)
        data = Listlike2List(self.objlist, transformer=transformer)

        for i, row in enumerate(data):
            if i == 0:
                assert row[1] == Decimal("12.5")
                assert row[2] == Decimal("12.54")
            elif i == 1:
                assert row[1] == Decimal("145.2")
                assert row[2] == Decimal("145.23")

    def test_004_indextransformer_raises(self):
        q1 = Decimal('0.1')
        q2 = Decimal('0.01')

        def quantize2(value):
            return value.quantize(q2)

        def quantize1(value):
            return value.quantize(q1)

        transformer = IndexTransformer()
        transformer.register_func(1, quantize1)
        transformer.register_func(2, quantize2)
        data = Listlike2List(self.objlist, transformer=transformer)
        for row in data:
            for item in row:
                if isinstance(item, bool):
                    # omitting the index will raise
                    with self.assertRaises(TransformationError):
                        transformer.apply(item)

    def test_005_nametransformer(self):
        """we now use the name as a criterion to choose the function to apply
        """
        q1 = Decimal('0.1')
        q2 = Decimal('0.01')

        def quantize2(value):
            return value.quantize(q2)

        def quantize1(value):
            return value.quantize(q1)

        transformer = NameTransformer(self.colnames)
        transformer.register_func('amount', quantize1)
        transformer.register_func('amount2', quantize2)
        data = Listlike2List(self.objlist, transformer=transformer)

        for i, row in enumerate(data):
            if i == 0:
                assert row[1] == Decimal("12.5")
                assert row[2] == Decimal("12.54")
            elif i == 1:
                assert row[1] == Decimal("145.2")
                assert row[2] == Decimal("145.23")

    def test_006_nametransformerraises(self):
        q1 = Decimal('0.1')

        def quantize1(value):
            return value.quantize(q1)

        transformer = NameTransformer(self.colnames)
        # the name we are trying to bind a function to does not exist in the
        # names we gave to the constuctor... this should raise
        with self.assertRaises(ColumnMappingError):
            transformer.register_func('amountXX', quantize1)


class MyObj4Dict(object):
    """anonymous object used for our tests with the DictAdapter
    """
    pass


class TestDictAdapter(unittest.TestCase):

    def setUp(self):
        subobj1 = MyObj4Dict()
        subobj1.val1 = 42
        subobj2 = MyObj4Dict()
        subobj2.val1 = 24

        values = [
            {
                'name': u'Noël',
                'name_under': u'py_NewNoël',
                'amount': Decimal('212.576'),
                'amount2': Decimal('212.576'),
                'subobj': subobj1,
                'go': True
            },
            {
                'name': u'Pentecôte',
                'name_under': u'py_NewPentecôte',
                'amount': Decimal('45.266'),
                'amount2': Decimal('45.266'),
                'subobj': subobj2,
                'go': False
            },
        ]
        self.objlist = []
        for item in values:
            obj = MyObj4Dict()
            for k in item:
                setattr(obj, k, item[k])
            self.objlist.append(obj)

    def test_001_objisdict(self):
        column_mappings = [
            {'attr': 'amount', 'colname': 'Amount'},
            {'attr': 'name', 'colname': 'Name'},
            {'attr': 'go', 'colname': 'Will Go'},
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            if i == 0:
                assert adaptedasdict.get('Amount', None) == Decimal('212.576')
                assert adaptedasdict.get('Name', None) == u'Noël'
                assert adaptedasdict.get('Will Go', None) is True

            elif i == 1:
                assert adaptedasdict.get('Amount', None) == Decimal('45.266')
                assert adaptedasdict.get('Name', None) == u'Pentecôte'
                assert adaptedasdict.get('Will Go', None) is False

            else:
                assert False

    def test_002_iter_only_on_known_keys(self):
        column_mappings = [
            {'attr': 'amount', 'colname': 'Amount'},
            {'attr': 'name', 'colname': 'Name'},
            {'attr': 'go', 'colname': 'Will Go'},
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            keys1 = [k for k in adaptedasdict]
            keys2 = adaptedasdict.keys()
            # attributes not in the mapping are not itered
            assert set(keys1) == set(['Amount', 'Name', 'Will Go'])
            assert set(keys2) == set(['Amount', 'Name', 'Will Go'])

    def test_003_dictadpater_with_callable_renderer(self):

        def renderer_name(value):
            return value.split('_')[1]

        def renderer_amount(value):
            return '%s' % value

        column_mappings = [
            {
                'attr': 'name_under',
                'colname': 'Name',
                'renderer': renderer_name,
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': renderer_amount,
            },
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            if i == 0:
                assert adaptedasdict.get('Val1 of subobj', None) == '42'
                if six.PY2:
                    assert adaptedasdict.get('Name', None) == u'NewNoël'
                else:
                    assert adaptedasdict.get('Name', None) == 'NewNoël'

            elif i == 1:
                assert adaptedasdict.get('Val1 of subobj', None) == '24'
                if six.PY2:
                    assert adaptedasdict.get('Name', None) == u'NewPentecôte'
                else:
                    assert adaptedasdict.get('Name', None) == 'NewPentecôte'

            else:
                assert False

    def test_004_dictadpater_with_string_renderer(self):

        column_mappings = [
            {
                'attr': 'name_under',
                'colname': 'Name',
                'renderer': "Hard Coded Name",
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': "Hard Coded Val1",
            },
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            assert adaptedasdict.get('Val1 of subobj', None) == (
                "Hard Coded Val1"
            )
            assert adaptedasdict.get('Name', None) == (
                "Hard Coded Name"
            )

    def test_005_dictadpater_with_invalid_renderer_raises(self):

        column_mappings = [
            {
                'attr': 'name_under',
                'colname': 'Name',
                'renderer': Decimal("42"),
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': "Hard Coded Val1",
            },
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            assert adaptedasdict.get('Val1 of subobj', None) == (
                "Hard Coded Val1"
            )
            with self.assertRaises(ColumnMappingError):
                # accessing this particular column will raise
                # if you want to avoid this use any2.Any2Base to check your
                # column mappings
                adaptedasdict.get('Name', None)

    def test_006_dictadpater_missing_attr(self):

        column_mappings = [
            {
                'attr': 'some.missing.attr',
                'colname': 'Name',
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': "Hard Coded Val1",
            },
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            assert adaptedasdict.get('Name', "default") == "default"

    def test_007_dictadpater_attr_isnot_inmapping(self):
        """if the mapping does not include the attr for a colname, then the
        adapter will return an empty string...
        """

        column_mappings = [
            {
                'colname': 'Name',
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': "Hard Coded Val1",
            },
        ]

        for i, item in enumerate(self.objlist):
            adaptedasdict = DictAdapter(item, column_mappings, 'utf-8')
            assert adaptedasdict.get('Name', "default") == u''


class TestBase(unittest.TestCase):

    def renderer_name(self, value):
        return value.split('_')[1]

    def renderer_amount(self, value):
        return '%s' % value

    def test_001_instanciation(self):
        column_mappings = [
            {
                'attr': 'name_under',
                'colname': 'Name',
                'renderer': self.renderer_name,
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': self.renderer_amount,
            },
        ]

        base = Any2Base(
            'targetfilename',
            column_mappings=column_mappings,
            show_first_line=False
        )
        assert base.target_filename == "targetfilename"

    def test_002_invalid_mapping_missing_colname(self):
        """colname is a mandatory field in the column mapping
        """
        column_mappings = [
            {
                'attr': 'name_under',
                'renderer': self.renderer_name,
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': self.renderer_amount,
            },
        ]

        with self.assertRaises(ColumnMappingError):
            base = Any2Base(
                'targetfilename',
                column_mappings=column_mappings,
            )

    def test_003_invalid_renderertype(self):
        """renderer should be stringtype or callable
        """
        column_mappings = [
            {
                'attr': 'name_under',
                'colname': 'Name',
                'renderer': Decimal('10.24'),
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': self.renderer_amount,
            },
        ]

        with self.assertRaises(ColumnMappingError):
            base = Any2Base(
                'targetfilename',
                column_mappings=column_mappings,
                show_first_line=False
            )

    def test_004_renderer_or_attr_should_be_present(self):
        """column mapping needs either attr or renderer
        """
        column_mappings = [
            {
                'colname': 'Name',
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': self.renderer_amount,
            },
        ]

        with self.assertRaises(ColumnMappingError):
            base = Any2Base(
                'targetfilename',
                column_mappings=column_mappings,
                show_first_line=False
            )

    def test_005_renderer_callable_needs_attr(self):
        """a callable renderer needs an attr to work on
        """
        column_mappings = [
            {
                'colname': 'Name',
                'renderer': self.renderer_name,
            },
            {
                'attr': 'subobj.val1',
                'colname': 'Val1 of subobj',
                'renderer': self.renderer_amount,
            },
        ]

        with self.assertRaises(ColumnMappingError):
            base = Any2Base(
                'targetfilename',
                column_mappings=column_mappings,
                show_first_line=False
            )
