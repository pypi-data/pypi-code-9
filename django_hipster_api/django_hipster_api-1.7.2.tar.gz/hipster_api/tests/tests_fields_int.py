# -*- coding: utf-8 -*-
from django.test import TestCase
from hipster_api import fields


class FiledIntTestCase(TestCase):

    def get_value(self, obj):
        obj.to_python()
        obj.to_rules(None)
        return obj.value

    def test_field_int(self):
        obj = fields.Integer(default=0)

        obj.setitem('123')
        self.assertEqual(self.get_value(obj), 123)

        obj.setitem(1234)
        self.assertEqual(self.get_value(obj), 1234)

        obj.setitem(-23)
        self.assertEqual(self.get_value(obj), -23)

        obj.setitem('asd123')
        self.assertEqual(self.get_value(obj), 0)

    def test_field_int_less(self):
        obj = fields.IntegerLess(default=0, less=5)

        obj.setitem('123')
        self.assertEqual(self.get_value(obj), 0)

        obj.setitem(2)
        self.assertEqual(self.get_value(obj), 2)

        obj.setitem(-23)
        self.assertEqual(self.get_value(obj), -23)

        obj.setitem('asd123')
        self.assertEqual(self.get_value(obj), 0)

    def test_field_int_larger(self):
        obj = fields.IntegerLarger(default=0, larger=5)

        obj.setitem('123')
        self.assertEqual(self.get_value(obj), 123)

        obj.setitem(2)
        self.assertEqual(self.get_value(obj), 0)

        obj.setitem(-23)
        self.assertEqual(self.get_value(obj), 0)

        obj.setitem('asd123')
        self.assertEqual(self.get_value(obj), 0)

    def test_field_int_list(self):
        obj = fields.IntegerList(default='')

        self.assertListEqual(self.get_value(obj), [])

        obj.setitem('123,2,6')
        self.assertListEqual(self.get_value(obj), [123, 2, 6])

        obj.setitem('123, asdf, 2,6')
        self.assertListEqual(self.get_value(obj), [])
