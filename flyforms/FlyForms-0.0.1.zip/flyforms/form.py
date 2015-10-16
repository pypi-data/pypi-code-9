# coding=utf-8

from flyforms.validators import ValidationError
from flyforms.fields import AbstractField, UNSET
from flyforms.compatibility import with_metaclass

__all__ = ("Form", "BindingForm", "NonbindingForm")


class BoundField(object):
    """
    Fields with associated data attached to Form instance
    """

    def __init__(self, form, field_obj, field_name):
        """
        :param form: Form instance to attach
        :type form: Form

        :param field_obj: Field instance
        :type field_obj: instance of any AbstractField's subclass

        :param field_name: title of the field
        :type field_name: str
        """

        self.name = field_name
        self.form = form
        self.field = field_obj
        setattr(self.form, self.name, field_obj.default)

    def bind(self, value):
        """
        Bind field with given data

        :param value: given value
        """
        try:
            self.field.validate(value)  # do validation of value
        except ValidationError as e:
            self.form.errors[self.name] = str(e)  # add form's errors
        else:
            setattr(self.form, self.name, value)  # delegate value to form's attribute

    @property
    def is_bound(self):
        """
        Property that checks is data set for this field
        """
        return getattr(self.form, self.name, UNSET) is not UNSET


class FormMeta(type):
    """
    The metaclass for Form and it's subclasses
    """

    def __new__(mcs, name, bases, dct):

        fields = {}  # create a container for Form's fields names
        for attr, val in dct.items():  # walk through class attributes
            if isinstance(val, AbstractField):  # find all Field instances
                fields[attr] = val  # catch tem
        dct["_fields"] = fields  # update class attributes
        cls = super(FormMeta, mcs).__new__(mcs, name, bases, dct)  # call superclass __new__

        # Get all fields from MRO
        _fields = {}  # prepare container
        for base in cls.__mro__:  # walk through the MRO
            if hasattr(base, "_fields"):  # check has base any fields
                # noinspection PyProtectedMember
                _fields.update(base._fields)  # get fields from base
        cls._fields = _fields  # update Form's fields
        return cls


class Form(with_metaclass(FormMeta, object)):
    """
    The root class for all Forms
    """

    _fields = {}  # container for Form's fields

    def __new__(cls, *args, **kwargs):
        """
        :param cls: the Form class
        :param args: positional arguments for constructor (not used in this method)
        :param kwargs: keyword arguments for constrictor (not used in this method)

        :return: new Form instance

        """
        obj = super(Form, cls).__new__(cls)  # create new instance
        obj.errors = {}  # create a container for Form's errors
        obj.fields = {}  # create a container for Form's fields and data
        for field in cls._fields:  # walk through class fields
            obj.fields[field] = BoundField(obj, cls._fields[field], field)  # fill Form's fields (without data)
        return obj

    def __init__(self, **data):
        """
        :param data: additional data to form
        :type data: dict
        """
        for field in self.fields:  # walk through instance fields
            self.fields[field].bind(data.pop(field, UNSET))  # try to bind each field
        for unk in data:  # if some extra fields given  -> raise ValidationError
            self.errors[unk] = "Unknown field %s in data for Form %s" % (unk, self.__class__.__name__)

    @property
    def is_bound(self):
        """
        Property that checks is Form instance bound.
        Return True if all fields is bound. Otherwise, False.
        """
        return all(field.is_bound for field in self.fields.values())

    @property
    def is_valid(self):
        """
        Property that checks is Form instance valid.
        Return True when it's bound and there are no errors. Otherwise, False.
        """
        return self.is_bound and self.errors == {}


class NonbindingForm(with_metaclass(FormMeta, object)):
    """
    The root class for all NonbindingForms
    """

    _fields = {}  # container for NonbindingForm's fields

    def is_valid(self, **schema):
        """
        Check is given data valid.
        It is the same as the validate method but without rising ValidationError.

        :param schema: the from data.
        :type schema: dict.

        :return: boolean flag.
        :rtype: bool.

        """
        try:
            self.validate(**schema)
        except ValidationError:
            return False
        else:
            return True

    def validate(self, **schema):
        """
        Validate the given data.

        :param schema: the from data
        :type schema: dict

        :raise: ValidationError if data is not valid.

        """
        for field, field_obj in self._fields.items():  # walk through class fields
            if field not in schema:  # if field is not found in given data ...
                if field_obj.required:  # ... and it's required - it's bad
                    raise ValidationError("Required field %s missed in Form %s" % (field, self.__class__.__name__))
                continue
            field_obj.validate(schema.pop(field, UNSET))  # do field validation
        if schema:  # check for some extra data
            raise ValidationError(
                "Unknown fields " + ", ".join(schema.keys()) + " in schema for Form %s" % self.__class__.__name__
            )


# Add some symmetry =)
BindingForm = Form
