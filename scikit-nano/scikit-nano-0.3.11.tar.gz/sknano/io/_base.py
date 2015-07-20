# -*- coding: utf-8 -*-
"""
=============================================================================
Base classes for structure data (:mod:`sknano.io._base`)
=============================================================================

.. currentmodule:: sknano.io._base

"""
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
__docformat__ = 'restructuredtext en'

from abc import ABCMeta, abstractmethod

from sknano.core import get_fpath
from sknano.core.atoms import StructureAtom as Atom, StructureAtoms as Atoms
# from sknano.utils.analysis import StructureAnalyzer
from sknano.version import release, full_version, git_revision

version = full_version
if not release:
    version = '-'.join((full_version, git_revision[:7]))

default_comment_line = \
    'Structure data generated using scikit-nano version {}'.format(version)
default_structure_format = 'xyz'
supported_structure_formats = ('xyz', 'data', 'dump')

__all__ = ['Atom', 'Atoms',
           'StructureData',
           'StructureIO',
           'StructureReader',
           'StructureWriter',
           'StructureConverter',
           'StructureIOError',
           'StructureFormatSpec',
           'default_comment_line',
           'default_structure_format',
           'supported_structure_formats']


class StructureData:
    """Container class for structure data."""
    def __init__(self):
        self._atoms = Atoms()
        super().__init__()

    @property
    def atoms(self):
        return self._atoms

    def __getattr__(self, name):
        if name != '_atoms':
            return getattr(self._atoms, name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._atoms, name, value)

    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            delattr(self._atoms, name)


class StructureIO:
    """Base class for structure data file input and output.

    Parameters
    ----------
    fpath : {None, str}, optional

    """
    def __init__(self, fpath=None, fname=None, **kwargs):
        self.comment_line = default_comment_line
        if fpath is None and fname is not None:
            fpath = fname
        self.fpath = fpath
        self.kwargs = kwargs
        self.structure_data = StructureData()

    @property
    def comment_line(self):
        """Comment line."""
        return self._comment_line

    @comment_line.setter
    def comment_line(self, value):
        """Set the comment line string.

        Parameters
        ----------
        value : str

        """
        if not isinstance(value, str):
            raise TypeError('Expected a string.')
        self._comment_line = value

    @comment_line.deleter
    def comment_line(self):
        del self._comment_line

    def __getattr__(self, name):
        return getattr(self.structure_data, name)

    def __deepcopy__(self, memo):
        from copy import deepcopy
        cp = self.__class__(None)
        memo[id(self)] = cp
        for attr in dir(self):
            if not attr.startswith('_'):
                setattr(cp, attr, deepcopy(getattr(self, attr), memo))
        return cp


class StructureReader:
    """Structure data reader base class."""
    @classmethod
    def read(cls, fpath, structure_format=None, **kwargs):
        """Read structure data from file.

        Parameters
        ----------
        fpath : str
        structure_format : {None, str}
        """
        if (structure_format is None and fpath.endswith('.data')) or \
                structure_format == 'data':
            from ._lammps_data_format import DATAReader
            return DATAReader(fpath, **kwargs)
        elif (structure_format is None and fpath.endswith('.dump')) or \
                structure_format == 'dump':
            from ._lammps_dump_format import DUMPReader
            return DUMPReader(fpath, **kwargs)
        elif (structure_format is None and fpath.endswith('.xyz')) or \
                structure_format == 'xyz':
            from ._xyz_format import XYZReader
            return XYZReader.read(fpath)
        else:
            raise StructureIOError("Unable to determine `structure_format`")


class StructureWriter:
    """Structure data writer base class."""
    @classmethod
    def write(cls, fname=None, atoms=None, structure_format=None, **kwargs):
        """Write structure data to file.

        Parameters
        ----------
        fname : str, optional
        atoms : `~sknano.core.atoms.Atoms` instance
        structure_format : {None, str}, optional

        """
        if fname is None and structure_format is None:
            structure_format = default_structure_format

        if fname is None:
            fname = get_fpath(fname='structure_data', ext=structure_format,
                              add_fnum=True)

        if (structure_format is None and fname.endswith('.data')) or \
                structure_format == 'data':
            from ._lammps_data_format import DATAWriter
            DATAWriter.write(fname=fname, atoms=atoms, **kwargs)
        elif (structure_format is None and fname.endswith('.dump')) or \
                structure_format == 'dump':
            from ._lammps_dump_format import DUMPWriter
            DUMPWriter.write(fname=fname, atoms=atoms, **kwargs)
        #elif (structure_format is None and fname.endswith('.xyz')) or \
        #        structure_format == 'xyz':
        else:
            from ._xyz_format import XYZWriter
            XYZWriter.write(fname=fname, atoms=atoms, **kwargs)


class StructureConverter(metaclass=ABCMeta):
    """Abstract base class for converting structure data.

    Parameters
    ----------
    infile : str
    outfile : str

    """

    def __init__(self, infile=None, outfile=None, **kwargs):
        self.infile = infile
        self.outfile = outfile
        self.kwargs = kwargs

    @abstractmethod
    def convert(self):
        """Convert structure data from one format to another format."""
        raise NotImplementedError('Subclasses of `StructureConverter` need '
                                  'to implement the `convert` method.')


class StructureFormatSpec:
    """Base class for defining a format specification.

    Parameters
    ----------

    """
    def __init__(self, **kwargs):
        pass


class StructureIOError(Exception):
    """Base class for `StructureIO` errors."""
    pass
