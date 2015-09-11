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

import operator
import ast

import ldb.algebra.manager

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
        try:
            hash(key)
        except TypeError:
            # No point in any of this if we can't store in dictionary
            return

        if key in self.order:
            self.order.remove(key)
        elif len(self.order) >= self.max_len:
            to_kill = self.order[0]
            del self.cache[to_kill]
            del self.order[0]

        self.cache[key] = val
        self.order.append(key)


def make_function(expression, order):
    return_expression = expression.ast()
    imports = expression.ast_imports()
    return_statement = ast.Return(return_expression, lineno=1)
    args = [ast.Name(id=var_name, ctx=ast.Param()) for var_name in order]
    func = ast.FunctionDef(name='f', args=ast.arguments(args, None, None, []),
                           body=[return_statement], decorator_list=[], lineno=1)
    import_aliases = [ast.alias(name=import_name, asname=None)
                      for import_name in imports]
    module = ast.Module(body=[ast.ImportFrom("__future__",
                                             [ast.alias(name="division",
                                                        asname=None)], 0)] +
                             [ast.Import(import_aliases) for _ in [1]
                              if len(import_aliases) > 0] + 
                             [func])

    ast.fix_missing_locations(module)

    module_compiled = compile(module, filename='<ast>', mode='exec')

    my_globals = {}

    exec module_compiled in my_globals, None

    return my_globals['f']


def ast_(expression):
    try:
        return expression.ast()
    except:
        return ast.Num(expression)


def bind_kw(expression, **binding):
    return bind(expression, binding)

def bind(expression, binding):
    if hasattr(expression, 'bind'):
        return expression.bind(binding)
    else:
        return expression


def differentiate(expression, variable):
    if hasattr(expression, 'differentiate'):
        return expression.differentiate(variable)
    else:
        return 0


class Expression(object):
    _manager = ldb.algebra.manager.ExpressionManager()

    def __init__(self):
        pass

    def ast_imports(self):
        return set(())

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

    def __pow__(self, other):
        return Power(self, other)


class Variable(Expression):
    def __init__(self, var_name):
        self.var_name = var_name
        self.support = set((self,))

    def ast(self):
        return ast.Name(self.var_name, ast.Load())

    def bind(self, binding):
        if self in binding:
            return binding[self]
        elif self.var_name in binding:
            return binding[self.var_name]
        else:
            return self

    def differentiate(self, variable):
        if self == variable or self.var_name == variable:
            return 1
        else:
            return 0

    def __hash__(self):
        return hash(self.var_name)

    def __eq__(self, other):
        try:
            return self.var_name == other.var_name
        except:
            return False

    def __repr__(self):
        return self.var_name


class VectorVariableIndexed(Expression):
    def __init__(self, vector_variable, indexer):
        self.vector_variable = vector_variable
        self.indexer = indexer
        self.support = set((self,))

    def bind(self, binding):
        if self in binding:
            return binding[self][self.indexer]

        vector_variable_name = self.vector_variable.vec_var_name
        if vector_variable_name in binding:
            return binding[vector_variable_name][self.indexer]
        else:
            return self

    # TODO: Implement differentiation


class VectorVariable(object):
    def __init__(self, vec_var_name, length):
        self.vec_var_name = vec_var_name
        self.length = length

    def __getitem__(self, index):
        return VectorVariableIndexed(self, index)

    def __iter__(self):
        for i in xrange(self.length):
            yield self[i]

    def __len__(self):
        return self.length


class CachedExpression(Expression):
    def __init__(self, children, comparable):
        self.children = children
        self.comparable = comparable

        self.support = set()
        for child in self.children:
            self.support |= getattr(child, 'support', set())

        self._binding_cache = MethodCache()
        self._differentiate_cache = MethodCache()

    def ast_imports(self):
        imports = self.ast_extra_imports()
        for child in self.children:
            try:
                imports |= child.ast_imports()
            except:
                pass

        return imports

    def ast_extra_imports(self):
        return set(())

    def bind(self, binding):
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

    def __hash__(self):
        return hash(self.comparable)

    def __eq__(self, other):
        try:
            return self.comparable == other.comparable
        except:
            return False


class Product(CachedExpression):
    def __init__(self, a, b):
        super(Product, self).__init__((a,b), ('Product', frozenset((a, b))))

    def ast(self):
        return ast.BinOp(ast_(self.children[0]), ast.Mult(),
                         ast_(self.children[1]))

    def _bind(self, binding):
        return bind(self.children[0], binding) * bind(self.children[1], binding)

    def _differentiate(self, variable):
        a = self.children[0]
        b = self.children[1]
        da = differentiate(a, variable)
        db = differentiate(b, variable)
        return b * da + a * db

    def __repr__(self):
        return "(%s * %s)"%(repr(self.children[0]), repr(self.children[1]))


class Quotient(CachedExpression):
    def __init__(self, a, b):
        super(Quotient, self).__init__((a,b), ('Quotient', (a, b)))

    def ast(self):
        return ast.BinOp(ast_(self.children[0]), ast.Div(),
                         ast_(self.children[1]))

    def _bind(self, binding):
        return operator.truediv(bind(self.children[0], binding),
                                bind(self.children[1], binding))

    def _differentiate(self, variable):
        a = self.children[0]
        b = self.children[1]
        da = differentiate(a, variable)
        db = differentiate(b, variable)
        return (b * da - a * db) / (b*b)

    def __repr__(self):
        return "(%s / %s)"%(repr(self.children[0]), repr(self.children[1]))


class Sum(CachedExpression):
    def __init__(self, a, b):
        super(Sum, self).__init__((a,b), ('Sum', frozenset((a, b))))

    def ast(self):
        return ast.BinOp(ast_(self.children[0]), ast.Add(),
                         ast_(self.children[1]))

    def _bind(self, binding):
        return bind(self.children[0], binding) + bind(self.children[1], binding)

    def _differentiate(self, variable):
        a = self.children[0]
        b = self.children[1]
        da = differentiate(a, variable)
        db = differentiate(b, variable)
        return da + db

    def __repr__(self):
        return "(%s + %s)"%(repr(self.children[0]), repr(self.children[1]))


class Power(CachedExpression):
    def __init__(self, a, b):
        super(Power, self).__init__((a,b), ('Power', (a, b)))

    def ast(self):
        return ast.BinOp(ast_(self.children[0]), ast.Pow(),
                         ast_(self.children[1]))

    def _bind(self, binding):
        return (bind(self.children[0], binding) **
                bind(self.children[1], binding))

    def _differentiate(self, variable):
        import ldb.algebra.math

        a = self.children[0]
        b = self.children[1]
        da = differentiate(a, variable)
        db = differentiate(b, variable)
        return (da * b * (a ** (b - 1)) +
                db * ldb.algebra.math.log(a) * (a ** b))

    def __repr__(self):
        return "(%s ** %s)"%(repr(self.children[0]), repr(self.children[1]))
