# Copyright 2014 Alex Orange
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
from ldb.algebra.expression import (CachedExpression, bind, differentiate,
                                    Expression)
from ldb.algebra.math import sqrt

pi = math.pi

def degrees(expression):
    return 180.0/pi*expression

def radians(expression):
    return pi/180.0*expression

def acos(expression):
    if isinstance(expression, Expression):
        return ACos(expression)
    else:
        return math.acos(expression)

def acosh(expression):
    if isinstance(expression, Expression):
        return ACosh(expression)
    else:
        return math.acosh(expression)

def asin(expression):
    if isinstance(expression, Expression):
        return ASin(expression)
    else:
        return math.asin(expression)

def asinh(expression):
    if isinstance(expression, Expression):
        return ASinh(expression)
    else:
        return math.asinh(expression)

def atan(expression):
    if isinstance(expression, Expression):
        return ATan(expression)
    else:
        return math.atan(expression)

def atan2(a, b):
    if isinstance(a, Expression) or isinstance(b, Expression):
        return ATan2(a, b)
    else:
        return math.atan2(a, b)

def atanh(expression):
    if isinstance(expression, Expression):
        return ATanh(expression)
    else:
        return math.atanh(expression)

def cos(expression):
    if isinstance(expression, Expression):
        return Cos(expression)
    else:
        return math.cos(expression)

def cosh(expression):
    if isinstance(expression, Expression):
        return Cosh(expression)
    else:
        return math.cosh(expression)

def sin(expression):
    if isinstance(expression, Expression):
        return Sin(expression)
    else:
        return math.sin(expression)

def sinh(expression):
    if isinstance(expression, Expression):
        return Sinh(expression)
    else:
        return math.sinh(expression)

def tan(expression):
    if isinstance(expression, Expression):
        return Tan(expression)
    else:
        return math.tan(expression)

def tanh(expression):
    if isinstance(expression, Expression):
        return Tanh(expression)
    else:
        return math.tanh(expression)


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


