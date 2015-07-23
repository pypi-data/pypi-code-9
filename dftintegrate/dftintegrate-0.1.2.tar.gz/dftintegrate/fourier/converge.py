"""
Classes::
  Converge -- A collection of functions that loop over the number of
    integration points, calling integratedata, and then recording and
    plotting the convergence rate of the rectangles to the convergence
    rate of Gaussian quadrature.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt

from dftintegrate.fourier import integratedata
from dftintegrate import customserializer as cs


class Converge():
    """
    Compare integrating the fourier representation with rectangles to
    integrating it with Gaussian quadrature.

    Variables::
      name -- Path to directory with data to work on.

      maxpoints -- Maximum number of integration points to use.

      p -- Number of integration points for the current iteration.

      bandnum -- Number of bands to work on.

      recints -- A list. Each entry is the integral under all the bands
        specified. Each succeeding entry is the same integral with more
        integration points. Rectangle Rule.

      gaussints -- A list. Each entry is the integral under all the bands
        specified. Each succeeding entry is the same integral with more
        integration points. Gaussian quadrature.

      rec_conv -- A list. The last entry in recints is the 'right'
        answer. It is subtracted from each entry in recints to
        produce rec_conv.

      gaussconv -- A list. The last entry in recints is the 'right'
        answer. It is subtracted from each entry in recints to
        produce gaussconv.

    Funtions::
      _getintegraldata -- Load integral.json.

      _calc_convergence -- Subtract the correct answer from each
        integral.
      converge -- Loop over the number of integration points, load data,
        do subtraction.

      serialize -- Serialize the convergence data to a json file
        (converge.json).
      plot -- Make a plot with Matplotlib.
    """
    def __init__(self, name_of_directory, maxpoints, bandnum='all'):
        """
        Arguments::
          name_of_directory -- path to directory that contains integral.json

          maxpoints -- Maximum number of integration points.

        Keyword Arguments::
          bandnum -- Number of bands to use in integration. Default is to
            integrate all bands in fit.json.
        """
        self.name = name_of_directory+'/'
        self.maxpoints = int(maxpoints)
        self.bandnum = bandnum
        self.recints = []
        self.gaussints = []
        self.rec_conv = []
        self.gaussconv = []
        self.integrate = integratedata.IntegrateData
        self.converge()

    def _getintegraldata(self):
        """
        Load integral.json to self.data and extract the total integrals.
        The total integrals are the integrals of all the specified bands
        added together. Rename integral.json so it isn't overwritten in
        the next iteration.
        """
        with open(self.name+'integral.json', mode='r',
                  encoding='utf-8') as inf:
            self.data = json.load(inf, object_hook=cs.fromjson)
        self.recints.append(self.data['totalrectangleintegral'])
        self.gaussints.append(self.data['totalgaussintegral'])
        os.rename('integral.json', 'integral'+str(self.p)+'.json')

    def _calc_convergence(self):
        """
        Since rectangles can integrate periodic functions exactly,
        the last entry in recints should be the correct answer. We
        subtract the correct answer from all the total integrals to
        see how fast they approach it.
        """
        correct = self.recints[-1]
        self.rec_conv = [abs(el-correct) for el in self.recints]
        self.gaussconv = [abs(el-correct) for el in self.gaussints]

    def converge(self):
        """
        Loop over the number of integration points, carrying out the
        integration each time.
        """
        for p in range(1, self.maxpoints+1):
            self.p = p
            self.integrate(self.name, p, self.bandnum)
            self._getintegraldata()
        self._calc_convergence()
        self.serialize()
        self.plot()

    def serialize(self):
        converge_dict = {'rectangles': self.rec_conv,
                         'gauss': self.gaussconv}
        with open(self.name+'converge.json', mode='w',
                  encoding='utf-8') as outf:
            json.dump(converge_dict, outf, indent=2, default=cs.tojson)

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        xaxis = np.power(np.asarray(range(1, self.maxpoints+1)), 3)
        ax.plot(xaxis, self.rec_conv, label='rectangles', color='r')
        ax.plot(xaxis, self.gaussconv, label='gauss', color='b')
        plt.legend(loc='best', prop={'size': 20})
        plt.xlabel('integration points', fontsize=20)
        plt.ylabel('absolute error', fontsize=20)
        plt.xscale('log')
        plt.yscale('log')
        ax.tick_params(axis='both', which='major', labelsize=20)
        plt.title('Convergence: Rectangle vs. Gauss', fontsize=20, y=1.02)
        plt.savefig('converge.png', bbox_inches='tight')
        plt.close()
