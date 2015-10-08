# -*- coding: utf-8 -*-
from django.test import TestCase
from hipster_api import fields
import datetime


class FiledDateTestCase(TestCase):

    def get_value(self, obj):
        obj.to_python()
        obj.to_rules(None)
        return obj.value

    def test_field_date(self):
        date = datetime.date.today()
        obj = fields.Date(default=date)

        self.assertEqual(self.get_value(obj), obj.default)

        obj.setitem('2015-10-02')
        self.assertEqual(self.get_value(obj), date.replace(2015, 10, 2))

        obj.setitem('02.10.2015')
        self.assertEqual(self.get_value(obj), obj.default)

        obj = fields.Date(default=date, date_format=u'%d.%m.%Y')
        obj.setitem('02.10.2015')
        self.assertEqual(self.get_value(obj), date.replace(2015, 10, 2))

    def test_field_datetime(self):
        date = datetime.datetime.now().replace(2015, 10, 8, 11, 36, 18, 0)

        obj = fields.DateTime(default=date)
        self.assertEqual(self.get_value(obj).strftime(obj.date_format), obj.default.strftime(obj.date_format))

        obj.setitem('2015-10-02 04:02:10')
        self.assertEqual(
            self.get_value(obj).strftime(obj.date_format),
            date.replace(2015, 10, 2, 4, 2, 10).strftime(obj.date_format)
        )

        obj.setitem('02.10.2015')
        self.assertEqual(self.get_value(obj).strftime(obj.date_format), obj.default.strftime(obj.date_format))

        obj = fields.DateTime(default=date, date_format=u'%d.%m.%Y %H:%M:%S')
        obj.setitem('02.10.2015 11:44:36')
        self.assertEqual(
            self.get_value(obj).strftime(obj.date_format),
            date.replace(2015, 10, 2, 11, 44, 36).strftime(obj.date_format)
        )
