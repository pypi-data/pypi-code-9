# coding=utf-8
"""
This module contains a collection of fields classes
"""

from abc import ABCMeta
from collections import Iterable, deque
from warnings import warn

from flyforms.validators import *
from flyforms.validators import Validator
from flyforms.compatibility import string_types, with_metaclass, NoneType

__all__ = (
    "StringField",
    "EmailField",
    "IntField",
    "FloatField",
    "BooleanField",
    "Ip4Field"
)


UNSET = object()  # the default mark for not set values


class AbstractField(with_metaclass(ABCMeta, object)):
    """
    This the base class for all Fields.
    Fields instances reflect and validate data.
    """

    value_types = (type,)  # valid types of field value
    
    def __init__(self, required=True, choices=(), validators=(), default=UNSET):
        """
        :param required: boolean flag is this field required or can be empty
        :type required: bool

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """

        self.required = required

        # Check given default value
        self.default = default
        if not isinstance(self.default, self.value_types) and self.default is not UNSET:
            raise ValidationError(
                "Bad default value type. \nExpected %s, got %s" % (
                    self.value_types,
                    type(self.default)
                )
            )
        if self.required and self.default is not UNSET:
            warn(
                "Warning in field %s: default value given for required field. I'll be skipped.", RuntimeWarning
            )

        self.validators = deque()

        # Check is given choices iterable object
        if not isinstance(choices, Iterable):
            raise TypeError("Choices should be an iterable object")

        # Add choices validation, if necessary
        if choices:
            self.validators.appendleft(EntryValidator(choices))

        # Clean given list of validators, if necessary
        if not isinstance(validators, Iterable):
            validators = tuple(self.validators)

        # Check is given validators are callable object and extend validators list
        for validator in validators:
            if not isinstance(validator, Validator):
                raise TypeError("Validator should be a child of Validator superclass")
            self.validators.append(validator)

    def validate(self, value):
        """
        This is base validation of given value.
        It contain:
            - given value type check;
            - required check;
            - choices check;

        :param value: the value to validate
        :type value: any

        :raise ValidationError with first error occurred during validation
        """
        # Check the required flag
        if value is UNSET and self.required:
            raise ValidationError("Field is required.")

        # Check the type of given value
        if not isinstance(value, self.value_types):
            raise ValidationError(
                "Bad value type. Expected %s, got %s" % (self.value_types, type(value))
            )

        # Run all validators
        for validator in self.validators:
            validator(value)

    def is_valid(self, value):
        """
        The 'silent' variant of value validation.

        :param value: the value to validate
        :type value: any

        :return: True if given value is valid, otherwise - False
        :rtype: bool
        """
        try:
            self.validate(value)
        except ValidationError:
            return False
        else:
            return True


class StringField(AbstractField):
    """
    StringField reflects Python strings
    """

    value_types = string_types  # valid types of field value

    def __init__(self, min_length=None, max_length=None, regex="", **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param min_length: the minimum length of the string
        :type min_length: int or None

        :param max_length: the maximum length of the string
        :type max_length: int or None

        :param regex: the regular expression to validate
        :type regex: str or regexp

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(StringField, self).__init__(**kwargs)

        if min_length:
            self.validators.appendleft(MinLengthValidator(min_length, False))

        if max_length:
            self.validators.appendleft(MaxLengthValidator(max_length, False))

        if regex:
            self.validators.appendleft(RegexValidator(regex))


class EmailField(AbstractField):
    """
    EmailField reflects Python string corresponding to an email (str and unicode)
    """

    value_types = string_types  # valid types of field value

    def __init__(self, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(EmailField, self).__init__(**kwargs)

        self.validators.appendleft(EmailValidator())


class IntField(AbstractField):
    """
    IntField reflects Python integer (int)
    """

    value_types = (int, NoneType)  # valid types of field value

    def __init__(self, min_value=None, max_value=None, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param min_value: the minimum value of the given number
        :type min_value: int or None

        :param max_value: the maximum value of the given number
        :type max_value: int or None

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(IntField, self).__init__(**kwargs)

        if min_value and max_value:
            self.validators.appendleft(MinMaxValueValidator(min_value, max_value, False))
        elif min_value:
            self.validators.appendleft(MinValueValidator(min_value, False))
        elif max_value:
            self.validators.appendleft(MaxValueValidator(max_value, False))


class FloatField(IntField):
    """
    FloatField reflects Python float (float)
    """

    value_types = (float, NoneType)  # valid types of field value


class BooleanField(AbstractField):
    """
    BooleanField reflects Python boolean (bool)
    """

    value_types = (bool, NoneType)  # valid types of field value

    def __init__(self, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        """
        super(BooleanField, self).__init__(**kwargs)


class Ip4Field(AbstractField):
    """
    Ip4Field reflects Python string corresponding to an IPv4 address (str and unicode)
    """

    value_types = string_types  # valid types of field value

    def __init__(self, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types

        """
        super(Ip4Field, self).__init__(**kwargs)

        self.validators.appendleft(Ip4AddressValidator())
