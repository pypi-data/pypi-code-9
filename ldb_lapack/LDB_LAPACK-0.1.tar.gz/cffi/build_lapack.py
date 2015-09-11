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

from cffi import FFI

ffi = FFI()

ffi.set_source("ldb.lapack._lapack",
               """
#include <complex.h>

extern void dgesv_(int* n, int* nrhs, double* a, int* lda, int* ipiv, double* b,
                   int* ldb, int* info);
               """,
               libraries=['lapack'])

ffi.cdef("""
extern void dgesv_(int* n, int* nrhs, double* a, int* lda, int* ipiv, double* b,
                   int* ldb, int* info);
         """)
