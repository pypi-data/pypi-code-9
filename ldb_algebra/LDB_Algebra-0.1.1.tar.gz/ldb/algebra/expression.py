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

import operator

def freezedict(dict_):
    return tuple(sorted(dict_.items()))

class MethodCache(object):
    def __init__(self):
        self.order = []
        self.cache = {}
        self.max_len = 5

    def __contains__(self, key):
        return key in self.order

    def get_result(self, key):
        # TODO: Test performance for test and test and grab vs grab and handle
        # exception
        if key in self.order:
            return self.cache[key]

    def store_result(self, key, val):
        if key in self.order:
            self.order.remove(key)
        elif len(self.order) >= self.max_len:
            to_kill = self.order[0]
            del self.cache[to_kill]
            del self.order[0]

        self.cache[key] = val
        self.order.append(key)


def bind(expression, binding):
    if hasattr(expression, 'bind'):
        return expression.bind(**binding)
    else:
        return expression


def differentiate(expression, variable):
    if hasattr(expression, 'differentiate'):
        return expression.differentiate(variable)
    else:
        return 0


class Expression(object):
    def __init__(self):
        pass

    def __mul__(self, other):
        if other == 0:
            return 0
        elif other == 1:
            return self
        return Product(self, other)

    def __rmul__(self, other):
        if other == 0:
            return 0
        elif other == 1:
            return self
        return Product(other, self)

    def __add__(self, other):
        if other == 0:
            return self
        return Sum(self, other)

    def __radd__(self, other):
        if other == 0:
            return self
        return Sum(other, self)

    def __sub__(self, other):
        if self == other:
            return 0
        if other == 0:
            return self
        return Sum(self, -1*other)

    def __rsub__(self, other):
        if self == other:
            return 0
        if other == 0:
            return -self
        return Sum(other, -1*self)

    def __truediv__(self, other):
        if other == 1:
            return self
        return Quotient(self, other)

    def __rtruediv__(self, other):
        if other == 0:
            return 0
        return Quotient(other, self)

    def __div__(self, other):
        if other == 1:
            return self
        return Quotient(self, other)

    def __rdiv__(self, other):
        if other == 0:
            return 0
        return Quotient(other, self)

    def __neg__(self):
        return -1*self


class Variable(Expression):
    def __init__(self, var_name):
        self.var_name = var_name

    def bind(self, **binding):
        if self.var_name in binding:
            return binding[self.var_name]
        else:
            return self

    def differentiate(self, variable):
        if self.var_name == variable:
            return 1
        else:
            return 0

    def __repr__(self):
        return self.var_name


class CachedExpression(Expression):
    def __init__(self):
        self._binding_cache = MethodCache()
        self._differentiate_cache = MethodCache()

    def bind(self, **binding):
        hash_binding = freezedict(binding)
        if hash_binding in self._binding_cache:
            return self._binding_cache.get_result(hash_binding)
        else:
            val = self._bind(binding)
            self._binding_cache.store_result(hash_binding, val)
            return val

    def differentiate(self, variable):
        if variable in self._differentiate_cache:
            return self._differentiate_cache.get_result(variable)
        else:
            val = self._differentiate(variable)
            self._differentiate_cache.store_result(variable, val)
            return val


class Product(CachedExpression):
    def __init__(self, a, b):
        super(Product, self).__init__()
        self.a = a
        self.b = b

    def _bind(self, binding):
        return bind(self.a, binding) * bind(self.b, binding)

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        db = differentiate(self.b, variable)
        return self.b * da + self.a * db

    def __repr__(self):
        return "(%s * %s)"%(repr(self.a), repr(self.b))


class Quotient(CachedExpression):
    def __init__(self, a, b):
        super(Quotient, self).__init__()
        self.a = a
        self.b = b

    def _bind(self, binding):
        return operator.truediv(bind(self.a, binding), bind(self.b, binding))

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        db = differentiate(self.b, variable)
        return (self.b * da - self.a * db) / (self.b*self.b)

    def __repr__(self):
        return "(%s / %s)"%(repr(self.a), repr(self.b))


class Sum(CachedExpression):
    def __init__(self, a, b):
        super(Sum, self).__init__()
        self.a = a
        self.b = b

    def _bind(self, binding):
        return bind(self.a, binding) + bind(self.b, binding)

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        db = differentiate(self.b, variable)
        return da + db

    def __repr__(self):
        return "(%s + %s)"%(repr(self.a), repr(self.b))
