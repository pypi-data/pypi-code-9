# coding=utf-8
from unittest import TestCase

from flyforms.validators import *
from flyforms.common import UNSET


# Cool mixin class for Validators testing =)
# noinspection PyUnresolvedReferences
class ValidatorTestMixin(object):
    validator = object()

    valid_values = []
    invalid_values = []

    def test_validator(self):
        for vv in self.valid_values:
            self.validator.validate(vv)
            self.assertEqual(self.validator.is_valid(vv), True)
        for iv in self.invalid_values:
            with self.assertRaises(ValidationError):
                self.validator.validate(iv)
            self.assertEqual(self.validator.is_valid(iv), False)


class LenImplementer(object):

    def __init__(self, length):
        self.length = length

    def __len__(self):
        return self.length


# Test cases
class TestEntryValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.valid_values = [0, "qwerty", None, "#$_"]
        self.validator = EntryValidator(self.valid_values)
        self.invalid_values = [1, "Hello!", object()]


class TestMaxValueValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.validator = MaxValueValidator(10)
        self.valid_values = [0, 9.99, -100, -500]
        self.invalid_values = [10.0001, 100]


class TestMinValueValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.validator = MinValueValidator(0)

        self.valid_values = [1, 100, 0.001]
        self.invalid_values = [-0.001, 0, None]


class TestMinLengthValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.validator = MinLengthValidator(4)
        self.valid_values = [LenImplementer(5), LenImplementer(20), "012345", "!2*^%"]
        self.invalid_values = [LenImplementer(3), "0", "!^%", ""]


class TestMaxLengthValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.validator = MaxLengthValidator(5)
        self.valid_values = ["", "___", LenImplementer(2)]
        self.invalid_values = ["      ", "qwerty__", LenImplementer(5)]


class TestEmailValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.validator = EmailValidator()
        self.valid_values = ["qwerty@gmail.com", "John@Smith.com"]
        self.invalid_values = ["qwerty_gmail.com", "John@Smith_com", "@gmail.com"]


class TestRegexValidator(TestCase, ValidatorTestMixin):

    def setUp(self):
        self.validator = RegexValidator(r"^[A-Z].*$")
        self.invalid_values = ["_AAA", "", "aaa"]
        self.valid_values = ["A__", "W", "WWW"]


class TestIp4Validator(TestCase, ValidatorTestMixin):
    def setUp(self):
        self.validator = Ip4AddressValidator()
        self.valid_values = ["127.0.0.1", "192.188.1.1"]
        self.invalid_values = ["1270.0.1", "192.1881.1", None, object()]


class TestRequiredValidator(TestCase, ValidatorTestMixin):
    def setUp(self):
        self.validator = RequiredValidator()
        self.invalid_values = [UNSET, ]
        self.valid_values = [0, 2.5, object(), "Hello world!"]


class TestTypeValidator(TestCase, ValidatorTestMixin):
    def setUp(self):
        self.validator = TypedValidator(value_types=(int, float))
        self.valid_values = [0, 0.0, 99, -100.5, UNSET]
        self.invalid_values = [object(), "Hello world!"]