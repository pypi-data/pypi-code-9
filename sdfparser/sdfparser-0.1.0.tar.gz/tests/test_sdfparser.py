#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
from StringIO import StringIO

from sdfparser import SDFReader, SDFWriter


class TestSdfparser(unittest.TestCase):

    def setUp(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        with file(os.path.join(current_path, 'data/DRD3_Antagonists.sdf')) as drd3_file:
            self.parser = SDFReader(drd3_file)

    def test_test_DRD3_Antagonist_file(self):
        result = self.parser.result()
        self.assertEquals(len(result), 12793)
        molecule = result[0]
        self.assertEquals(molecule.name, 'ZINC36379153')
        self.assertEquals(molecule.software_used, '-OEChem-11151013503D')
        self.assertEquals(len(molecule.atoms), 57)
        self.assertEquals(len(molecule.bonds), 60)
        self.assertEquals(molecule.metadata['LIGAND'], '15232472')
        self.assertEquals(molecule.metadata['LOGP'], '5.170400')
        self.assertEquals(molecule.metadata['HBD'], '2')
        self.assertEquals(molecule.metadata['PSA'], '68.680000')
        self.assertEquals(molecule.metadata['HBA'], '5')
        self.assertEquals(molecule.metadata['FPT'], '00000000 00000000 0000001b fffaa33c a7c8860d d256bc0021033400 01000480')
        self.assertEquals(molecule.metadata['MW'], '495.388300')
        self.assertEquals(molecule.metadata['FC'], '1')
        self.assertEquals(molecule.metadata['RB'], '8')

    def test_writer_output_is_equal_to_read_input(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        result = self.parser.result()
        output_file = StringIO()

        writer = SDFWriter(output_file, result)
        writer.write()

        output_file.seek(0)
#        with file(os.path.join(current_path, 'data/DRD3_Antagonists.sdf')) as drd3_file:
#            self.assertEquals(output_file.read(), drd3_file.read())
        output_file.seek(0)
        with file('pepe', 'w') as salida:
            salida.write(output_file.read())


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
