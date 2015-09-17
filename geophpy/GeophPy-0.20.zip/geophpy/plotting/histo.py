# -*- coding: utf-8 -*-
'''
    geophpy.plotting.histo
    ----------------------

    Map Plotting Histofeam Managing.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import matplotlib.pyplot as plt
import numpy as np
import math


def plot(dataset, fig=None, filename=None, zmin=None, zmax=None, dpi=None, transparent=False):
    '''plotting the histogram curve.'''
    if (fig == None):
        fig = plt.figure()
    else:
        fig.clf()

    Z = dataset.data.z_image
    n, bins, patches = plt.hist(Z.reshape((1, Z.shape[0]*Z.shape[1]))[0], bins=100, range=(zmin,zmax), facecolor='black', alpha=1)
    plt.xlim(bins.min(), bins.max())
    if (filename != None):
       plt.savefig(filename, dpi=dpi, transparent=transparent)

    return fig



def getlimits(self):
    '''getting limits values of histogram.'''
    Z = self.data.z_image
    array = np.reshape(np.array(Z), (1, -1))
    min = np.nanmin(array)
    max = np.nanmax(array)
    return min, max
