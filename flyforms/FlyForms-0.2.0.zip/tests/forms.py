# coding=utf-8
from unittest import TestCase

from flyforms import *


class TestForms(TestCase):

    def test(self):

        class GrandPa(Form):
            field1 = StringField()

        class Pa(GrandPa):
            field2 = BooleanField()

        class Son(Pa):
            field3 = FloatField()

        class Child(Son):
            field4 = BooleanField(required=False)
            field5 = IntField(required=False, default=100500)

        data = {
            "field1": "Hello world!",
            "field2": False,
            "field3": 2.5
        }

        vf = Son(**data)

        self.assertEqual(vf.is_bound, True)
        self.assertEqual(vf.is_valid, True)
        self.assertEqual(vf.errors, {})
        self.assertEqual(len(vf._fields), 3)
        self.assertEqual(len(vf.data), 3)
        self.assertEqual(validate_schema(Son, **data), True)

        data["field4"] = False

        iv = Son(**data)

        self.assertEqual(iv.is_bound, True)
        self.assertEqual(iv.is_valid, False)
        self.assertEqual(len(iv.errors), 1)
        self.assertEqual(validate_schema(Son, **data), False)

        f = Child(**data)

        self.assertEqual(f.field4, False)
        self.assertEqual(f.field5, 100500)
        self.assertEqual(f.is_bound, True)
        self.assertEqual(f.is_valid, True)
        self.assertEqual(validate_schema(Child, **data), True)
