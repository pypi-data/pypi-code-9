# -*- coding: utf-8 -*-
'''
    geophpy.plotting.correlation
    ----------------------------

    Map Plotting Correlation Managing.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import matplotlib.pyplot as plt
import geophpy.processing.general as genprocessing
import numpy as np
import math



def plotmap(dataset, fig=None, filename=None, method="Pearson", dpi=None, transparent=False):
    '''plotting the correlation map.'''

    if (fig == None) :                      # if first display
        fig = plt.figure()                  # creates the figure
    else :                                  # if not first display
        fig.clf()                           # clears figure

    ax = fig.add_subplot(111)

    # Compute the profiles correlation map ######################
    cor1, pva1 = genprocessing.correlmap(dataset, method)
    shift      = genprocessing.correlshift(cor1, pva1)

    # Build the image
    xmin = dataset.info.x_min   # - xdelta/2 ?
    xmax = dataset.info.x_max   # + xdelta/2 ?
    ny   = (cor1.shape[0] + 1) // 2

    ax.imshow(cor1, extent=(xmin,xmax,-ny,+ny), origin='lower', interpolation='none', aspect='auto')

    ax.plot([xmin,xmax], [-shift,-shift], 'k', linewidth=2)

    if (filename != None):
       plt.savefig(filename, dpi=dpi, transparent=transparent)

    return fig



def plotsum(dataset, fig=None, filename=None, method="Pearson", dpi=None, transparent=False):
    '''plotting the correlation sum.'''

    if (fig == None) :                      # if first display
        fig = plt.figure()                  # creates the figure
    else :                                  # if not first display
        fig.clf()                           # clears figure

    ax = fig.add_subplot(111)

    # Compute the profiles correlation map ######################
    cor1, pva1 = genprocessing.correlmap(dataset, method)
    corm       = np.zeros(cor1.shape[0])
    shift      = genprocessing.correlshift(cor1, pva1, output=corm)
    n          = corm.size

    # builds the image
    ax.plot(np.arange(0,n)-(n-1)//2, corm)

    ax.plot([-shift,-shift], [np.nanmin(corm),np.nanmax(corm)], 'k', linewidth=2)

    if (filename != None):
       plt.savefig(filename, dpi=dpi, transparent=transparent)

    return fig
