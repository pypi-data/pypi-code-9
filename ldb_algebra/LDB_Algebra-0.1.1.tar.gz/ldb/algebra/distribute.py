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

from expression import *

def distribute(expression):
    """
    >>> from ldb.algebra.expression import Variable
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> distribute(a+b)
    [([a], []), ([b], [])]
    >>> distribute(a*b)
    [([a, b], [])]
    >>> distribute(a/b)
    [([a], [b])]
    """
    # TODO: Add more thorough tests
    # List of (numerator product terms, denominator product terms) empty lists
    # in tuple interpreted as 1.0
    sum_ = []
    if isinstance(expression, Sum):
        sum_ += distribute(expression.a)
        sum_ += distribute(expression.b)
    elif isinstance(expression, Product):
        a = distribute(expression.a)
        b = distribute(expression.b)
        for a_term in a:
            for b_term in b:
                sum_.append((a_term[0]+b_term[0], a_term[1]+b_term[1]))
    elif isinstance(expression, Quotient):
        a = distribute(expression.a)
        sum_ += [(_[0], _[1]+[expression.b]) for _ in a]
    else:
        sum_.append(([expression], []))

    return sum_

def undistribute_product(product_):
    if len(product_) == 0:
        return 1.0

    result = product_[0]

    for term in product_[1:]:
        result *= term

    return result

def undistribute_quotient(numerator, denominator):
    num_expr = undistribute_product(numerator)

    if len(denominator) == 0:
        return num_expr
    else:
        return num_expr / undistribute_product(denominator)

def undistribute(sum_):
    """
    >>> from ldb.algebra.expression import Variable
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> undistribute([([a], []), ([b], [])])
    (a + b)
    >>> undistribute([([a, b], [])])
    (a * b)
    >>> undistribute([([a], [b])])
    (a / b)
    """
    # TODO: Add more thorough tests
    if len(sum_) == 0:
        return 0

    result = undistribute_quotient(*sum_[0])

    for term in sum_[1:]:
        result += undistribute_quotient(*term)

    return result

def divide(a, b):
    """
    divide(a, b) - returns (c, d) for expression b*c+d, b should be something
    that distributes to [([b], [])]
    >>> from ldb.algebra.expression import Variable
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> c = Variable('c')
    >>> divide(a*b+c, a)
    (b, c)
    """
    # TODO: Add more thorough tests
    c_terms = []
    d_terms = []

    for term in distribute(a):
        if b in term[0]:
            term[0].remove(b)
            c_terms.append(term)
        else:
            d_terms.append(term)

    return (undistribute(c_terms), undistribute(d_terms))
