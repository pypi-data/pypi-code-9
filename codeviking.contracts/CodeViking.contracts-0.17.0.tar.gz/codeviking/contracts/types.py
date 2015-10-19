from collections import namedtuple, OrderedDict

from codeviking.contracts.argcheckers import NamedTupleArgChecker

__author__ = 'dan'


def NamedTuple(name, elements):
    """
    Create a new named tuple class.
    :param name: the name of the class
    :type name: str
    :param elements: ordered list of fields: (field_name, field_checker)
    :type elements: list[(str, ArgCheck)]
    :return: the class
    :rtype: namedtuple
    """
    checker = NamedTupleArgChecker(name, elements)
    T = namedtuple(name, [n for (n, _) in elements])
    orig_new = T.__new__

    def __new__(*args, **kwargs):
        ok = checker((args[1:], kwargs), T.__new__.__globals__)
        return orig_new(*args, **kwargs)

    T.__new__ = __new__
    T.__name__ = name
    return T
