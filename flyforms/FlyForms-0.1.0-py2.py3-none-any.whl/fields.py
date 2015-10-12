# coding=utf-8
"""
This module contains a collection of fields classes
"""

from abc import ABCMeta
from collections import Iterable
from itertools import chain
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


class Field(with_metaclass(ABCMeta, object)):
    """
    This the base class for all Fields.
    Fields instances reflect and validate data.
    """

    value_types = (type,)  # valid types of field value

    def __init__(self, required=True, choices=(), validators=(), **kwargs):
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

        # Check given default value
        self.default = kwargs.get("default", UNSET)
        if not isinstance(self.default, self.value_types) and self.default is not UNSET:
            raise TypeError(
                "Bad default value type. \nExpected {}, got {}".format(self.value_types, type(self.default))
            )
        if required and self.default is not UNSET:
            warn(
                "Warning in field %s: default value given for required field. I'll be skipped.", RuntimeWarning
            )

        # Define validators container
        self.base_validators = []

        # Add required validation, if necessary
        if required:
            self.base_validators.append(RequiredValidator())
        self.required = required

        # Add type validation
        self.base_validators.append(TypedValidator(self.value_types))

        # Check is given choices iterable object
        if not isinstance(choices, Iterable):
            raise TypeError("Choices should be an iterable object")

        # Check choices type
        for choice in choices:
            if not isinstance(choice, self.value_types):
                raise TypeError(
                    "Bad value type in choices. \nExpected %s, got %s" % (
                        self.value_types,
                        type(choice)
                    )
                )

        # Add choices validation, if necessary
        if choices:
            self.base_validators.append(EntryValidator(choices))

        # Clean given list of validators, if necessary
        if not isinstance(validators, Iterable):
            validators = (validators,)

        # Check is given validators are callable object and extend validators list
        for validator in validators:
            if not isinstance(validator, Validator):
                raise TypeError("Validator should be a child of Validator superclass")
        self.custom_validators = validators

    def validate(self, value):
        """
        This is base validation of given value (type, required and choices checks)

        :param value: the value to validate
        :type value: any

        :raise: ValidationError with first error occurred during validation
        """

        # Check is value set
        if not self.required and not is_set(value):
            return

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

        # Check is value set
        if not self.required and not is_set(value):
            return True

        # Check value via validators
        for validator in self.validators:
            if not validator.is_valid(value):
                return False
        return True

    @property
    def validators(self):
        return chain(self.base_validators, self.custom_validators)


class StringField(Field):
    """
    Reflects Python strings
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
            self.base_validators.append(MinLengthValidator(min_length, False))

        if max_length:
            self.base_validators.append(MaxLengthValidator(max_length, False))

        if regex:
            self.base_validators.append(RegexValidator(regex))


class EmailField(Field):
    """
    Reflects Python string corresponding to an email
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

        self.base_validators.append(EmailValidator())


class IntField(Field):
    """
    Reflects Python integer (:code:`int`)
    """

    value_types = (int, NoneType)  # valid types of field value

    def __init__(self, min_value=None, max_value=None, **kwargs):
        """
        :param required: boolean flag is this field required
        :type required: bool

        :param min_value: the minimum valid value

        :param max_value: the maximum valid value

        :param choices: iterable object contains possible values of this field
        :type choices: iterable

        :param validators: the additional validators for field
        :type validators: list of callable

        :param default: the default value of the field
        :type default: instance of value_types
        """
        super(IntField, self).__init__(**kwargs)

        if min_value is not None and max_value is not None:
            self.base_validators.append(MinMaxValueValidator(min_value, max_value, False))
        elif min_value is not None:
            self.base_validators.append(MinValueValidator(min_value, False))
        elif max_value is not None:
            self.base_validators.append(MaxValueValidator(max_value, False))


class FloatField(IntField):
    """
    Reflects Python float (:code:`float`)
    """

    value_types = (float, NoneType)  # valid types of field value


class BooleanField(Field):
    """
    Reflects Python boolean (:code:`bool`)
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


class Ip4Field(Field):
    """
    Ip4Field reflects Python string corresponding to an IPv4 address
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

        self.base_validators.append(Ip4AddressValidator())
