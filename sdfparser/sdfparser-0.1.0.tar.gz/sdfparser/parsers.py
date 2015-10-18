# -*- coding: utf-8 -*-
import logging
from models import Molecule

logger = logging.getLogger(__name__)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


class SDFReader(object):

    def __init__(self, raw_file):
        self.raw_file = raw_file
        self.molecules = self._process_file()

    def _process_file(self):
        res = []
        raw_file = self.raw_file.read()
        raw_molecules = raw_file.split('$$$$')
        logger.info('Found {0} molecules in file'.format(len(raw_molecules)))
        for mol_no, raw_mol_data in enumerate(raw_molecules):
            data_field = None
            for line_no, raw_data in enumerate(raw_mol_data.lstrip('\n').split('\n')):
                raw_data = raw_data.strip()
                if line_no == 0:
                    logger.info('Processing molecule {0}'.format(raw_data))
                    current_mol = Molecule(name=raw_data)
                if line_no == 1:
                    current_mol.software_used = raw_data
                if line_no == 2:
                    current_mol.comments = raw_data
                if line_no == 3:
                    # counts line
                    current_mol.counts = raw_data
                    counts = filter(lambda elem: len(elem) > 0, raw_data.split(' '))
                    number_of_atoms_limit = int(counts[0]) + line_no
                    number_of_bonds_limit = number_of_atoms_limit + int(counts[1])

                if line_no > 3:
                    if line_no <= number_of_atoms_limit:
                        current_mol.add_atom(raw_data)

                    if line_no <= number_of_bonds_limit and line_no > number_of_atoms_limit:
                        current_mol.add_bond(raw_data)

                # properties
                if raw_data.startswith('M'):
                    current_mol.add_property(raw_data)

                # data fields. custom metadata
                if data_field:
                    current_mol.add_metadata(data_field, raw_data)
                    data_field = raw_data
                    data_field = None

                if raw_data.startswith('>'):
                    data_field = find_between(raw_data, '<', '>')

            res.append(current_mol)
        return res

    def result(self):
        return self.molecules


class SDFWriter(object):

    def __init__(self, file_obj, molecules):
        self.file_object = file_obj
        self.molecules = molecules

    def write(self):
        for molecule in self.molecules:
            if len(molecule.name) == 0:
                logger.warn('Trying to save empty molecule')
                continue
            self.file_object.write(molecule.name + '\n')
            self.file_object.write('  {0}\n'.format(molecule.software_used))
            self.file_object.write('\n')
            self.file_object.write(' {0}\n'.format(molecule.counts))
            for atom in molecule.atoms:
                self.file_object.write('   {0}\n'.format(atom))
            for bond in molecule.bonds:
                self.file_object.write('  {0}\n'.format(bond))
            for prop in molecule.properties:
                self.file_object.write(prop + '\n')
            for key, value in molecule.metadata.iteritems():
                self.file_object.write('> <{0}>\n'.format(key))
                self.file_object.write(value + '\n')
            self.file_object.write('$$$$\n')


class MOLReader(object):
    pass
