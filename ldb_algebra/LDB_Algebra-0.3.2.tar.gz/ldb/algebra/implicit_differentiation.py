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

from ldb.lapack.lapack import Matrix, Vector, dgesv, LAPACKTypeEnum
import ldb.algebra.expression
from ldb.algebra.expression import bind
from ldb.algebra.distribute import divide_list

def chain_differentiate(expression, differentiation):
    """
    >>> from ldb.algebra.expression import Variable
    >>> x = Variable('x')
    >>> chain_differentiate(x*x, [x, x])
    2
    >>> y = Variable('y')
    >>> chain_differentiate(x*x*y, [x, y])
    (x + x)
    """
    if len(differentiation) == 0:
        return expression
    else:
        next_diff = ldb.algebra.expression.differentiate(expression,
                                                         differentiation[0])
        return chain_differentiate(next_diff, differentiation[1:])

def differentiate(equations, dependent_variables, differentiation, binding):
    """
    z = 2 y^3 + 3 x^2
    z2 = 15 sqrt(y) + 5 x
    F1 = z^2 - (4 y^6 + 12 y^3 x^2 + 9 x^4)
    F2 = z2 - z - (15 sqrt(y) + 5x) + (2 y^3 + 3 x^2)

    >>> from ldb.algebra.expression import Variable, differentiate as diff
    >>> from ldb.algebra.function import Function
    >>> from ldb.algebra.math import sqrt
    >>> x = Variable('x')
    >>> y = Variable('y')
    >>> z = Function('z')
    >>> z2 = Function('z2')
    >>> dz_dx = diff(z, x)
    >>> dz2_dx = diff(z2, x)
    >>> F1 = z*z - (4*y**6 + 12*y**3*x**2 + 9*x**4)
    >>> F2 = z2 - z - (15*sqrt(y) + 5*x) + (2*y**3 + 3*x**2)
    >>> differentiate([F1, F2], [z, z2], [x], {x: 2, y: 9, z: 1470, z2: 55})
    [12.0, 5.0]
    >>> differentiate([F1, F2], [z, z2], [x, x], {x: 2, y: 9, z: 1470, z2: 55})
    [6.0, 0.0]
    """
    assert len(equations) == len(dependent_variables)

    dF_diff = [chain_differentiate(equation, differentiation) for
               equation in equations]
    ddep_diff = [chain_differentiate(dependent_variable, differentiation) for
                 dependent_variable in dependent_variables]

    total_binding = dict(binding)

    # TODO: memoize the intermediate values
    for i in range(1, len(differentiation)):
        this_differentiation = differentiation[0:i]
        extra_binding_vars = [chain_differentiate(dependent_variable,
                                                  this_differentiation) for
                              dependent_variable in dependent_variables]
        extra_binding_values = differentiate(equations, dependent_variables,
                                              this_differentiation,
                                              total_binding)
        these_extra_bindings = {var:value for var, value
                                in zip(extra_binding_vars,
                                       extra_binding_values)}
        total_binding.update(these_extra_bindings)

    coefficient_matrix = Matrix(LAPACKTypeEnum.double, len(equations),
                                len(dependent_variables))
    right_hand_side = Vector(LAPACKTypeEnum.double, len(equations))

    for row, diff_eq in enumerate(dF_diff):
        coeffs, remainder = divide_list(diff_eq, ddep_diff)
        try:
            for column, coeff in enumerate(coeffs):
                coefficient_matrix[row, column] = bind(coeff, total_binding)
        except TypeError:
            raise Exception, 'Unbound value: '+str(bind(coeff, total_binding))

        try:
            right_hand_side[row] = -bind(remainder, total_binding)
        except TypeError:
            raise Exception, ('Unbound value: ' + str(bind(remainder,
                                                           total_binding))
                              + ' with binding: ' + str(total_binding))

    dgesv(coefficient_matrix, right_hand_side)

    return list(right_hand_side)
