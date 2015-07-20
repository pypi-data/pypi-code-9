# -*- coding: utf-8 -*-
"""
========================================================================
Helper functions for testing (:mod:`sknano.testing._funcs`)
========================================================================

.. currentmodule:: sknano.testing._funcs

"""
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import importlib

from sknano.core.atoms import StructureAtom as Atom, StructureAtoms as Atoms
from sknano.core.refdata import element_symbols as periodic_table_of_elements
from sknano.generators import STRUCTURE_GENERATORS

__all__ = ['generate_atoms']


def generate_atoms(*args, elements=None, generator_class=None, **kwargs):
    """Helper function to generate sequence of atoms for testing purposes."""
    atoms = None
    if elements is not None:
        if isinstance(elements, str) and elements == 'periodic_table':
            elements = periodic_table_of_elements
        if isinstance(elements, list):
            atoms = Atoms()
            for e in elements:
                atoms.append(Atom(e))

    elif generator_class is not None and \
            generator_class in STRUCTURE_GENERATORS:
        try:
            generator = getattr(importlib.import_module('sknano.generators'),
                                generator_class)
            structure = generator(*args, **kwargs)
            atoms = structure.atoms
        except ImportError as e:
            print(e)

    return atoms
