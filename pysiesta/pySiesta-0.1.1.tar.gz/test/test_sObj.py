# Copyright (C) 2014 Ezequiel Castillo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
#import pysiesta
from .. import pysiesta
import unittest

class TestSiestaObj(unittest.TestCase):
    def setUp(self):
        self.cgDir = os.path.join(os.path.dirname(__file__), os.path.pardir, 'samples', 'siesta', 'cg')
        #self.cgDir = os.path.join('samples', 'siesta', 'cg')
    def testInstatiation(self):
        self.assertTrue(pysiesta.SiestaObj(siestaDir=self.cgDir),
                        msg='Everything was OK')

if __name__ == '__main__':
    unittest.main()
