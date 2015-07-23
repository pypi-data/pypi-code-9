"""Classes::
  EvaluateFit -- The EvaluateFit class is a collection of
    functions that allows you evaluate a fourier representation
    of a function created by FitData (fit.json) at arbitrary points.

"""

import numpy as np
from json import load

from dftintegrate import customserializer as cs
from dftintegrate.fourier import fitdata


class EvaluateFit(object):
    """
    Evaluate a fourier representation of a 3D function created by the
    FitData object.

    Solve A x = b where A is a matrix and x and b are column vectors.

    Variables::
      name -- Path to directory with data to work on.

      bandnum -- Number of bands to fit.

      data -- Data to fit represented in data.json.

      kgrid -- A list of lists. Each inner list is a triplet that
        represents a k-point. The outer list is the collection of
        the triplets or k-points and therefore represents the k-kgrid.
        This is set to the points you want to evaluate the fit at in 
        "evaluate."

      series -- Matrix representation of the series. "A" in the equation
        to solve.

      coeffs -- Fourier Coefficients in the Fourier series. "x" in the
        equation to solve. A dictionary, the key is the band number and
        the value is the list of coefficients for that band.

      recips -- Reciprocal lattice vectors in the Fourier sum.

    Funtions::
      __evaluatefit -- Generates "A" by calling FitData.gen_series
        and sets "x" to the coeffs for a particular band. Solves for "b"
        by finding the dot product of "A" and "x".

      evaluate -- Sets kgrid to points you wish to evaluate fit at.
        Recursively calls __evaluatefit according to specified number of
        bands. Returns dictionary of results.

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
        with open(self.name+'fit.json', mode='r',
                  encoding='utf-8') as inf:
            self.data = load(inf, object_hook=cs.fromjson)
        self.recips = self.data['reciprocals']
        self.coeffs = self.data['coefficients']

    def _evaluatefit(self):
        """
        Use A x = b to solve for b. First generate A with fitdata's
        gen_series. x is the coefficients that correspond to the
        band we are currently calculating (num).
        """
        fitdata.FitData.gen_series(self)
        A = self.series
        x = self.coeffs[self.num]
        return(np.dot(A, x))

    def evaluate(self, points):
        fiteval = {}
        self.kgrid = points
        if self.bandnum == 'all':
            for num in range(1, len(self.coeffs.keys())+1):
                self.num = num
                fiteval[num] = self._evaluatefit()
        else:
            for num in range(1, self.bandnum+1):
                self.num = str(num)
                fiteval[num] = self._evaluatefit()
        return fiteval
