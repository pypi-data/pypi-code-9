"""Utilities that operate on functions."""


def is_function(obj):
    """
    :param obj: the object to check
    :return: whether the object is callable
    """
    return hasattr(obj, '__call__')



def compose(*functions):
    """
    Composes functions which take a single argument, e.g.:
    
    >> from nose.tools import assert_almost_equal
    >> from math import tan, atan, pi
    >> ident = compose(tan, atan)
    >> assert_almost_equal(ident(pi), pi)
    True

    :param functions: the functions to compose, in reverse order of
        application (outer to inner)
    :return: the function to apply the composition to a value
    """
    # The return value is a function which calls the functions to
    # compose in inner-to-outer succession on the prior result,
    # starting with the original input value.
    return lambda x: reduce(lambda memo, f: f(memo), reversed(functions), x)
