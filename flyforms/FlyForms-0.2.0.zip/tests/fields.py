# coding=utf-8
from __future__ import print_function
from unittest import TestCase
from sys import version_info
import random

from flyforms.fields import *
from flyforms.fields import Field
from flyforms.validators import ValidationError
from flyforms import UNSET


# noinspection PyUnresolvedReferences
class MixinTestField(object):
    field_cls = Field
    valid_values = []
    invalid_values = []

    def test(self):
        field = self.field_cls()
        for vv in self.valid_values:
            self.assertEqual(field.is_valid(vv), True)
            field.validate(vv)
        for iv in self.invalid_values:
            self.assertEqual(field.is_valid(iv), False)
            with self.assertRaises(ValidationError):
                field.validate(iv)

    def test_choices(self):
        field = self.field_cls(choices=self.valid_values)
        self.assertEqual(field.is_valid(random.choice(self.valid_values)), True)
        field.validate(random.choice(self.valid_values))

        self.assertEqual(field.is_valid(random.choice(self.invalid_values)), False)


class BaseTestField(TestCase):

    def test_required(self):
        if version_info[0] == 3 and version_info[1] >= 3:
            # noinspection PyUnresolvedReferences
            with self.assertWarns(RuntimeWarning):
                IntField(default=5)
        field_required = Field()
        with self.assertRaises(ValidationError):
            field_required.validate(UNSET)

        field_not_required = Field(required=False)
        field_not_required.validate(UNSET)

    def test_fields_init_args(self):
        with self.assertRaises(TypeError):
            StringField(required=False, default=None)
        IntField(choices=[0, 10, 100, None])
        with self.assertRaises(TypeError):
            StringField(choices=["", None])
        with self.assertRaises(TypeError):
            FloatField(choices=None)
        with self.assertRaises(TypeError):
            FloatField(validators=(object(),))


class TestStringField(TestCase, MixinTestField):
    field_cls = StringField
    valid_values = ["", " ", u" ", u"qwerty", "Hello world!"]
    invalid_values = [None, object(), 0.25, 15, UNSET]

    def test_regex(self):
        field = self.field_cls(regex=r"^[A-Z].*$")
        self.check(field)

    def test_validators_add(self):
        from flyforms.validators import RegexValidator
        field = self.field_cls(
            min_length=1,
            max_length=10,
            validators=RegexValidator(regex=r"^[A-Z].*$"))
        self.check(field)

    def check(self, field):
        for vv in ["A__", "W", "WWW"]:
            self.assertEqual(field.is_valid(vv), True)
            field.validate(vv)
        for iv in ["_AAA", "", "aaa"]:
            self.assertEqual(field.is_valid(iv), False)
            with self.assertRaises(ValidationError):
                field.validate(iv)


class TestEmailField(TestCase, MixinTestField):
    field_cls = EmailField
    valid_values = ["qwerty@gmail.com", "John@Smith.ua"]
    invalid_values = [None, UNSET, "@gmail.com", "qwerty@gmail,com", "qwerty_gmail.com"]


class TestIntField(TestCase, MixinTestField):
    field_cls = IntField
    valid_values = [0, 10, -50, None]
    invalid_values = [0.1, object(), UNSET]

    def test_attrs(self):
        IntField(min_value=0, max_value=2).is_valid(1)
        IntField(min_value=0).is_valid(1)
        IntField(max_value=5).is_valid(3)


class TestFloatField(TestCase, MixinTestField):
    field_cls = FloatField
    valid_values = [0.0, 10.1, -100500.0, None]
    invalid_values = [0, UNSET, object()]

    def test_attrs(self):
        FloatField(min_value=0.0, max_value=0.1).is_valid(0.05)
        with self.assertRaises(ValidationError):
            FloatField(min_value=0.0).validate(-0.05)


class TestIp4Field(TestCase, MixinTestField):
    field_cls = Ip4Field
    valid_values = ["127.0.0.1", "192.188.1.1"]
    invalid_values = [UNSET, "1270.0.1", "192.1881.1", None, object()]


class TestBoolField(TestCase, MixinTestField):

    class BClass(object):
        def __nonzero__(self):
            return False

    field_cls = BooleanField
    valid_values = [True, False, None]
    invalid_values = [0, UNSET, 100500.2, BClass()]
