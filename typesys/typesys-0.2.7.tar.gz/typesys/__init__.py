
"""
Typesys
-------

Typesys is a module that is meant to make it more easy to manage types.
It contains three decorators; type_hints, type_corrector, and return_type.

usage:
    from typesys import type_hints, type_corrector, return_type
    
    Type hint:

    # a and b must be integers
    @type_hints(int, int)
    def add(a, b):
        return a+b


    # also work with default arguments
    @type_hints(int, float)
    def add(a, b=0.0):
        return a+b


    # accepts both integers and floats as arguments
    @type_hints(int, float)
    def mult(*numbers):
        result = 1
        for num in numbers:
            result *= num
        return result


    # Only accept integer arguments
    @type_hints(int)
    def mult(**kwargs):
        x = kwargs.get('x')
        y = kwargs.get('y')
        z = kwargs.get('z')    
        return x * y * z


    Type corrector:
    
    # x and y will be casted to integers,
    # if they have another type, and if it's
    # possible to cast them to integers
    @type_corrector(int, int)
    def add(x,y):
        return x+y

    # same as above but with *args
    # only need one type as paramater when
    # decorating a function with *args
    @type_corrector(int)
    def mult(*numbers):
        result = 1
        for num in numbers:
            result *= num
        return result

    
    Same as above, but with **kwargs
    @type_corrector(int)
    def kw_mult(**kwargs):
        x = kwargs.get('x')
        y = kwargs.get('y')
        z = kwargs.get('z')
        return x * y * z


    Return type
    
    # accepts both integers, float and complex numbers
    # to be returned
    @return_type(int, float, complex)
    def add(x,y):
        return x+y


    # only accept integers to be returned
    @return_type(int)
    def strict_add(x,y):
        return x+y

"""

__title__ = 'typesys'
__version__ = '0.2.7'
__author__ = 'Fredrik Gjertsen'
__licence__ = 'MIT'
__copyright__ = 'Copyright 2015 Fredrik Gjertsen'

from .type_system import type_corrector, type_hints, return_type

