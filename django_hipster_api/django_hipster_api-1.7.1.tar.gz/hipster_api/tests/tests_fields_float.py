# -*- coding: utf-8 -*-
from django.test import TestCase
from hipster_api import fields


class FiledFloatTestCase(TestCase):

    def get_value(self, obj):
        obj.to_python()
        obj.to_rules(None)
        return obj.value

    def test_field(self):
        obj = fields.Float(default=0.0)

        self.assertEqual(self.get_value(obj), 0.0)

        obj.setitem('123,2')
        self.assertEqual(self.get_value(obj), 123.2)

        obj.setitem('12326')
        self.assertEqual(self.get_value(obj), 12326.0)

        obj.setitem('12d326')
        self.assertEqual(self.get_value(obj), 0.0)

    def test_field_less(self):
        obj = fields.FloatLess(default=0.1, less=5)

        obj.setitem('123')
        self.assertEqual(self.get_value(obj), obj.default)

        obj.setitem(2)
        self.assertEqual(self.get_value(obj), 2.0)

        obj.setitem(-23)
        self.assertEqual(self.get_value(obj), -23.0)

        obj.setitem('asd123')
        self.assertEqual(self.get_value(obj), obj.default)

    def test_field_larger(self):
        obj = fields.FloatLarger(default=0.6, larger=5)

        obj.setitem('123')
        self.assertEqual(self.get_value(obj), 123.0)

        obj.setitem(2)
        self.assertEqual(self.get_value(obj), obj.default)

        obj.setitem(-23)
        self.assertEqual(self.get_value(obj), obj.default)

        obj.setitem('asd123')
        self.assertEqual(self.get_value(obj), obj.default)

    def test_field_list(self):
        obj = fields.FloatList(default='')

        self.assertListEqual(self.get_value(obj), [])

        obj.setitem('123.3,2,6')
        self.assertListEqual(self.get_value(obj), [123.3, 2.0, 6.0])

        obj.setitem('123, asdf, 2,6')
        self.assertListEqual(self.get_value(obj), [])
