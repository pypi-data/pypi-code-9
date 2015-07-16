import numpy as _np
import matplotlib.pyplot as _plt
from .figure import figure
from .linspacestep import linspacestep
from .gaussfit import gaussfit
# import copy
# import pdb as _pdb


def findpinch(img, xbounds=None, ybounds=None, step=1, verbose=False):
    # ======================================
    # Translate to clearer variables
    # ======================================
    if xbounds is None:
        xstart = 0
        xstop = img.shape[0]
    else:
        xstart = xbounds[0]
        xstop  = xbounds[1]

    if ybounds is None:
        ystart = 0
        ystop = img.shape[1]
    else:
        ystart = ybounds[0]
        ystop  = ybounds[1]

    xrange = slice(xstart, xstop)
    yrange = slice(ystart, ystop)

    img = img[yrange, xrange]
    if verbose:
        fig = figure('To process')
        ax = fig.add_subplot(111)
        ax.imshow(img)
        _plt.show()
    
    # ======================================
    # Check number of points and
    # initialize arrays
    # ======================================
    num_pts   = (ystop - ystart) / step
    # sigs      = _np.zeros(num_pts)
    variance  = _np.zeros(num_pts)
    # stddev    = _np.zeros(num_pts)
    # varerr    = _np.zeros(num_pts)
    chisq_red = _np.zeros(num_pts)
    
    # ======================================
    # Fit individual slices
    # ======================================
    for i, val in enumerate(linspacestep(0, ystop - ystart - step, step)):
        # Take a strip of the image
        strip = img[slice(val, val + step), :]
        
        # Sum over the strip to get an average of sorts
        histdata = _np.sum(strip, 0)
        xbins = len(histdata)
        x = _np.linspace(1, xbins, xbins)
        
        # Fit with a Gaussian to find spot size
        # plotbool = True
        plotbool = False
        varbool  = False
        popt, pcov, chisq_red[i] = gaussfit(
            x,
            histdata,
            sigma_y         = _np.ones(xbins),
            plot            = plotbool,
            variance_bool   = varbool,
            background_bool = True,
            verbose         = False)
    
        variance[i] = popt[2]
    
    # ======================================
    # Fit 2nd-deg poly to results
    # ======================================
    yvar = _np.shape(linspacestep(ystart, ystop, step))[0] - 1
    yvar = linspacestep(1, yvar)
    
    out = _np.polyfit(yvar, variance, 2)

    if verbose:
        # pass
        _plt.figure()
        pvar = ystart + yvar * step
        _plt.plot(pvar, variance, '.-', pvar, _np.polyval(out, yvar), '-')
        _plt.show()

    # ======================================
    # Report minimum in steps and pixels
    # ======================================
    fitmin = -out[1] / (2 * out[0])
    pxmin = fitmin * step + ystart

    print('Minimum at {} step, {}px'.format(fitmin, pxmin))

    return pxmin
