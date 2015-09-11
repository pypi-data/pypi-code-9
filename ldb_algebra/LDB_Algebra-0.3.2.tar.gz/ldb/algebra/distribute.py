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
        sum_ += distribute(expression.children[0])
        sum_ += distribute(expression.children[1])
    elif isinstance(expression, Product):
        a = distribute(expression.children[0])
        b = distribute(expression.children[1])
        for a_term in a:
            for b_term in b:
                sum_.append((a_term[0]+b_term[0], a_term[1]+b_term[1]))
    elif isinstance(expression, Quotient):
        a = distribute(expression.children[0])
        sum_ += [(_[0], _[1]+[expression.children[1]]) for _ in a]
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

def divide_list(a, b):
    """
    divide(a, [b1, b2, b3, ..., bn]) - returns ([c1, c2, c3, ..., cn], d) when
    a is b1*c1 + b2*c2 + b3*c3 + ... + bn*cn + d where c1, c2, c3, ..., cn are
    general expressions and b1, b2, b3, ..., bn are expressions that can not
    be distributed (variables, functions like sqrt, sin, etc). Any valid b will
    have that property that distribute(b) == [([b], [])]

    Please note that if any bi*bj is in any term of a the divisor that gets used
    (bi/bj) will be arbitrary based on what the set data structure gives us.
    This may even be non-deterministic based on python's hash randomization.

    >>> from ldb.algebra.expression import Variable
    >>> b1 = Variable('b1')
    >>> b2 = Variable('b2')
    >>> b3 = Variable('b3')
    >>> c1 = Variable('c1')
    >>> c2 = Variable('c2')
    >>> c3 = Variable('c3')
    >>> d = Variable('d')
    >>> divide_list(b1*c1 + b2*c2 + b3*c3 + d, [b1, b2, b3])
    ([c1, c2, c3], d)
    """
    # TODO: Add more thorough tests
    term_set = set(b)
    idx_dict = {val:idx for idx, val in enumerate(b)}
    result = [[] for _ in b]
    d_terms = []

    for term in distribute(a):
        intersection = term_set.intersection(term[0])
        if len(intersection) > 0:
            b_val = intersection.pop()
            idx = idx_dict[b_val]
            term[0].remove(b_val)
            result[idx].append(term)
        else:
            d_terms.append(term)

    return [undistribute(_) for _ in result], undistribute(d_terms)
