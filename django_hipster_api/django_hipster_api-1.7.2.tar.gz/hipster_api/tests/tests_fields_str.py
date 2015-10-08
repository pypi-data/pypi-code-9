# -*- coding: utf-8 -*-
from django.test import TestCase
from hipster_api import fields


class FiledStrTestCase(TestCase):

    def get_value(self, obj):
        obj.to_python()
        obj.to_rules(None)
        return obj.value

    def test_field_string(self):
        string = fields.String(default=u'', verbose_name=u'Текст')

        string.setitem('Проверка')
        self.assertEqual(self.get_value(string), 'Проверка')

        string.setitem(u'Проверка')
        self.assertEqual(self.get_value(string), u'Проверка')

        string.setitem(1)
        self.assertEqual(self.get_value(string), '1')

    def test_field_string_list(self):
        string = fields.StringList(default=u'')

        string.setitem('Проверка,строчка,field')
        self.assertListEqual(self.get_value(string), ['Проверка', 'строчка', 'field'])

        string.setitem(u'Проверка,строчка,field')
        self.assertListEqual(self.get_value(string), [u'Проверка', u'строчка', u'field'])

        string.setitem(u'')
        self.assertListEqual(self.get_value(string), [])

    def test_field_list(self):
        string = fields.FieldsListResponse(default=u'')

        string.setitem('Проверка,строчка,field, post__user__password, post__user')
        self.assertListEqual(self.get_value(string), ['Проверка', 'строчка', 'field', 'post__user'])

        string.setitem(u'Проверка,строчка,field, password')
        self.assertListEqual(self.get_value(string), [u'Проверка', u'строчка', u'field'])

        string.setitem(u'')
        self.assertListEqual(self.get_value(string), [])
