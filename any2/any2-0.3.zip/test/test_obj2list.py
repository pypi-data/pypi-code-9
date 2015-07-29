# -*- encoding: utf-8 -*-
import datetime
import unittest
from decimal import Decimal
from any2 import NameTransformer
from any2 import Obj2List

quantizer = Decimal('0.01')


class SubObj(object):
    def __init__(self, v):
        self.amount = Decimal('42.4242424242')
        self.start_date = datetime.date(year=2001, month=2, day=3)
        self.description = "%s_%s" % ("Task", v)


class MyObj(object):
    def __init__(self, v, urgent):
        self.description = v
        self.urgent = urgent
        self.subobj = SubObj(v)


def quantize2(value):
    return value.quantize(quantizer)


def yesno(value):
    if value:
        return "Yes"
    else:
        return "No"


class TestObj2ListAdapter(unittest.TestCase):

    def setUp(self):
        self.quantizer = Decimal('0.01')
        vals = [
            ('Project 1', True),
            ('Project 2', False),
            ('Project 3', False),
        ]
        self.objs = [MyObj(*val) for val in vals]

    def test_001_obj2list(self):
        # the name transformer will work on output columns
        # in fact indexes...
        colnames = [
            "Start Date",
            "Amount",
            "Description",
            "Task Description",
            "Is Urgent"
        ]
        transformer = NameTransformer(colnames)
        transformer.register_func('Amount', quantize2)
        transformer.register_func('Is Urgent', yesno)

        # to adapt an object as a list we must give the list
        # of attributes we want
        attrs = [
            'subobj.start_date',
            'subobj.amount',
            'description',
            'subobj.description',
            'urgent'
        ]

        data_feed = Obj2List(self.objs, attrs, transformer=transformer)

        for index, row in enumerate(data_feed):
            if index == 0:
                assert row[0] == datetime.date(year=2001, month=2, day=3)
                # this should have been quantized
                assert row[1] == Decimal('42.42')
                assert row[4] == "Yes"

            elif index == 1:
                assert row[0] == datetime.date(year=2001, month=2, day=3)
                # this should have been quantized
                assert row[1] == Decimal('42.42')
                assert row[4] == "No"

            elif index == 2:
                assert row[0] == datetime.date(year=2001, month=2, day=3)
                # this should have been quantized
                assert row[1] == Decimal('42.42')
                assert row[4] == "No"

            else:
                assert False, "We only have 2 items in the data feed"
