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

import unittest

from ldb.lapack._lapack import ffi, lib

class SimpleUnitTest(unittest.TestCase):
    def setUp(self):
        self.n = ffi.new('int *')
        self.nrhs = ffi.new('int *')
        self.lda = ffi.new('int *')
        self.ldb = ffi.new('int *')
        self.info = ffi.new('int *')

    def test_dgesv_(self):
        ipiv = ffi.new('int[]', 3)
        a = ffi.new('double[]', 9)
        b = ffi.new('double[]', 3)

        self.n[0] = 3
        self.nrhs[0] = 1
        a[0] = 0; a[3] = 2.0; a[6] = 0
        a[1] = 0.5; a[4] = 0; a[7] = 0
        a[2] = 0; a[5] = 0; a[8] = 1.0
        self.lda[0] = 3
        b[0] = 1.3; b[1] = 7.5; b[2] = 3.1
        self.ldb[0] = 3

        lib.dgesv_(self.n, self.nrhs, a, self.lda, ipiv, b, self.ldb, self.info)

        self.assertEqual(0, self.info[0])
        self.assertEqual(15.0, b[0])
        self.assertEqual(0.65, b[1])
        self.assertEqual(3.1, b[2])

    def testStringLoad(self):
        self.assertIsNot(getattr(lib, 'dgesv_'), None)
