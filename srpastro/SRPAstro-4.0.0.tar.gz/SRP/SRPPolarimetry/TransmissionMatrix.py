""" Utility functions and classes for SRP

Context : SRP
Module  : Polarimetry
Version : 1.0.0
Author  : Stefano Covino
Date    : 20/01/2015
E-mail  : stefano.covino@brera.inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : to be imported

Remarks :

History : (20/01/2015) First version.

"""

import numpy


def TransmissionMatrix (q0=1.0,u0=1.0,v0=1.0):
    #
    #
    r1 = [1., 0., 0., 0.]
    r2 = [0., q0, 0., 0.]
    r3 = [0., 0., u0, 0.]
    r4 = [0., 0., 0., v0]
    return numpy.matrix([r1, r2, r3, r4])
