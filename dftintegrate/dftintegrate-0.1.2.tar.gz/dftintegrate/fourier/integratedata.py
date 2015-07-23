"""
Classes::
  IntegrateData --  A collection of functions that integrate the fit
    created by FitData.
"""

import numpy as np

from itertools import product
from json import load, dump
from scipy.special.orthogonal import p_roots

from dftintegrate import customserializer as cs
from dftintegrate.fourier import fitdata


class IntegrateData(object):
    """Integrate the fourier representation of a 3D function contained in
    fit.json.

    Variables::
      name -- Path to directory with data to work on.

      bandnum -- Number of bands to work on.

      data -- Data to integrate represented in fit.json.

      points -- Number of integration points i.e. number of rectangles.

      coeffs -- Fourier Coefficients in the Fourier series. "x" in the
        equation to solve. A dictionary, the key is the band number and
        the value is the list of coefficients for that band.

      recips -- Reciprocal lattice vectors in the Fourier sum.

      rectangleintegrals -- A list of the integral of each band using
        the rectangle rule.

      gaussintegrals -- A list of the integral of each band using
        Gaussian quadrature.

    Functions::
      _integrate -- Call the functions to run the integration scheme.

      _evaluatefit -- Take the Fourier representation of the band and
        evaluate it at the integration points.

      _rectangleintegral -- Use the 3D analogue of the midpoint rule to
        integrate the Fourier representation of a band.

      _gaussintegral -- Use Gaussian Quadrature to integrate the Fourier
        representation of a band.

      rectangles -- Loop through the calculated bands and call
        _rectangleintegral.

      gauss -- Loop through the calculated bands and call _gaussintegral.

      serialize -- Serialize the integration to a json file.

    """
    def __init__(self, name_of_directory, points, bandnum='all'):
        """
        Arguments::
          name_of_directory -- path to directory that contains fit.json.

          points -- Number of integration points i.e. number of
            rectangles.

        Keyword Arguments::
          bandnum -- Number of bands to fit. Default is to integrate all
            bands in fit.json.
        """
        self.name = name_of_directory+'/'
        self.points = int(points)
        self.bandnum = bandnum
        with open(self.name+'fit.json', mode='r',
                  encoding='utf-8') as inf:
            self.data = load(inf, object_hook=cs.fromjson)
        self.recips = self.data['reciprocals']
        self.coeffs = self.data['coefficients']
        self.rectangleintegrals = []
        self.gaussintegrals = []
        self._integrate()

    def _integrate(self):
        self.rectangles()
        self.gauss()
        self.serialize()

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

    def _rectangleintegral(self):
        """Since we are integrating a 3D function this isn't technically
        the rectangle method, but it is the same idea. The whole idea is
        to make a bunch of cubes that tile space then evaluate the
        function at the center of each cube and add them up and call
        that the integral.
        """
        b = self._evaluatefit()
        divs = len(b)
        volume = 1/divs
        integral = sum(b*volume)
        self.rectangleintegrals.append(integral)

    def _gaussintegral(self):
        """
        Integrate over the interval 0 to 1. Evaluate the fit on that
        kgid, multiply function value by the weights.

        """
        b = self._evaluatefit()
        # For even functions do 8*np.power...
        integral = np.power((self.end-self.start)/2, 3) * \
            sum(np.multiply(b, self.weights))
        self.gaussintegrals.append(integral)

    def rectangles(self):
        """Generate a grid to evaluate the function on, the points will be
        used as the midpoints for our rectangle rule. Then run the
        loops according to how many bands we are calculating.

        """
        self.kgrid = [x for x in
                      product([i/self.points for i in range(self.points)],
                              repeat=3)]
        if self.bandnum == 'all':
            for num in range(1, len(self.coeffs.keys())+1):
                self.num = str(num)
                self._rectangleintegral()
        else:
            for num in range(1, self.bandnum+1):
                self.num = str(num)
                self._rectangleintegral()

    def gauss(self):
        """
        Integrate over the interval 0 to 1. Generate the grid to
        evaluate the function on with scipy.special.orthogonal's
        p_roots, also generates the weights. p_roots gave the gauss
        points in 1d so we make kgrid 3D with itertools.product, then
        shift to 0 to 1. Similarly make the weights 3D. Then run the
        loops according to haw many bands we are calculating.

        """
        self.start = 0
        # For even functions do 0.5
        self.end = 1.0
        self.kgrid, self.weights = p_roots(self.points)
        self.kgrid = np.real(self.kgrid)
        self.kgrid = np.asarray([x for x in product(self.kgrid, repeat=3)])
        self.kgrid = (self.end-self.start)*(self.kgrid+1)/2.0 + self.start
        self.weights = np.asarray([np.product(x) for x in
                                   product(self.weights, repeat=3)])
        if self.bandnum == 'all':
            for num in range(1, len(self.coeffs.keys())+1):
                self.num = str(num)
                self._gaussintegral()
        else:
            for num in range(1, self.bandnum+1):
                self.num = str(num)
                self._gaussintegral()

    def serialize(self):
        integral_dict = {'rectangleintegrals': self.rectangleintegrals,
                         'totalrectangleintegral': sum(self.rectangleintegrals),
                         'gaussintegrals': self.gaussintegrals,
                         'totalgaussintegral': sum(self.gaussintegrals)}
        with open(self.name+'integral.json', mode='w',
                  encoding='utf-8') as outf:
            dump(integral_dict, outf, indent=2, default=cs.tojson)
