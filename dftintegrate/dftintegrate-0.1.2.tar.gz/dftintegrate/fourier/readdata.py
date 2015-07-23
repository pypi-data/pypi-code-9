"""
Classes::
  ReadData -- A collection of functions to collect extracted VASP/QE data
    into a json file.
"""

import json
from copy import deepcopy
from ast import literal_eval
from collections import defaultdict


class ReadData(object):
    """
    A collection of functions to collect extracted VASP/QE data
    into a json file.

    Variables::
      name -- A string containing the name to the extracted data.

      kmax -- A number that determines how many terms can be used
        in the fourier representation based on the density of the
        sample points.

      kgrid -- A list of lists. Each inner list is a triplet that
        represents a k-point. The outer list is the collection of
        the triplets or k-points and therefore represents the k-kgrid.
        Note these are the irreducibl k-points.

      weights -- A list of floats. Since kgrid represents the
        irreducible wedge, each k-point has a weight that
        represents in a way how degenerate it is. These
        are in the same order as their corresponding k-point
        in kgrid.

      eigenvals -- A dictionary. At each k-point there is an
        eigenvalue (energy) for each band that was calculated. The
        keys are the band number and the values are a list of
        energies for that band at each k-point.

      symops -- A triple nested list. The outer list is a collection
        matrices that represent the symmetry operators for the
        system calculated. The inner double nested lists are
        representations of the matrices.

      trans -- A list of lists. Each symmetry operator has a
        translation vector associated with it. We aren't sure
        what they are for but we have them so we can implement
        them if we figure it out.

    Functions::
      _read_lines -- Read a file yielding one line at a time. Generator.

      read_kpts_eigenvals -- Read kpts_eigenvals.dat in as a list of
            k-points and a dictionary.

      read_symops_trans -- Read symops_trans.dat in as two lists.

      read_kmax -- Read kmax from kmax.dat in. For exampl one might run
        a calulation with a grid of 4 4 4, in this case k is 4. This
        is needed in the Fourier basis fit to ensure the highest
        frequency term doens't exceed the Nyquist frequency. This means
        that the highest frequency can't exeed k/2; so if k is 4
        then the highest frequency can't exeed 2. Since we are in 3D we
        have to consider sqrt(x^2+x^2+x^2) < k/2, thus
        x = kmax = ceil(k/(2sqrt(3)).

      serialize -- Serialize the data to a json file.

    """

    def __init__(self, name_of_data_directory):
        """
        Arguments::
          name_of_data_directory -- A string containing the name to
            the VASP data.
        """
        self.name = name_of_data_directory
        self.read_kpts_eigenvals()
        self.read_symops_trans()
        self.read_kmax()
        self.serialize()

    def _read_lines(self, path_to_file):
        """
        Read file, yield line by line.

        Arguments::
          path_to_file -- String containing the path to the file.
        """
        with open(path_to_file) as inf:
            for line in inf:
                yield [literal_eval(x) for x in line.strip().split()]

    def read_kpts_eigenvals(self):
        """
        Read in kpts_eigenvals.dat with _read_lines. Stores the k-pionts
        in kgrid, the weights in weights, and the band energy
        (eigenvalues) in eigenvals. See this class's (ReadData)
        docstring for more details on kgrid, weights, and eigenvals.
        """
        name = self.name
        kgrid = []
        weights = []
        eigenvals = defaultdict(list)
        for line in self._read_lines(name + '/kpts_eigenvals.dat'):
            if len(line) == 4:
                kgrid.append(line[:3])
                weights.append(line[-1])
            elif len(line) == 2:
                eigenvals[line[0]].append(line[1])
        self.kgrid = kgrid
        self.weights = weights
        self.eigenvals = eigenvals

    def read_symops_trans(self):
        """
        Read in symops_trans.dat with _read_lines. Stores the symmetry
        operators in symops and the translations in trans. See this
        class's (ReadData) docstring for more details on symops and trans.
        """
        name = self.name
        symops = []
        symop = []
        trans = []
        lines = self._read_lines(name + '/symops_trans.dat')
        for line in lines:
            symop.append(line)
            symop.append(next(lines))
            symop.append(next(lines))
            next(lines)
            tran = next(lines)
            next(lines)
            symops.append(deepcopy(symop))
            trans.append(tran)
            symop.clear()
        self.symops = symops
        self.trans = trans

    def read_kmax(self):
        """
        Read in kmax.dat using _read_lines. Only the first line will beh
        read. It will be assigned to self.kmax.
        """
        name = self.name
        lines = self._read_lines(name + '/kmax.dat')
        self.kmax = next(lines)[0]

    def serialize(self):
        data_dict = {'kmax': self.kmax, 'kgrid': self.kgrid,
                     'weights': self.weights, 'eigenvals': self.eigenvals,
                     'symops': self.symops, 'trans': self.trans}
        with open(self.name + '/data.json', mode='w',
                  encoding='utf-8') as outf:
            json.dump(data_dict, outf, indent=2)
