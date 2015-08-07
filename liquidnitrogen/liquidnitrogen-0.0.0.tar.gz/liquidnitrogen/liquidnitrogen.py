from inspect import isfunction
from datetime import datetime
from collections import OrderedDict

from frozendict import frozendict
from frozenordereddict import FrozenOrderedDict
from copy import deepcopy

from liquidnitrogen.exceptions import LiquidNitrogenException

IMMUTABLE_TYPES = frozenset({
    int,
    float,
    complex,
    str,
    bytes,
    tuple,
    frozenset,
    datetime,
    frozendict,
    FrozenOrderedDict
})


def isimmutable(thing):
    '''
        Determine whether a thing is immutable

        :param value thing: a Python value (object or primitive)
        :returns true if the value is known to liquidnitrogen to be of an immutable type
    '''

    return (
        thing is None or
        thing is True or
        thing is False or
        any([
            isinstance(thing, t)
            for t in IMMUTABLE_TYPES.union(frozenset({frozenobject}))
        ]) or
        isfunction(thing)
    )


class frozenobject(object):
    '''
        A wrapper for arbitrary Python objects,
        that protects against attribute mutation

        Warning: `freezemethod` and `freezeobject` perform a `deepcopy` of the object's attributes upon each method call in order to test whether the method call would modify the object. The attribute copy  may use a significant amount of memory. To save memory, model data with structures designed to be immutable, such as tuples, frozensets, frozendicts, etc.
    '''

    def __init__(self, value):
        '''
            Construct a frozen object

            :param value value: a Python object
            :returns a frozen version of the object
        '''

        self._value = value

    def __getattribute__(self, name):
        '''
            Override attribute getters,
            returning immutable versions of each attribute

            :param str name: an attribute name
            :returns value: a wrapped version of the attribute
        '''

        if name == '_value':
            return super(frozenobject, self).__getattribute__('_value')

        attribute = getattr(self._value, name)

        # protect methods from mutation
        if callable(attribute) and not isfunction(attribute):
            return frozenmethod(self._value, name)
        # protect non-method attributes from mutation
        else:
            return freeze(attribute)

    def __setattr__(self, name, value):
        '''
            Override attribute setters,
            preventing attribute mutation

            :param str name: an attribute name
            :param value value: a value for the attribute to take
            :raises LiquidNitrogenException in most cases
        '''

        if name == '_value':
            super(frozenobject, self).__setattr__('_value', value)
        else:
            raise LiquidNitrogenException(
                'Cannot alter attribute {0} of frozenobject {1}'
                .format(name, self)
            )

    def __call__(self, *args, **kwargs):
        '''
            Forwards method calls to the wrapped object

            :param list args: any positional call arguments
            :param dict kwargs: any named call arguments
            :returns value: the return value of the wrapped method call
            :raises LiquidNitrogenException if call would modify this object
        '''

        return self._value.__call__(*args, **kwargs)

    def __repr__(self):
        '''
            Forwards string representation calls to the wrapped object

            :returns str: a string representation of the wrapped object
        '''

        return self._value.__repr__()


def frozenmethod(obj, method_name):
    '''
        Create an immutable version of a method,
        that detects when a call would modify the object,
        and instead raises LiquidNitrogenException

        Warning: `freezemethod` and `freezeobject` perform a `deepcopy` of the object's attributes upon each method call in order to test whether the method call would modify the object. The attribute copy  may use a significant amount of memory. To save memory, model data with structures designed to be immutable, such as tuples, frozensets, frozendicts, etc.

        :param object obj: an object
        :param str method_name: a method to wrap on the object
        :returns method: a wrapped method that protects against mutation
    '''

    obj_copy = deepcopy(obj)
    method_copy = getattr(obj_copy, method_name)

    def protected_method(*args, **kwargs):
        result = method_copy(*args, **kwargs)

        # Has the copy mutated compared to the original?
        if obj_copy == obj:
            return result
        else:
            raise LiquidNitrogenException(
                'frozenmethod call {0} with arguments {1} {2} would mutate {3}'
                .format(method_name, args, kwargs, obj)
            )

    return protected_method

def freeze(thing):
    '''
        Given a Python value, return an immutable version of the value.

        Natively immutable values such as tuples, frozensets, and frozendicts are simply returned as-is.

        Methods and objects are wrapped to raise LiquidNitrogenExceptions on attempts to set attributes or call methods that would mutate the objects.

        Warning: `freezemethod` and `freezeobject` perform a `deepcopy` of the object's attributes upon each method call in order to test whether the method call would modify the object. The attribute copy  may use a significant amount of memory. To save memory, model data with structures designed to be immutable, such as tuples, frozensets, frozendicts, etc.

        :param value thing: a Python value (object or primitive)
        :returns a frozen version of the value
    '''

    if isimmutable(thing):
        return thing
    elif isinstance(thing, list):
        return tuple(thing)
    elif isinstance(thing, set):
        return frozenset(thing)
    elif isinstance(thing, OrderedDict):
        return FrozenOrderedDict(thing)
    elif isinstance(thing, dict):
        return frozendict(thing)
    else:
        return frozenobject(thing)
