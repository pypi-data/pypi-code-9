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
from .. import molekule
import unittest

class TestMolekule(unittest.TestCase):
    def setUp(self):
        self.xyzFile = os.path.join(os.path.dirname(__file__), os.path.pardir, 'samples', 'system.xyz')
    def testFileLoading(self):
        self.assertTrue(molekule.Molecule(fromFile=self.xyzFile),
                        msg='Everything was OK')
    def testSpecies(self):
        mol = molekule.Molecule(fromFile=self.xyzFile)
        testAtom = mol.by_symbol('H')[0]
        self.failUnlessEqual(testAtom.specieNo, 2)

    def testZMatrix(self):
        mol = molekule.Molecule(fromFile=self.xyzFile)
        zm = molekule.ZMatrix(mol, firstAtom=mol[6])
        zm.set_atomsZmatrixType('molecule')
        zm.prepare_molecule()
        self.assertTrue(zm.write_toFile('system_siesta.zm'))


if __name__ == '__main__':
    unittest.main()
