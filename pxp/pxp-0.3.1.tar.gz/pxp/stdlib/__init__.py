"""This package contains the implementaion of pxp standard library methods and constants."""

from pxp.function import FunctionList
from pxp.scope import DictScope

from pxp.stdlib.general import general_functions
from pxp.stdlib.operator import operator_functions
from pxp.stdlib.math import math_functions, math_constants
from pxp.stdlib.string import string_functions


_function_list = FunctionList()
_function_list.merge(general_functions,
                     operator_functions,
                     math_functions,
                     string_functions)


global_scope = DictScope(None, math_constants, _function_list)
