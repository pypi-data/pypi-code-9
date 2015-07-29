# -*- encoding: utf-8 -*-
from any2 import TransformationError
from any2 import ColumnMappingError


class BaseTransformer(object):
    """base class for all transformers
    """
    def __init__(self):
        self.typefuncs = {}

    def register_func(self, criterion, func):
        self.typefuncs[criterion] = func


class IndexTransformer(BaseTransformer):
    """apply a transformation to an object based on its index inside a list
    """
    def apply(self, value, index=None):
        """apply a transformation on the input value based on its index in a
        list.
        :param value: any object you want to tentatively transform
        :param index: the index of the item inside the row, only used
        in the other transformers implementations
        :raises: any2.exceptions.TransformationError
        """
        if index is None:
            raise TransformationError(
                "index cannot be None for value '{}'".format(
                    value
                )
            )

        func = self.typefuncs.get(index)

        if not callable(func):
            return value
        else:
            return func(value)


class NameTransformer(IndexTransformer):
    """WARNING: the name transformer works only if each name is unique. IE: it
    will not work as expected if you have duplicate names in your name list
    """
    def __init__(self, colnames):
        self.colnames = colnames
        super(NameTransformer, self).__init__()

    def register_func(self, criterion, func):
        if criterion not in self.colnames:
            raise ColumnMappingError(
                "Name {} should be in colnames, "
                "cannot register function {}".format(criterion, func)
            )
        else:
            index = self.colnames.index(criterion)
            super(NameTransformer, self).register_func(index, func)


class TypeTransformer(BaseTransformer):
    """apply a transformation to an object based on its type
    This is useful to obtain things like:

      if my value is False then give result: "Faux"
      if my value is True then give result: "Vrai"

    you must initialze the transformer and then register type transformers::

        import types

        def bool2string(val):
            if val:
                return "Vrai"
            else:
                return "Faux"

        t = TypeTransformer()
        t.register_func(types.BooleanType, bool2string)
        result = t.apply(True)
        assert result == "Vrai"

    This is used in conjonction with a Listlike2List adapter to feed XLS
    writer with only the data we effectively need to write
    """

    def apply(self, value, index=None):
        """apply a transformation on the value according to its type
        if a function if registered for the give value's type then the function
        will be called and the result returned

        :param value: any object you want to tentatively transform
        :param index: the index of the item inside the row, only used
        in the other transformers implementations
        """
        func = self.typefuncs.get(type(value), None)

        if not callable(func):
            return value
        else:
            return func(value)
