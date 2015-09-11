# Copyright 2015 Alex Orange
# 
# This file is part of LDB LAPACK.
# 
# LDB LAPACK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LDB LAPACK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with LDB LAPACK.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

from ldb.lapack._lapack import ffi, lib

class LAPACKType(object):
    def __init__(self, type_character, ctype_name):
        self.type_character = type_character,
        self.ctype_name = ctype_name

    def make_array(self, n):
        return ffi.new("%s[]"%(self.ctype_name,), n)


class LAPACKTypeEnum(object):
    float_ = LAPACKType('s', 'float')
    double = LAPACKType('d', 'double')
    complex_ = LAPACKType('c', 'float _Complex')
    complex_double = LAPACKType('z', 'float _Complex')


class Vector(object):
    def __init__(self, type_, length):
        self.type_ = type_
        self.length = length
        self._array = type_.make_array(self.length)

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, value):
        self._array[key] = value


class Matrix(object):
    def __init__(self, type_, rows, columns):
        self.rows = rows
        self.columns = columns
        self.type_ = type_
        self._array = type_.make_array(self.rows*self.columns)

    @property
    def size(self):
        return self.rows, self.columns

    def __getitem__(self, key):
        """
        Expects a row, column tuple to be passed in. For example:
        >>> m = Matrix(LAPACKTypeEnum.double, 2, 2)
        >>> m[1,1] = 2.0
        >>> m[1,1]
        2.0
        """
        return self._array[key[1]*self.rows + key[0]]

    def __setitem__(self, key, value):
        self._array[key[1]*self.rows + key[0]] = value


# TODO: LAPACK functions re-entrant or not?
# TODO: Check if allocations are wasting a lot of time or not
def dgesv(a, b):
    """
    >>> m = Matrix(LAPACKTypeEnum.double, 2, 2)
    >>> m[0,0] = 0.0; m[0,1] = 0.5
    >>> m[1,0] = 2.0; m[1,1] = 0.0
    >>> v = Vector(LAPACKTypeEnum.double, 2)
    >>> v[0] = 3.0
    >>> v[1] = 7.5
    >>> ipiv, info = dgesv(m, v)
    >>> info
    0
    >>> v[0]
    3.75
    >>> v[1]
    6.0
    """
    assert (a.type_.type_character == 'd',
            "Type character is '%s', not 'd'"%(a.type_.type_character,))
    assert (b.type_.type_character == 'd',
            "Type character is '%s', not 'd'"%(b.type_.type_character,))

    assert a.rows == a.columns

    n = ffi.new('int *')
    nrhs = ffi.new('int *')
    lda = ffi.new('int *')
    ipiv = ffi.new('int[]', a.rows)
    ldb = ffi.new('int *')
    info = ffi.new('int *')

    n[0] = a.rows
    nrhs[0] = 1 # TODO: Support multiple rhs's
    lda[0] = a.rows # TODO: Understand what this and ldb are for
    ldb[0] = len(b)

    lib.dgesv_(n, nrhs, a._array, lda, ipiv, b._array, ldb, info)

    return list(ipiv), info[0]
