# coding=utf-8
from abc import ABCMeta, abstractmethod
from collections import Iterable
import re

from flyforms.compatibility import string_types, with_metaclass

__all__ = (
    "EntryValidator",
    "MaxValueValidator",
    "MaxLengthValidator",
    "MinLengthValidator",
    "MinMaxValueValidator",
    "MinValueValidator",
    "EmailValidator",
    "RegexValidator",
    "Ip4AddressValidator",
    "ValidationError"
)


class ValidationError(Exception):
    """
    Raised when a validator fails to validate it's input.
    """
    pass


class Validator(with_metaclass(ABCMeta, object)):
    """
    The abstract root class for all Validators
    """

    @abstractmethod
    def validate(self, value):
        """
        Validate the given value

        :param value: given value to validate

        :raise ValidationError if given value is not valid
        """
        pass

    def __call__(self, value):
        """
        The same with validate
        """
        self.validate(value)

    def is_valid(self, value):
        """
        The 'silent' variant of validation

        :param value: given value to validate

        :return: boolean flag is given value valid
        :rtype: bool
        """
        try:
            self.validate(value)
        except ValidationError:
            return False
        else:
            return True


class SimpleValidator(with_metaclass(ABCMeta, Validator)):
    """
    The root class for Validators with only one validation case
    """

    # It's positive validation case (given value should satisfies this condition)
    positive_case = abstractmethod(lambda self, x: x is x)

    def validate(self, value):
        """
        Implementation of Validator's validate method
        """
        if not self.positive_case(value):  # if positive case wasn't satisfied then ValidationError will be raised
            raise ValidationError("%s failed with value %s." % (self.__class__.__name__, value))


class EntryValidator(SimpleValidator):
    """
    EntryValidator validates is given value in specified during initialization iterable object
    """

    def __init__(self, iterable):
        """
        :param iterable: the iterable object

        :raise: TypeError if given object is not iterable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Entry validator instance need an iterable object")
        self.iterable = iterable

    positive_case = lambda self, value: value in self.iterable


class MinValueValidator(SimpleValidator):
    """
    Validates is given value greater than specified during initialization value
    """

    def __init__(self, min_value, strong=True):
        """
        :param min_value: the minimum valid value

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.min_value = min_value
        self.strong = strong

    positive_case = lambda self, value: value > self.min_value if self.strong else value >= self.min_value


class MaxValueValidator(SimpleValidator):
    """
    Validates is given value less than specified during initialization value
    """
    def __init__(self, max_value, strong=True):
        """
        :param max_value: the maximum valid value

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.max_value = max_value
        self.strong = strong

    positive_case = lambda self, value: value < self.max_value if self.strong else value <= self.max_value


class MinMaxValueValidator(SimpleValidator):
    """
    Validates is given value less than maximum value
    and greater then minimum value specified during initialization
    """

    def __init__(self, min_value, max_value, strong=True):
        """
        :param min_value: the minimum valid value

        :param max_value: the maximum valid value

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.min_value = min_value
        self.max_value = max_value
        self.strong = strong

    positive_case = lambda self, value: self.min_value < value < self.max_value if self.strong else \
        self.min_value <= value <= self.max_value


class MinLengthValidator(SimpleValidator):
    """
    Validates the minimum object length
    """

    def __init__(self, min_length, strong=True):
        """
        :param min_length: the minimum valid length

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        self.len = min_length
        self.strong = strong

    def validate(self, value):
        """
        Implementation of Validator's validate method
        """
        if not hasattr(value, '__len__'):  # check for __len__ attribute
            raise ValidationError("Validation failed because value of type '%s' has no len()" % type(value))
        super(MinLengthValidator, self).validate(
            len(value)
        )

    positive_case = lambda self, value_len: value_len > self.len if self.strong else value_len >= self.len


class MaxLengthValidator(MinLengthValidator):
    """
    Validates the maximum object length
    """

    def __init__(self, max_length, strong=True):
        """
        :param max_length: the maximum valid length

        :param strong: boolean flag should be comparison strict or not
        :type strong: bool
        """
        super(MaxLengthValidator, self).__init__(max_length, strong)

    positive_case = lambda self, value_len: value_len < self.len if self.strong else value_len <= self.len


class RegexValidator(SimpleValidator):
    """
    RegexValidator validates matching with regular expression
    """

    def __init__(self, regex, flags=0):
        """
        :param regex: the regular expression

        :param flags: flags passed to re.match function
        """
        self.r = re.compile(regex, flags)

    def validate(self, value):
        """
        The Validator's validate method implementation
        """
        if not isinstance(value, string_types):
            raise ValidationError("Validation failed because value is not string")
        super(RegexValidator, self).validate(value)

    positive_case = lambda self, value: self.r.match(value)


class EmailValidator(RegexValidator):
    """
    Validates an email address via simple regex.
    """
    def __init__(self):
        super(EmailValidator, self).__init__(
            regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )


class Ip4AddressValidator(RegexValidator):
    """
    Validates an IPv4 address via simple regex.
    """

    def __init__(self):
        super(Ip4AddressValidator, self).__init__(
            regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        )
