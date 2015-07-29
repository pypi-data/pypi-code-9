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


class ACos(CachedExpression):
    def __init__(self, a):
        super(ACos, self).__init__()
        self.a = a

    def _bind(self, binding):
        return acos(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return -da / sqrt(1.0 - self.a*self.a)

    def __repr__(self):
        return "acos(%s)"%(repr(self.a))


class ACosh(CachedExpression):
    def __init__(self, a):
        super(ACosh, self).__init__()
        self.a = a

    def _bind(self, binding):
        return acosh(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / sqrt(self.a*self.a - 1.0)

    def __repr__(self):
        return "acosh(%s)"%(repr(self.a))


class ASin(CachedExpression):
    def __init__(self, a):
        super(ASin, self).__init__()
        self.a = a

    def _bind(self, binding):
        return asin(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / sqrt(1.0 - self.a*self.a)

    def __repr__(self):
        return "asin(%s)"%(repr(self.a))


class ASinh(CachedExpression):
    def __init__(self, a):
        super(ASinh, self).__init__()
        self.a = a

    def _bind(self, binding):
        return asinh(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / sqrt(self.a*self.a + 1.0)

    def __repr__(self):
        return "asinh(%s)"%(repr(self.a))


class ATan(CachedExpression):
    def __init__(self, a):
        super(ATan, self).__init__()
        self.a = a

    def _bind(self, binding):
        return atan(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / (self.a*self.a + 1.0)

    def __repr__(self):
        return "atan(%s)"%(repr(self.a))


class ATan2(CachedExpression):
    def __init__(self, a, b):
        super(ATan2, self).__init__()
        self.a = a
        self.b = b

    def _bind(self, binding):
        return atan2(bind(self.a, binding), bind(self.b, binding))

    def _differentiate(self, variable):
        a = self.a / self.b
        da = differentiate(a, variable)
        return da / (a*a + 1.0)

    def __repr__(self):
        return "atan2(%s, %s)"%(repr(self.a), repr(self.b))


class ATanh(CachedExpression):
    def __init__(self, a):
        super(ATanh, self).__init__()
        self.a = a

    def _bind(self, binding):
        return atanh(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / (1.0 - self.a*self.a)

    def __repr__(self):
        return "atanh(%s)"%(repr(self.a))


class Cos(CachedExpression):
    def __init__(self, a):
        super(Cos, self).__init__()
        self.a = a

    def _bind(self, binding):
        return cos(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da * -sin(self.a)

    def __repr__(self):
        return "cos(%s)"%(repr(self.a))


class Cosh(CachedExpression):
    def __init__(self, a):
        super(Cosh, self).__init__()
        self.a = a

    def _bind(self, binding):
        return cosh(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da * sinh(self.a)

    def __repr__(self):
        return "cosh(%s)"%(repr(self.a))


class Sin(CachedExpression):
    def __init__(self, a):
        super(Sin, self).__init__()
        self.a = a

    def _bind(self, binding):
        return sin(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da * cos(self.a)

    def __repr__(self):
        return "sin(%s)"%(repr(self.a))


class Sinh(CachedExpression):
    def __init__(self, a):
        super(Sinh, self).__init__()
        self.a = a

    def _bind(self, binding):
        return sinh(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da * cosh(self.a)

    def __repr__(self):
        return "sinh(%s)"%(repr(self.a))


class Tan(CachedExpression):
    def __init__(self, a):
        super(Tan, self).__init__()
        self.a = a

    def _bind(self, binding):
        return tan(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / (cos(self.a)*cos(self.a))

    def __repr__(self):
        return "tan(%s)"%(repr(self.a))


class Tanh(CachedExpression):
    def __init__(self, a):
        super(Tanh, self).__init__()
        self.a = a

    def _bind(self, binding):
        return tanh(bind(self.a, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        return da / (cosh(self.a)*cosh(self.a))

    def __repr__(self):
        return "tanh(%s)"%(repr(self.a))


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
