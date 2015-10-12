# coding=utf-8
from inspect import isclass

from flyforms.validators import ValidationError, UNSET
from flyforms.fields import Field
from flyforms.compatibility import with_metaclass


__all__ = ("Form", "validate_schema")


class FormMeta(type):
    """
    The metaclass for Form and it's subclasses
    """

    def __new__(mcs, name, bases, dct):

        fields = []  # create a container for Form's fields names
        for attr, val in dct.items():  # walk through class attributes
            if isinstance(val, Field):  # find all Field instances
                fields.append(attr)  # catch them
                dct[attr] = FormField(attr, val)  # and replace with descriptor
        dct["_fields"] = fields  # update class attributes
        cls = super(FormMeta, mcs).__new__(mcs, name, bases, dct)  # create new class

        # Get all fields names from MRO
        _fields = set()  # prepare container
        for base in cls.__mro__:  # walk through the MRO
            _fields |= set(getattr(base, "_fields", []) ) # get fields names from each base
        cls._fields = _fields  # update Form's fields
        return cls


class FormField(object):
    def __init__(self, name, field_obj):
        if not isinstance(field_obj, Field):
            raise TypeError("You should bind FormField with Field subclass instance, not {}".format(type(field_obj)))
        self.name = name
        self.field = field_obj

    def __get__(self, instance, owner):
        if isinstance(instance, Form) and issubclass(owner, Form):
            return instance.raw_data.get(self.name, UNSET)
        if instance is None and issubclass(owner, Form):
            return self.field
        raise AttributeError("You can\'t use FormField without Form")

    def __set__(self, instance, value):
        if not isinstance(instance, Form):
            raise AttributeError("You can\'t use FormField without Form")
        if instance.raw_data.get(self.name, UNSET) is not UNSET:
            raise AttributeError("You can\'t overwrite already bound field {}!".format(self.name))
        try:
            self.field.validate(value)
        except ValidationError as e:
            instance.errors[self.name] = str(e)
        else:
            instance.raw_data[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("You can\'t delete Form fields!")


class Form(with_metaclass(FormMeta, object)):
    """
    The root class for all Forms
    """

    _fields = set()

    def __init__(self, **data):
        """
        :param data: additional data to form
        :type data: dict
        """
        self.raw_data = {}  # create a container for Form's data
        self.errors = {}  # create a container for Form's errors

        for field_name in self._fields:  # walk through class fields
            setattr(self, field_name, data.pop(field_name, UNSET))  # and try to set up them
        for unk in data:  # if some extra fields given it's an error
            self.errors[unk] = "Unknown field %s in data for Form %s" % (unk, self.__class__.__name__)

    @property
    def is_bound(self):
        """
        Checks is Form instance bound.
        Returns True if all fields is bound. Otherwise, False.
        """
        return UNSET not in self.raw_data.values()

    @property
    def is_valid(self):
        """
        Checks is Form instance valid.
        Returns there are no errors. Otherwise, False.
        """
        return self.errors == {}

    @property
    def data(self):
        """
        Property that returns :code:`dict` with bound data (if you need all data even unset values -
        use :code:`form.raw_data`)
        """
        return {field: self.raw_data[field] for field in self._fields if self.raw_data[field] is not UNSET}


def validate_schema(form_cls, **data):
    """
    This function validates given data via given Form subclass
    without creating defined Form instance.

    :param form_cls: defined Form class
    :type form_cls: Form subclass
    :param data: data to validate
    :return: boolean flag is data valid
    :rtype: bool

    :raise TypeError: if given *form_cls* is not class or not Form subclass
    """
    if not isclass(form_cls) or not issubclass(form_cls, Form):
        raise TypeError("You should pass Form subclass, not instance as first arg")

    for field_name in form_cls._fields:
        field_obj = getattr(form_cls, field_name)
        if not field_obj.is_valid(data.pop(field_name, UNSET)):
            return False
    if data:
        return False
    return True
