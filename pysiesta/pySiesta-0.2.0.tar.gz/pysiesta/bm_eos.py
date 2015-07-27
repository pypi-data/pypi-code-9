#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pysiesta import SiestaObj, Test
import os
from numpy import linspace, where
from matplotlib import pyplot as plt
from pylab import xlabel, ylabel, title, scatter, plot, show, where, linspace, text
from scipy.optimize import curve_fit

def bm_eos(a, e0, a0, b0, db0):
    aa = (a0/a)**2
    bb = aa - 1
    return e0 + 9.*a0**3*b0/16. * (bb**3*db0 + bb**2 * (6-4*aa))


T = Test(testName=r'Lattice', loadTest=True)
T.set_TotalFinalEnergies(ref='m')

x = T.TestSteps
y = T.TotalFinalEnergies

popt, pcov = curve_fit(bm_eos, x, y, p0=[y.min(), x[where(y==y.min())[0][0]], 1, 1], maxfev=1000000)

e0, a0, b0, db0 = popt


xf = linspace(x[0], x[-1], 100)
yf = bm_eos(xf, e0, a0, b0, db0)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(r'Lattice Parameter [\AA]')
ax.set_ylabel('Energy [eV]')
ax.scatter(x, y, c='red', s=50, alpha=0.8)
ax.plot(xf, bm_eos(xf, e0, a0, b0, db0), 'b-', lw=2)
ax.text(0.9, 0.9, r'\noindent $a_0=%.2f$ \AA \\ $B_0=%.3f$ GPa' % (a0, b0*1.6021*10**2),
        verticalalignment='top', horizontalalignment='right',
        transform=ax.transAxes)

plt.show()
