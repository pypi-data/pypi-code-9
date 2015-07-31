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

from __future__ import absolute_import, division

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
        self.children = (a,)

    def _bind(self, binding):
        bound = bind(self.children[0], binding)
        if isinstance(bound, Expression):
            return self.__class__(bound)
        else:
            return self.function(bound)

    def _differentiate(self, variable):
        da = differentiate(self.children[0], variable)
        return da * self.derivative


class SquareRoot(MathFunction):
    def __init__(self, a):
        super(SquareRoot, self).__init__(a)

    @property
    def derivative(self):
        return 0.5 / self

    def __repr__(self):
        return "sqrt(%s)"%(repr(self.children[0]))


class Logarithm(MathFunction):
    def __init__(self, a):
        super(Logarithm, self).__init__(a)

    @property
    def derivative(self):
        return 1 / self.children[0]

    def __repr__(self):
        return "log(%s)"%(repr(self.children[0]))


class ACos(MathFunction):
    def __init__(self, a):
        super(ACos, self).__init__(a)

    @property
    def derivative(self):
        return -1 / sqrt(1.0 - self.children[0]*self.children[0])

    def __repr__(self):
        return "acos(%s)"%(repr(self.children[0]))


class ACosh(MathFunction):
    def __init__(self, a):
        super(ACosh, self).__init__(a)

    @property
    def derivative(self):
        return 1 / sqrt(self.children[0]*self.children[0] - 1.0)

    def __repr__(self):
        return "acosh(%s)"%(repr(self.children[0]))


class ASin(MathFunction):
    def __init__(self, a):
        super(ASin, self).__init__(a)

    @property
    def derivative(self):
        return 1 / sqrt(1.0 - self.children[0]*self.children[0])

    def __repr__(self):
        return "asin(%s)"%(repr(self.children[0]))


class ASinh(MathFunction):
    def __init__(self, a):
        super(ASinh, self).__init__(a)

    @property
    def derivative(self):
        return 1 / sqrt(self.children[0]*self.children[0] + 1.0)

    def __repr__(self):
        return "asinh(%s)"%(repr(self.children[0]))


class ATan(MathFunction):
    def __init__(self, a):
        super(ATan, self).__init__(a)

    @property
    def derivative(self):
        return 1 / (self.children[0]*self.children[0] + 1.0)

    def __repr__(self):
        return "atan(%s)"%(repr(self.children[0]))


class ATan2(CachedExpression):
    def __init__(self, a, b):
        super(ATan2, self).__init__()
        self.children = (a,b)

    def _bind(self, binding):
        return atan2(bind(self.children[0], binding),
                     bind(self.children[1], binding))

    def _differentiate(self, variable):
        a = self.children[0] / self.children[1]
        da = differentiate(a, variable)
        return da / (a*a + 1.0)

    def __repr__(self):
        return "atan2(%s, %s)"%(repr(self.children[0]), repr(self.children[1]))


class ATanh(MathFunction):
    def __init__(self, a):
        super(ATanh, self).__init__(a)

    @property
    def derivative(self):
        return 1 / (1.0 - self.children[0]*self.children[0])

    def __repr__(self):
        return "atanh(%s)"%(repr(self.children[0]))


class Cos(MathFunction):
    def __init__(self, a):
        super(Cos, self).__init__(a)

    @property
    def derivative(self):
        return -sin(self.children[0])

    def __repr__(self):
        return "cos(%s)"%(repr(self.children[0]))


class Cosh(MathFunction):
    def __init__(self, a):
        super(Cosh, self).__init__(a)

    @property
    def derivative(self):
        return sinh(self.children[0])

    def __repr__(self):
        return "cosh(%s)"%(repr(self.children[0]))


class Sin(MathFunction):
    def __init__(self, a):
        super(Sin, self).__init__(a)

    @property
    def derivative(self):
        return cos(self.children[0])

    def __repr__(self):
        return "sin(%s)"%(repr(self.children[0]))


class Sinh(MathFunction):
    def __init__(self, a):
        super(Sinh, self).__init__(a)

    @property
    def derivative(self):
        return cosh(self.children[0])

    def __repr__(self):
        return "sinh(%s)"%(repr(self.children[0]))


class Tan(MathFunction):
    def __init__(self, a):
        super(Tan, self).__init__(a)

    def derivative(self):
        return 1 / (cos(self.children[0])*cos(self.children[0]))

    def __repr__(self):
        return "tan(%s)"%(repr(self.children[0]))


class Tanh(MathFunction):
    def __init__(self, a):
        super(Tanh, self).__init__(a)

    def _differentiate(self, variable):
        return 1 / (cosh(self.children[0])*cosh(self.children[0]))

    def __repr__(self):
        return "tanh(%s)"%(repr(self.children[0]))


sqrt = wrap_function(SquareRoot, math.sqrt)
log = wrap_function(Logarithm, math.log)

acos = wrap_function(ACos, math.acos)
acosh = wrap_function(ACosh, math.acosh)
asin = wrap_function(ASin, math.asin)
asinh = wrap_function(ASinh, math.asinh)
atan = wrap_function(ATan, math.atan)
atan2 = wrap_function(ATan2, math.atan2)
atanh = wrap_function(ATanh, math.atanh)
cos = wrap_function(Cos, math.cos)
cosh = wrap_function(Cosh, math.cosh)
sin = wrap_function(Sin, math.sin)
sinh = wrap_function(Sinh, math.sinh)
tan = wrap_function(Tan, math.tan)
tanh = wrap_function(Tanh, math.tanh)
