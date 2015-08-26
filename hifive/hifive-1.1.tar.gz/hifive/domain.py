#!/usr/bin/env python

"""A set of classes for handling HiC domain calling."""

import os
import sys

import numpy
import h5py


class Arrowhead(object):

    """
    This class calculates the arrowhead transformation and domain calling described by Rao et al. (2014).

    This class stores a list of chromosomes, a dictionary for converting from chromosome label to integer and back, fragment starts, stops, and chromosome number in an h5dict.
        
    .. note::
      This class is also available as hifive.Fend

    When initialized, this class creates an h5dict in which to store all data associated with this object.

    :param filename: The file name of the h5dict. This should end with the suffix '.hdf5'
    :type filename: str.
    :param mode: The mode to open the h5dict with. This should be 'w' for creating or overwriting an h5dict with name given in filename.
    :type mode: str.
    :param silent: Indicates whether to print information about function execution for this object.
    :type silent: bool.
    :returns: :class:`Fend <hifive.fend.Fend>` class object

    :attributes: * **file** (*str.*) - A string containing the name of the file passed during object creation for saving the object to.
                 * **silent** (*bool.*) - A boolean indicating whether to suppress all of the output messages.
                 * **history** (*str.*) - A string containing all of the commands executed on this object and their outcome.
    """

    def __init__(self, hic, binsize, chroms=None):
        """Create an arrowhead domain object."""
        self.binsize = binsize
        if chroms is None:
            self.chroms = hic.chr2int.keys()
            self.chroms.sort()
        else:
            self.chroms = chroms
        self.matrices = {}
        for chrom in self.chroms:
            self.calculate_transformation(hic, chrom)

    def calculate_transformation(self, hic, chrom):
        """Calculate the arrowhead-transformed matrix.

        :param hic: A :class:`HiC <hifive.hic.HiC>` class object.
        :type hic: :class:`HiC <hifive.hic.HiC>`
        :param chrom: The chromosome for which the transformatio is calculated.
        :type chrom: str.
        returns None
        """
        data, mapping = hic.cis_heatmap(chrom, binsize=self.binsize, datatype='fend', arraytype='upper',
                                        returnmapping=True)
        data = data[:, 0] / data[:, 1]
        













