# -*- coding: utf-8 -*-


class Molecule(object):

    def __init__(self, name):
        self.name = name
        self.atoms = []
        self.bonds = []
        self.properties = []
        self.metadata = {}

    def add_atom(self, atom):
        self.atoms.append(atom)

    def add_bond(self, bond):
        self.bonds.append(bond)

    def add_metadata(self, name, value):
        self.metadata[name] = value

    def add_property(self, prop):
        self.properties.append(prop)
