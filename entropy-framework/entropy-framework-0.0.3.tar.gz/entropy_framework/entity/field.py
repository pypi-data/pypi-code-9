import types


class Field(object):
    _type = types.ObjectType
    _default = None

    def __init__(self, default=None, is_none=True):
        if default:
            if self.is_valid(default):
                self._default = default
            else:
                raise TypeError("Default value '%s' is not valid" % (default,))

        self.is_none = is_none

    def validate(self, val):
        """
        Get valid val
        :param val:
        :return:
        """
        if self.is_valid(val):
            return val
        else:
            raise TypeError("Value '%s' is not valid. It should be '%s' instance." % (val, self._type))

    def get_default(self):
        """
        :return: default value of the field
        """
        return self._default

    def is_valid(self, val):
        """
        Checking val validity
        :param val:
        :return:
        """
        return isinstance(val, self._type)


class IntField(Field):
    _type = types.IntType
    _default = 0


class FloatField(Field):
    _type = types.FloatType
    _default = .0


class StrField(Field):
    _type = str
    _default = ''


class ListField(Field):
    _type = types.ListType
    _default = []


class LambdaField(Field):
    _type = types.LambdaType


class FunctionField(Field):
    _type = types.FunctionType


class BoolField(Field):
    _type = types.BooleanType
    _default = False
