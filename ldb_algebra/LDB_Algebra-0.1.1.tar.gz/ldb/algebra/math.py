# Copyright 2015 Alex Orange
# 
# This file is part of LDB Algebra.
# 
# LDB Algebra is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LDB Algebra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with LDB Algebra.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
import math
from ldb.algebra.expression import (CachedExpression, Expression, bind,
                                    differentiate)


def wrap_function(function_class, function):
    function_class.function = function
    return lambda x: function_class(x) if isinstance(x, Expression) else function(x)


class WrappedFunction(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, expression):
        if isinstance(expression, Expression):
            return self.function_class(expression)
        else:
            return self.function(expression)


class MathFunction(CachedExpression):
    def __init__(self, a):
        super(MathFunction, self).__init__()
        self.a = a

    def _bind(self, binding):
        bound = bind(self.a, binding)
        if isinstance(bound, Expression):
            return self.__class__(bound)
        else:
            return self.function(bound)

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da * self.derivative


class SquareRoot(MathFunction):
    def __init__(self, a):
        super(SquareRoot, self).__init__(a)

    @property
    def derivative(self):
        return 0.5 / self

    def __repr__(self):
        return "sqrt(%s)"%(repr(self.a))


class Logarithm(MathFunction):
    def __init__(self, a):
        super(Logarithm, self).__init__(a)

    @property
    def derivative(self):
        return 1 / self.a

    def __repr__(self):
        return "log(%s)"%(repr(self.a))


sqrt = wrap_function(SquareRoot, math.sqrt)
log = wrap_function(Logarithm, math.log)
