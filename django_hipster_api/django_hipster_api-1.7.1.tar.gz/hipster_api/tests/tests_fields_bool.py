# -*- coding: utf-8 -*-
from django.test import TestCase
from hipster_api import fields


class FiledBoolTestCase(TestCase):

    def get_value(self, obj):
        obj.to_python()
        obj.to_rules(None)
        return obj.value

    def test_field(self):
        obj = fields.Boolean(default=False)

        self.assertEqual(self.get_value(obj), obj.default)

        obj.setitem('123,2')
        self.assertEqual(self.get_value(obj), obj.default)

        obj.setitem(1)
        self.assertEqual(self.get_value(obj), True)

        obj.setitem(0)
        self.assertEqual(self.get_value(obj), False)

        obj.setitem('13')
        self.assertEqual(self.get_value(obj), True)
