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

def node_count(node):
    """
    >>> from ldb.algebra.expression import Variable
    >>> from ldb.algebra.math import cos
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> node_count(a+b)
    3
    >>> node_count(cos(a))
    2
    """
    if not hasattr(node, 'children'):
        return 1
    return sum([node_count(child) for child in node.children]) + 1

def dict_sum(dict_sequence):
    """
    >>> dict_sum([{'a': 1}, {'a': 2, 'b': 1}])['a']
    3
    >>> dict_sum([{'a': 1}, {'a': 2, 'b': 1}])['b']
    1
    """
    keys = set.union(*[set(dict_.keys()) for dict_ in dict_sequence])

    return {k: sum([dict_.get(k, 0) for dict_ in dict_sequence]) for k in keys}

def node_usage(node):
    """
    >>> from ldb.algebra.expression import Variable, Sum
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> node_usage(a+b)[Variable]
    2
    >>> node_usage(a+b)[Sum]
    1
    """
    return dict_sum([node_usage(child)
                     for child in getattr(node, 'children', [])] +
                    [{type(node): 1}])
