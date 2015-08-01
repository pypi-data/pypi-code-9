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

def node_count(node, cache=None):
    """
    >>> from ldb.algebra.expression import Variable
    >>> from ldb.algebra.math import cos
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> node_count(a+b+(a+b))
    7
    >>> c = a+b
    >>> node_count((c+1)+c)
    9
    >>> node_count(cos(a))
    2
    """
    if cache is None:
        cache = {}

    if id(node) in cache:
        return cache[id(node)]

    if not hasattr(node, 'children'):
        result = 1
    else:
        result = sum([node_count(child, cache) for child in node.children]) + 1

    cache[id(node)] = result
    return result


def node_count_unique(node, cache=None):
    """
    >>> from ldb.algebra.expression import Variable
    >>> from ldb.algebra.math import cos
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> node_count_unique(a+b+(a+b))
    5
    >>> c = a+b
    >>> node_count_unique((c+1)+c)
    6
    >>> node_count_unique(cos(a))
    2
    """
    if cache is None:
        cache = set()

    if id(node) in cache:
        return 0

    cache.add(id(node))

    if not hasattr(node, 'children'):
        result = 1
    else:
        result = sum([node_count_unique(child, cache)
                      for child in node.children]) + 1

    return result


def dict_sum(dict_sequence):
    """
    >>> dict_sum([{'a': 1}, {'a': 2, 'b': 1}])['a']
    3
    >>> dict_sum([{'a': 1}, {'a': 2, 'b': 1}])['b']
    1
    """
    keys = set.union(*[set(dict_.keys()) for dict_ in dict_sequence])

    return {k: sum([dict_.get(k, 0) for dict_ in dict_sequence]) for k in keys}


def node_usage(node, cache=None):
    """
    >>> from ldb.algebra.expression import Variable, Sum
    >>> a = Variable('a')
    >>> b = Variable('b')
    >>> node_usage(a+b)[Variable]
    2
    >>> node_usage(a+b)[Sum]
    1
    """
    if cache is None:
        cache = {}

    if id(node) in cache:
        return cache[id(node)]

    result = dict_sum([node_usage(child)
                       for child in getattr(node, 'children', [])] +
                      [{type(node): 1}])

    cache[id(node)] = result
    return result
