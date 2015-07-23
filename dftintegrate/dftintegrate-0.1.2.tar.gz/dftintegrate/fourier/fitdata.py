"""Classes::
  FitData -- The FitData class is a collection of
    functions that fit a 3D function with a fourier series.

"""

import numpy as np
from json import dump, load
from scipy.linalg import lstsq
from itertools import product

from dftintegrate import customserializer as cs


class FitData(object):
    """
    Fit a periodic 3D function represented by a json file created by
    the ReadData object with fourier series, repersent the fit as an
    object.

    Solve A x = b where A is a matrix and x and b are column vectors.

    Variables::
      name -- Path to directory with data to work on.

      bandnum -- Number of bands to fit.

      data -- Data to fit represented in data.json.

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

      series -- Matrix representation of the series. "A" in the equation
        to solve.

      coeffs -- Fourier Coefficients in the Fourier series. "x" in the
        equation to solve. A dictionary, the key is the band number and
        the value is the list of coefficients for that band.

      recips -- Reciprocal lattice vectors in the Fourier sum.

      lstsq_err -- Total least squares error for the fit.

    Funtions::
      _get_fit -- Call gen_recips, gen_series, solve_coeffs, and
        serialize.

      gen_recips -- Generate the reciprocal lattice vectors.

      gen_series -- Generate the sines and cosines in the series in
        matrix form.

      solve_coeffs -- Use scipy.linalg.lstsq to solve A x = b for x.

      serialize -- Serialize the fit to a json file.

    """

    def __init__(self, name_of_directory, bandnum='all'):
        """
        Arguments::
          name_of_directory -- path to directory that contains the
            output from readdata.py

        Keyword Arguments::
          bandnum -- Number of bands to fit. Default is to fit all bands
            in data.json.
        """
        self.name = name_of_directory+'/'
        self.bandnum = bandnum
        with open(self.name+'data.json', mode='r',
                  encoding='utf-8') as inf:
            self.data = load(inf)
        self.kgrid = self.data['kgrid']
        self.eigenvals = self.data['eigenvals']
        self.symops = self.data['symops']
        self.kmax = int(self.data['kmax'])
        self._get_fit()

    def _get_fit(self):
        self.gen_recips()
        self.gen_series()
        self.solve_coeffs()
        self.serialize()

    def gen_recips(self):
        """
        In the Fourier basis representation we sum over the reciprocal
        lattice vectors; this function generates those reciprocal
        lattice vectors. Start by using itertools.product to create
        triplets in range 0 to kmax. In order to sum over the entire
        Fermi sphere we operate on the triplets with the systems
        symmetry operators given in symops. kmax and symops are
        explained in more detail in readdata.py

        Varibles::
          allList -- A list of all vectors seen. Including results of
            product and their rotated versions after being operated on
            by symops.

          recips -- A dictionary with the key being a unique vector and
            the value being a list of the symmetric versions of that
            unique vector.
        """
        allList = set()
        recips = {}
        # Loop over the positive octant in k-space.
        for v in product(range(self.kmax+1), repeat=3):
            # Tuple so it's hashable.
            v = tuple(v)

            # Check if it has been seen before, if so skip, if not add.
            if v not in allList:
                allList.add(v)
                recips[str(v)] = [list(v)]

                # Loop over all symops
                for i, matrix in enumerate(self.symops):
                    # Operate on it with the symop.
                    vRot = tuple(np.dot(matrix, v))

                    # Check if it has been seen before, if so skip, if not add.
                    if vRot not in allList:
                        vRot = tuple([int(x) for x in vRot])
                        allList.add(vRot)
                        recips[str(v)].append(list(vRot))

        self.recips = recips

    def gen_series(self):
        """
        In the equation A x = b where A is a matrix and x and b are
        column vectors, this function generates A. We use the matrix
        equation to fit the 3D function represented by kgrid and
        eigenvals. x is the coefficients to the complex exponentials and
        b contains the values of the function. Each entry in A is like
        exp(i2piG.r).
        """
        series = []
        i = 1j  # imaginary number
        pi = np.pi
        for kpt in self.kgrid:
            row = []
            for k, v in sorted(self.recips.items()):
                # The 2pi comes from the dot product of real and reciprocal
                # space lattice vectors. v is a list of reciprocal lattice
                # vectors that are symetric and therefore need to have the same
                # coefficient so they are summed together.
                gdotr = i*2*pi*np.dot(v, kpt)
                row.append(sum(np.exp(gdotr)))
            series.append(row)
        self.series = series

    def solve_coeffs(self):
        """
        Solve A x = b with scipy.linalg.lstsq. A is a matrix, see
        gen_series for more detail. x is the column vector we are
        solving for, it is the Fourier coefficients. b is a column
        vector, it is the energy values of the bands.
        """
        # A (series), b (eigenvals)
        coeffs = {}
        lstsq_err = {}
        A = self.series
        if self.bandnum == 'all':
            self.bandnum = len(self.eigenvals.keys())
        else:
            self.bandnum = int(self.bandnum)
        for num in range(1, self.bandnum+1):
            num = str(num)
            b = self.eigenvals[num]
            coeffs[num], lstsq_err[num] = np.array(lstsq(A, b)[:2])
        self.coeffs = coeffs
        self.lstsq_err = lstsq_err

    def serialize(self):
        fit_dict = {'coefficients': self.coeffs, 'reciprocals': self.recips,
                    'series': self.series}
        with open(self.name+'fit.json', mode='w', encoding='utf-8') as outf:
            dump(fit_dict, outf, indent=2, default=cs.tojson)
