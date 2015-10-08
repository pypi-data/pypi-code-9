# -*- coding: utf-8 -*-
from django.test import TestCase
from hipster_api import fields


class FiledJsonTestCase(TestCase):

    def get_value(self, obj):
        obj.to_python()
        obj.to_rules(None)
        return obj.value

    def test_field(self):
        obj = fields.JsonField(default={})

        self.assertDictEqual(self.get_value(obj), {})

        obj.setitem('asdasd')
        self.assertDictEqual(self.get_value(obj), {})

        obj.setitem('{"id": 123, "name": "Проверка"}')
        self.assertDictEqual(self.get_value(obj), {u'id': 123, u'name': u'Проверка'})

        obj.setitem('{"id": 123, "list": [1,2,3] , "name": "Проверка"}')
        self.assertDictEqual(self.get_value(obj), {u'id': 123, u'name': u'Проверка', u'list': [1, 2, 3]})

        obj.setitem('[1,2,3, "Проверка", "list"]')
        self.assertListEqual(self.get_value(obj), [1, 2, 3, u"Проверка", u"list"])

        obj.setitem('[1,2,3, "Проверка", {"name": "post"}, "list"]')
        self.assertListEqual(self.get_value(obj), [1, 2, 3, u"Проверка", {u'name': u'post'}, u"list"])
