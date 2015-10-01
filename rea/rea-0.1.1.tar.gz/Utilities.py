# Copyright (C) 2014
# Institut d'Astrophysique Spatiale
#
# Forked from the BoA project
#
# Copyright (C) 2002-2006
# Max-Planck-Institut fuer Radioastronomie Bonn
# Argelander Institut fuer Astronomie
# Astronomisches Institut der Ruhr-Universitaet Bochum
#
# Produced for the LABOCA project
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Library General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Library General Public License for more
# details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#

"""
..module:: Utilities
    :synopsis: contains utilities & methods for fitting functions
"""

__version__ = '$Revision: 2701 $'
__date__  = '$Date: 2010-03-29 12:07:16 +0200 (lun. 29 mars 2010) $'

#----------------------------------------------------------------------------------
#----- Import ---------------------------------------------------------------------
#----------------------------------------------------------------------------------
import time, sys, posix, cPickle


import numpy as np
import copy
import mpfit


from rea.fortran  import fUtilities, fStat
from rea.ReaError import ReaError
from rea          import ReaConfig

def ps():
    posix.system('ps -l | grep python | grep -v grep')

#----------------------------------------------------------------------------------
# Timing --------------------------------------------------------------------------
#----------------------------------------------------------------------------------

class Timing:
    """..class:: Timing
    :synopsis: easily profile time computation in program
    """

    def __init__(self):
        # the time mark
        self.initTime = time.time()
        self.lastTime = self.initTime
        self.nIter = 0

    def __str__(self):
        return "%10.3f seconds" % (time.time()-self.lastTime)

    def getTime(self):
        return (time.time()-self.lastTime)

    def setTime(self):
        self.lastTime = time.time()

    def resetTime(self):
        self.initTime = time.time()
        self.lastTime = self.initTime

    def setIter(self, maxiter=1):
        self.nIter = maxiter

    def timeLeft(self, iter=0):
        remainTime  = (time.time()-self.initTime)/(iter+1)*(self.nIter-iter)
        remainMin = int(remainTime/60.)
        print str("Time left : %3im %4.1fs"%(remainMin, remainTime-60*remainMin)), "\r",
        sys.stdout.flush()


class ProgressBar:
    """..class:: progressBar
    :synopsis: Creates a text-based progress bar.
    """

    def __init__(self, minValue = 0, maxValue = 100, totalWidth=80):
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount = 0):
        if newAmount < self.min:
            newAmount = self.min
        if newAmount > self.max:
            newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = int(round(percentDone))

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # Build a progress bar with an arrow of equal signs; special cases for
        # empty and full
        if numHashes == 0:
            self.progBar = "[>%s]" % (' '*(allFull-1))
        elif numHashes == allFull:
            self.progBar = "[%s]" % ('='*allFull)
        else:
            self.progBar = "[%s>%s]" % ('='*(numHashes-1),
                                        ' '*(allFull-numHashes))

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone))
        percentString = str(percentDone) + "%"

        # slice the percentage into the b1ar
        self.progBar = ''.join([self.progBar[0:percentPlace], percentString,
                                self.progBar[percentPlace+len(percentString):]
                                ])

    def __str__(self):
        return str(self.progBar)

    def __call__(self, value):
        """ Updates the amount, and writes to stdout. Prints a carriage return
            first, so it will overwrite the current line in stdout.

        Parameters
        ----------
        value : float
           the progress value
        """

        print '\r',
        self.updateAmount(value)
        sys.stdout.write(str(self))
        sys.stdout.flush()



def tolist_rea(a):
    """replacement for tolist (method) from Numeric (which is leaking memory) """
    # note that this function will become obsolete when and if
    # there is a fix for the memory leak problem in Numeric

    if len(a.shape) == 1:
        l = list(a)
    else:
        l = []
        for sa in a:
            l += [ tolist_rea(sa) ]
    return l


#--------------------------------------------------------------------------------
def compressNan(array):
    """return an array without nan

    Parameters
    ----------
    array : array
        input array

    Returns
    -------
    array
        values of the previous array without Nan
    int
        the number of nan found
    """

    inputArray = np.concatenate(copy.copy(array))
    mask = np.isnan(inputArray)
    return inputArray[~mask], np.count_nonzero(mask)

#----------------------------------------------------------------------------------
def prettyPrintList(inputList):
    """pretty print a list avoiding useless entries

    Parameters
    ----------
    inputList : list
        the input list, does not need to be sorted

    Returns
    -------
    str
        the resulting string
    """
    theList = sorted(inputList)

    startItem   = theList[0]
    currentItem = theList[0]

    outputString = ""

    for i in np.arange(1, len(theList)):
        if theList[i]-currentItem > 1:
            if currentItem - startItem != 0:
                outputString = outputString + str(startItem) + "-" + str(currentItem) + "; "
            else:
                outputString = outputString + str(startItem) + "; "

            currentItem = theList[i]
            startItem   = theList[i]
        else:
            currentItem = theList[i]


    if currentItem - startItem != 0:
        outputString = outputString + str(startItem) + "-" + str(currentItem)
    else:
        outputString = outputString + str(startItem)


    return outputString
#----------------------------------------------------------------------------------
def stripFitsExtension(filename):
    """strip any fits extension from a filename

    Parameters
    ----------
    filename : str
        the input filename

    Returns
    -------
    str
        the resulting string
    """
    output = filename

    if output[-5:] == '.fits':
        output = output[:-5]
    if output[-8:] == '.fits.gz':
        output = output[:-8]

    return output

#----------------------------------------------------------------------------------
# Fitting Functions ---------------------------------------------------------------
#----------------------------------------------------------------------------------



# ---- Parabola -------------------------------------------------------------------
def fitParabola(x, y, err):
    """parabola function for mpfit

    Parameters
    ----------
    x, y,err : float array
        x & y data and corresponding errors

    Returns
    -------
    array
        the chi2 array needed for mpfit
    """
    # p=detStartParaParabola(x,y)
    p = [0.0, 0.0, 0.0]
    parinfo = [{'value': 0., 'mpprint': 0}]*3
    for i in np.arange(3):
        parinfo[i]['value'] = p[i]
    fa = {'x': x, 'y': y, 'err': err}
    m = mpfit.mpfit(parabola, p, parinfo=parinfo, functkw=fa, quiet=1)
    # if (m.status <= 0):
    #    raise ReaError, str("mpfit failed: %s"%(m.errmsg))
    return m


# ---------------------------------------------------------------------------------
def detStartParaParabola(x, y):
    """define the proper start parameter to fit a parabola

    Parameters
    ----------
    x, y : float array
        the data

    Returns
    -------
    array
        hopefully a good parameter set for starting the fit
    """
    p = [0.0, 0.0, 0.0]
    s = []
    t = []
    for k in np.arange(0, 5):
        s.append(sum(x**k))
    for k in np.arange(0, 3):
        t.append(sum(x**k*y))
    d_0 = s[0]*t[1]-s[1]*t[0]
    d_1 = s[1]*s[2]-s[0]*s[3]
    d_2 = s[1]*s[3]-s[2]**2
    d_3 = s[1]*t[2]-s[2]*t[1]
    d_4 = s[2]*s[3]-s[1]*s[4]
    d_5 = s[0]*s[2]-s[1]**2
    p[2] = (d_3*d_5-d_0*d_2)/(d_1*d_2-d_4*d_5)
    p[1] = (d_3+p[2]*d_4)/d_2
    p[0] = (t[0]-p[1]*s[1]-p[2]*s[2])/s[0]
    return p

# ---------------------------------------------------------------------------------
def parabola(p, fjac=None, x=None, y=None, err=None):
    """function used by mpfit to fit a parabola

    Parameters
    ----------
    p : float array
        the parabola parameters

    Returns
    -------
    array
        status and chi2 array needed by mpfit
    """
    model = modelparabola(p, x)
    status = 0
    return([status, (y-model)/err])


def modelparabola(p, x):
    """compute a model parabola at position x for a given set of parameters p

    Parameters
    ----------
    p : float array
        the parabola parameters
    x : float array
        the point where we want the parabola

    Returns
    -------
    array
        the parabola value at `x` values
    """
    return(p[0]+p[1]*x+p[2]*x**2)


# ---------------------------------------------------------------------------------
def skydip(p, fjac=None, x=None, y=None, err=None):
    """signal as a function of elevation, aka skydip

    Parameters
    ----------
    p : float array
        the parameters of the skydip fit
    x, y, err : float array
        the data point

    Returns
    -------
    float array
        the status and chi2 array needed for mpfit

    """
    model = modelSkydip(p, x)
    status = 0
    return([status, (y-model)/err])

def modelSkydip(p, x):
    """ model function for fitting skydip

    Parameters
    ----------
    p : float array
       the parameter for the skydip model with 5 parameters
    x : float array
       the line of sight optical depth

    Notes
    -----
    skydip full model, with 5 parameters:

    t(x)=(1-opt)*tcabin+opt*tatm*((1-exp(-tauz/sin(pi*x/180.0)))*feff+(1-feff))

    p[0]=opt, p[1]=tcabin, p[2]=tatm, p[3]=tauz, p[4]=feff
    """
    tmp1 = -1.*p[3]/sin(x*np.pi/180.)
    tmp2 = p[0]*p[2]*((1.-np.exp(tmp1))*p[4] + (1.-p[4]))
    return ((1.-p[0])*p[1] + tmp2)

def fitSkydip(x, y, err, val0, fixT=True):
    """fits a skydip signal-elevation function

    Parameters
    ----------
    x, y, err : float array
        the data, tau, power and associated error
    val0 : float array
        first guess values, in this order:
        [coupling, Tcabin, Tatm, tau_z, F_eff]
    fixT : bool
        do we fix Tcabin ?

    Returns
    -------
    float array
        the fit result from mpfit

    Notes
    -----
    Only 2 parameters fitted: opt, tauz

    """
    parname = ['Coupling', 'Tcabin', 'Tatm', 'tau_z', 'F_eff']
    p = val0
    parinfo = []
    for i in np.arange(5):
        parinfo.extend([{'parname': parname[i], \
                         'value': p[i], \
                         'fixed': 0, \
                         'limits' : [0., 0.],\
                         'limited': [1, 1]}])
    parinfo[0]['limits'] = [0., 1.]
    parinfo[3]['limits'] = [0., 3.]  # don't observe at tau>3 !!
    if fixT:
        parinfo[1]['fixed'] = parinfo[4]['fixed'] = parinfo[2]['fixed'] = 1
    else:
        parinfo[1]['fixed'] = parinfo[4]['fixed'] = 1
    parinfo[1]['limits'] = [200, 320]
    parinfo[2]['limits'] = [100, 320]
    parinfo[4]['limits'] = [0., 1.]

    fa = {'x': x, 'y': y, 'err': err}
    m = mpfit.mpfit(skydip, p, parinfo=parinfo, functkw=fa, quiet=1, debug=0)
    if (m.status <= 0):
        raise ReaError(str("mpfit failed: %s"%(m.errmsg)))
    return m

# ---- Gaussian -------------------------------------------------------------------
def fitGaussian(x, y, err, const=0):
    """fits a Gaussian to the data using mpfit

    Parameters
    ----------
    x, y, err : float array
        the data and associated error
    const : bool
        do we also fit a constant term ?
    """

    p = [1.0, 1.0, 1.0]
    if const:
        p.append(0.)

    # try to guess the parameters quick-and-dirty
    p[0] = max(y)
    weights = y/sum(y)
    p[1] = sum(x*weights)
    cutoff_mask = np.where((np.array(y) > max(y)/2.), 1, 0)
    cutoff = np.compress(cutoff_mask, np.array(y))
    p[2] = max(x)*float(len(cutoff))/float(len(y))
    if const:
        p[3] = fStat.f_median(y)

    parinfo = [{'value': 0., 'mpprint': 0}]*3
    for i in np.arange(3):
        parinfo[i]['value'] = p[i]
    if const:
        parinfo.append({'value': 0., 'mpprint': 0})
        parinfo[3]['value'] = p[3]

    fa = {'x': x, 'y': y, 'err': err}
    try:
        if const:
            m = mpfit.mpfit(gaussbase, p, parinfo=parinfo, functkw=fa, quiet=1)
        else:
            m = mpfit.mpfit(gauss, p, parinfo=parinfo, functkw=fa, quiet=1)
        if (m.status <= 0):
            raise ReaError(str("mpfit failed: %s"%(m.errmsg)))

    except:
        m.params = [0., 1., 1.]
        if const:
            m.append(0.)
        # self.MessHand.warning("could not fit gaussian")
    return m

# ---------------------------------------------------------------------------------
def gauss(p, fjac=None, x=None, y=None, err=None):
    """function used by mpfit to fit a gaussian

    Parameters
    ----------
    p : float array
        the 3 gaussian parameters
    x, y, err : float array
        the data and associated error

    Returns
    -------
    float array
        status and chi2 arrays as needed by mpfit
    """
    model = modelgauss(p, x)
    status = 0
    return([status, (y-model)/err])


def modelgauss(p, x):
    """compute a model gaussian at position x for a given set of parameters p

    Parameters
    ----------
    p : float array
        the 3 gaussian parameters [norm, mu, sigma]
    x : float array
        the values at which we evaluate the gaussian

    Returns
    -------
    float array
        the gaussian at x values

    Notes
    -----
    norm*exp( -((x-mu)**2)/(2.*sigma**2)  )
    """

    norm = p[0]
    mu = p[1]
    sigma = p[2]

    exponent = ((x-mu)/sigma)

    # return( (norm/(2.*pi*sigma))*np.exp( -(exponent**2)/2.  ) )
    return( norm*np.exp( -(exponent**2)/2.  ) )

def gaussbase(p, fjac=None, x=None, y=None, err=None):
    """function used by mpfit to fit a gaussian + constant term

    Parameters
    ----------
    p : float array
        the 4 parameters
    x, y, err : float array
        the data and corresponding error

    Returns
    -------
    float array
        status and chi2 array as needed for mpfit
    """
    model = modelgaussbase(p, x)
    status = 0
    return([status, (y-model)/err])


def modelgaussbase(p, x):
    """compute a model gaussian + constant term

    Parameters
    ----------
    p : float array
        the 3 gaussian parameters and constant term
        [amplitude, mean, sigma, constant]

    x : float array
        the values at which we need to evaluate the function

    Returns
    -------
    float array
        the function evaluated at x

    Notes
    -----
    norm*exp( -((x-mu)**2)/(2.*sigma**2)  ) + constant
    """

    norm = p[0]
    mu = p[1]
    sigma = p[2]
    const = p[3]

    exponent = ((x-mu)/sigma)

    # return( (norm/(2.*pi*sigma))*np.exp( -(exponent**2)/2.  ) )
    return norm*np.exp( -(exponent**2)/2.) + const

#----- 2D Gauss + first order base surface --------------------------------------

def modelBaseEllipticalGaussian(p, position):
    """compute a 2D gaussian defined by the parameter p wihtin the position
    position should be a list of 2 arrays of same dimensions defining the map

    Parameters
    ----------
    p : float array
        the 2D elliptical gaussian parameters with plane gradiant
        [cont, cont_x, cont_y, int, x_offset, y_offset, x_fwhm, y_fwhm, tilt]
    position : 2D float array
        (x,y) the x and y position defining the map

    Returns
    -------
    float array
        the corresponding 2D ellipcital gaussian values
    """
    # p.name = ["gauss_cont","gauss_cont_x","gauss_cont_y", \
    #          "gauss_peak","gauss_x_offset","gauss_y_offset", \
    #          "gauss_x_FWHM","gauss_y_FWHM","gauss_tilt"]

    x, y = position
    cont, cont_x, cont_y, g_int, x_offset, y_offset, x_fwhm, y_fwhm, tilt = p

    fwhm2sigma = 1./(2*np.sqrt(2*np.log(2)))

    sigma_x = x_fwhm*fwhm2sigma
    sigma_y = y_fwhm*fwhm2sigma

    x_x_offset = x-x_offset
    y_y_offset = y-y_offset

    cos_tilt = np.cos(tilt)
    sin_tilt = np.sin(tilt)
    gauss_int = 2*np.pi*sigma_x*sigma_y

    xp = x_x_offset*cos_tilt-y_y_offset*sin_tilt
    yp = x_x_offset*sin_tilt+y_y_offset*cos_tilt
    U = (xp/sigma_x)**2+(yp/sigma_y)**2

    return cont + cont_x*x + cont_y*y + g_int/gauss_int*np.exp(-U/2)

#    model = fUtilities.modelbaseellipticalgaussian(p,position)
#    return reshape(model,shape(position[0]))

# ---------------------------------------------------------------------------------
def baseEllipticalGaussian(p, fjac=None, x=None, y=None, err=None):
    """function used by mpfit to fit a 2D gaussian+base

    Parameters
    p : float array
        9 parameters of the gaussian (see modelBase2Dgauss)
    x, y, err : float array
        x is a 3D float array wih the position of the pixels on the map
        "x" = x[0] and "y" = x[1] for each pixels
        y is a 2D float array, map to fit
        err is a 2D float array corresponding to y

    Returns
    -------
    float array
        status and chi2 arrays as needed by mpfit    """

    model = fUtilities.modelbaseellipticalgaussian(p, x)
    status = 0

    return([status, np.ravel((y-model)/err)])

# ---------------------------------------------------------------------------------
def baseCircularGaussian(p, fjac=None, x=None, y=None, err=None):
    """function used by mpfit to fit a Circular gaussian+base

    Parameters
    ----------
    p : float array
        7 parameters of the gaussian
    x, y, err : float array
        x is a 3D float array wih the position of the pixels on the map
        "x" = x[0] and "y" = x[1]
        y is a 2D float array, map to fit
        err is a 2D float array corresponding to y

    Returns
    -------
    float array
        status and chi2 arrays as needed by mpfit
    """

    lp = np.concatenate([p, [p[-1], 0]])
    model = fUtilities.modelbaseellipticalgaussian(lp, x)
    status = 0

    return([status, np.ravel((y-model)/err)])



# ---------------------------------------------------------------------------------
def fitBaseEllipticalGaussian(mapArray, x, y, err=1.0, fwhm=11.0, gradient=True, circular=False,\
                              Xpos=0., Ypos=0., fixedPos=False, incl=0., fixIncl=False):
    """fits a 2D Gaussian + 1st order base surface

    Parameters
    ----------
    x,y,mapArray,err : float arrays
        the data to fit (arrays of same dimension(s))
    fwhm  : float
        the first guess for the fwhm
    gradient : bool
        should we also fit a gradient in the map (default no) ?
    circular : bool
        fit a circular gaussian instead of a elliptical gaussian
    Xpos,Ypos : float
        source position if using fixed position
    fixedPos : bool
        if set, don't fit position, but use Xpos, Ypos
    incl : float
        inclination angle
    fixIncl : float
        fix the inclination angle? default no (0)

    Returns
    -------
    dictionnary
        a dictionnary containning the results of the fit check
        'status' and 'errmsg' to see if the fit was done correctly
        then for each parameters (see the parname variable below) you
        have the 'value' 'error' and 'limits' for the fit

    """

    # Test for dimension
    if not ((len(x.shape) == 2 or len(x.shape) == 1) and \
             len(x.shape) == len(y.shape) == len(mapArray.shape)):
        print "Error : Arrays must have the same dimension (1D or 2D)"
        return

    # In case we have 2D arrays, put everything into 1D
    x = np.ravel(x)
    y = np.ravel(y)
    mapArray = np.ravel(mapArray)
    err = np.ravel(err)

    if isinstance(err, float):
        # Unweighted
        err = np.ones(mapArray.shape)*err
        # err = ones(mapArray.shape)*sqrt(abs(mapArray))

    # Search and remove NaN
    good = np.logical_not(np.isnan(mapArray))
    lMapArray = mapArray[good]
    lX = x[good]
    lY = y[good]
    lErr = err[good]

    # At this point lX/Y/Z/Err are 1D array with only the mesured data points

    # the value to fit
    fa = {'x': np.array([lX, lY]), 'y': lMapArray, 'err': lErr}

    # fitting function by default elliptical gaussian
    fitFunction = baseEllipticalGaussian

    # define the parameters to fit
    parname = ["continuum", "continuum_x", "continuum_y", \
               "gauss_peak", "gauss_x_offset", "gauss_y_offset", \
               "gauss_x_fwhm", "gauss_y_fwhm", "gauss_tilt"]

    parinfo = []
    # set the values
    for i in np.arange(len(parname)):
        parinfo.extend([{'parname': parname[i], \
                           'value': 0., \
                           'fixed': 0, \
                         'limits' : [0., 0.],\
                         'limited': [0, 0]}])

    # set limits on position
    parinfo[4]['limited'] = [1, 1]
    parinfo[4]['limits'] = [min(lX), max(lX)]
    parinfo[4]['value'] = Xpos
    parinfo[5]['limited'] = [1, 1]
    parinfo[5]['limits'] = [min(lY), max(lY)]
    parinfo[5]['value'] = Ypos

    # check that X/Y pos are in the limits
    for i in [4, 6]:
        if not parinfo[i]['limits'][0] < parinfo[i]['value'] < parinfo[i]['limits'][1]:
            parinfo[i]['value'] = (parinfo[i]['limits'][1]-parinfo[i]['limits'][0])/2

    # fwhm has to be positive so (let say 1/10 of the given fwhm to
    # avoid division by 0) let say also that the fhwm can not be
    # greater than the total map

    # TODO: the definition below is not good: since the gaussian can rotate,
    # gauss_x_FWHM is not bound to the x axis
    parinfo[6]['value']   = fwhm
    parinfo[6]['limited'] = [0, 0]
    # parinfo[6]['limits']  = [fwhm/5,max(lX)-min(lX)]
    # parinfo[6]['limits']  = [fwhm/2.,2.*fwhm]
    parinfo[6]['limits']  = [fwhm*0.75, 5.*fwhm]  # allow for extended source, but no spike
    parinfo[7]['value']   = fwhm
    parinfo[7]['limited'] = [0, 0]
    # parinfo[7]['limits']  = [fwhm/5,max(lY)-min(lY)]
    # parinfo[7]['limits']  = [fwhm/2.,2.*fwhm]
    parinfo[7]['limits']  = [fwhm*0.75, 5.*fwhm]  # allow for extended source, but no spike

    # a tilt is always bound in a circle so
    # parinfo[8]['limited'] = [1,1]
    # parinfo[8]['limits'] = [-2.*pi,2.*pi]
    # except that mpfit doesn't converge right...
    parinfo[8]['limited'] = [0, 0]

    # the peak flux of the source is always positive, this is not SZ !
    parinfo[3]['limited'] = [1, 0]
    parinfo[3]['limits']  = [0, 0]

    # in case a circular gaussian was asked
    if circular:
        fitFunction = baseCircularGaussian
        parinfo = parinfo[0:7]

    # if we need to fit a gradient, then first fit it and then retrieve the gaussian
    if gradient:
        # Fix everything for the gaussian
        for i in np.arange(3, len(parinfo)):
            parinfo[i]['fixed'] = 1

        # 0 flux for the gaussian -> pure gradient
        parinfo[3]['value'] = 0

        # set up the first guess array (take the value from the
        # parinfo array)
        p = []
        for i in np.arange(len(parinfo)):
            p.append(parinfo[i]['value'])
        p = np.array(p)

        result = mpfit.mpfit(fitFunction, p, parinfo=parinfo, functkw=fa, quiet=1,\
                      ftol=1.e-2, xtol=1.e-2, gtol=1.e-2)
        if (result.status <= 0):
            raise ReaError(str("mpfit failed: %s"%(result.errmsg)))

        # set the values of the gradient found for the global fit NO !
        # the fitted gradient should be refitted, it is only used to
        # retrive the parameters of the gaussian, otherwise we go into
        # troubles
        for i in np.arange(3):
            parinfo[i]['value'] = result.params[i]

        # compute the residual map after the gradient fit (to find
        # the first guess for the gaussian)

        params = result.params.tolist()
        if circular:
            params.append(result.params[6]) # "gauss_y_fwhm"
            params.append(0)                # "gauss_tilt"

        params = np.array(params)

        model = modelBaseEllipticalGaussian(params, [lX, lY])

        # use a variable with a different name otherwhise values in
        # 'fa' will also be changed
        lMapArray = lMapArray-model

        # release everything for the gaussian
        for i in np.arange(3, len(parinfo)):
            parinfo[i]['fixed'] = 0

        # continuum level is biased in case of a weak gradient+strong
        # gaussian so leave it to 0

        parinfo[0]['value'] = 0

    # if asked no to fit a gradient, then do not fit it !
    if not gradient:
        for i in np.arange(1, 3):
            parinfo[i]['fixed'] = 1
            parinfo[i]['value'] = 0

    # We can simply try to retrieve the position of the gaussian:
    maxPos = np.nonzero(np.equal(lMapArray, np.nanmax(lMapArray)))[0]
    # If fixed position, then use it:
    if fixedPos:
        parinfo[4]['value'] = Xpos
        parinfo[4]['fixed'] = 1
        parinfo[5]['value'] = Ypos
        parinfo[5]['fixed'] = 1
    else:
        # Even if not fixed, if initial guesses are given, use them
        if Xpos:
            parinfo[4]['value'] = Xpos
        else:
            parinfo[4]['value'] = lX[maxPos]
        if Ypos:
            parinfo[5]['value'] = Ypos
        else:
            parinfo[5]['value'] = lY[maxPos]

    # fix inclination angle if needed
    if fixIncl:
        parinfo[8]['value'] = incl
        parinfo[8]['fixed'] = 1


    # Suppose we have circular gaussian and the right maximum there,
    # estimate the fwhm

#    inside_fwhm = nonzero(greater(lMapArray,(max(lMapArray)-min(lMapArray))/2))
#    distance = sqrt((take(lX,inside_fwhm)-lX[maxPos])**2+\
#                    (take(lY,inside_fwhm)-lY[maxPos])**2)
#    fwhm = max(distance)

    # Use it as a first guess
    parinfo[6]['value'] = fwhm

    if not circular:
        parinfo[7]['value'] = fwhm

    # use max in map as first guess for peak flux
    # parinfo[3]['value'] = lMapArray[maxPos]*2*pi*fwhm**2
    parinfo[3]['value'] = lMapArray[maxPos]

    # set up the first guess array (take the value from the parinfo array)
    p = []
    for i in np.arange(len(parinfo)):
        p.append(parinfo[i]['value'])
    p = np.array(p, np.float)

    m = mpfit.mpfit(fitFunction, p, parinfo=parinfo, functkw=fa, quiet=1,\
                      maxiter=50, ftol=1.e-10, xtol=1.e-9, gtol=1.e-10)
    if (m.status <= 0 or m.status >= 4):
        raise ReaError(str("mpfit failed: %s"%(m.errmsg)))

    if circular:
        m.params = np.concatenate([m.params, [m.params[-1], 0]])

    result = {'status': m.status, \
              'errmsg': m.errmsg, \
              'params': m.params}

    for i in np.arange(len(parinfo)):
        result[parname[i]] = {'value'  : m.params[i], \
                             'error'   : m.perror[i], \
                             'fixed'   : parinfo[i]['fixed'], \
                             'limits'  : parinfo[i]['limits'],\
                             'limited' : parinfo[i]['limited']}
    if circular:
        result[parname[7]] = { 'value'  : m.params[6], \
                               'error'   : m.perror[6], \
                               'fixed'   : parinfo[6]['fixed'], \
                               'limits'  : parinfo[6]['limits'],\
                               'limited' : parinfo[6]['limited']}

        result[parname[8]] = { 'value'  : 0, \
                               'error'   : 0, \
                               'fixed'   : 0, \
                               'limits'  : [0, 0],\
                               'limited' : [0, 0]}

    # convert tilt angle to degree
    result['gauss_tilt']['value'] *= 180./np.pi

    # Make sure that FWHM1 is major axis, and FWHM2 is minor axis...
    if not fixIncl:
        if result['gauss_x_fwhm']['value'] < result['gauss_y_fwhm']['value']:
            result['gauss_x_fwhm'], result['gauss_y_fwhm'] = result['gauss_y_fwhm'], result['gauss_x_fwhm']
            result['gauss_tilt']['value'] += 90.

    # ... and force tilt angle to be within -90 and +90 deg
    ang = result['gauss_tilt']['value']
    result['gauss_tilt']['value'] = (ang+90.)%180. - 90.

    # Compute integrated Gaussian
    fwhm2sigma = 1./(2*np.sqrt(2*np.log(2)))
    sigma_x = result['gauss_x_fwhm']['value']*fwhm2sigma
    sigma_y = result['gauss_y_fwhm']['value']*fwhm2sigma
    result['gauss_int'] = {'limited' : [0, 0], \
                           'fixed' : 1, \
                           'limits' : [0.0, 0.0], \
                           'value' : result['gauss_peak']['value']*2*np.pi*sigma_x*sigma_y, \
                           'error' : 0.0}

    return result

# ---------------------------------------------------------------------------------

def croppedCircularGaussian(p, position, threshold=3):
    """compute a cropped circular gaussian with intensity=1

    Parameters
    ----------
    p : float array
        the circular gaussian 3 parameters
        [x_offset, y_offset, fwhm]
    position : float array
        the position where to compute the gaussian
        [x,y]

    Returns
    -------
    float array
        the value of the gaussian at the required positions

    Notes
    -----
    Defined by the parameter p wihtin the position an a given threshold given in n*'sigma'
    position should be a list of 2 arrays of the same dimension defining the map
    """
    x, y = position
    x_offset, y_offset, fwhm = p

    sigma_squared = fwhm**2/(8*log(2))

    dist = ((x-x_offset)**2+(y-y_offset)**2)/sigma_squared

    returned_array = np.zeros(dist.shape)

    for i in np.arange(dist.shape[0]):
        if max(dist[i,:]) < threshold:
            returned_array[i,:] = np.exp(-dist[i,:]/2)

    return returned_array

def solvePoly(order, dataX, dataY):
    """
    NAM: solvePoly (function)
    DES: perform polyomial interpolation: solve linear system
         dataY = P_n(dataX)
    INP: (int) order : polynomial degree
         (flt arrays) dataX/Y : system to solve
    OUT: (flt array) coeff : polynomial coefficients
    """
    # TODO: use existing NumPy or Fortran package!!!

    result = []
    if order == 1:
        try:
            result.append((dataY[-2]-dataY[-1])/(dataX[-2]-dataX[-1]))
            result.append(dataY[-2]-result[0]*dataX[-2])
        except ZeroDivisionError:
            result = [0., dataY[-1]]
    # elif order == 2:
        # interpolate parabola...
    # nothing to do if order = 0
    return result

#----------------------------------------------------------------------------
# store array attribute of a given class to column major
#----------------------------------------------------------------------------
def as_column_major_storage(classIn):
    """
    DES: save all the attribute as column major to avoid copy in fortran
    """
    attrDict = vars(classIn)
    attrName = attrDict.keys()
    nbAttr = len(attrName)

    for attribute in attrName:
        if isinstance(attrDict[attribute], arraytype) and \
               attrDict[attribute] and \
               not fUtilities.has_column_major_storage(attrDict[attribute]) :
            print attribute
            attrDict[attribute] = fUtilities.as_column_major_storage(attrDict[attribute])

#----------------------------------------------------------------------------
# print attribute list of an object
#----------------------------------------------------------------------------
def attrStr(object,badAttributes=[]):
    """
    DES: return a string representing the attributes of the object
    OPT: (str list) badAttributes : list of attributes to remove from the output
    """

    attrDic = vars(object)
    attrName = attrDic.keys()
    nbAttr = len(attrName)
    attrName.sort()

    # remove badAttributes that can cause trouble
    for badattribute in badAttributes:
        if badattribute in attrName:
            attrName.remove(badattribute)

    out = str(object.__class__)+" object, with "+str(nbAttr)+" attributes\n\n"
    for a in attrName:
        d = attrDic[a]
        typAttr = type(d)
        if (isinstance(np.array(()), typAttr)):
            dim = np.shape(d)
            typElement = d.dtype.char
        else:
            try:
                dim = len(d)
            except TypeError:
                dim = 0

            if (dim and typAttr != dict):
                typElement = type(d[0])
            elif (typAttr == dict):
                typElement = "Keys"
            else:
                typElement = "None"

        out = out+"\t %20s %14s"%(a, typAttr)
        out = out+"\t with %15s elements of type %1s\n"%(dim, typElement)


    return out


# ---------------------------------------------------------------------------------
# Utilities related with Fourier transforms
# ---------------------------------------------------------------------------------

def Cr2p(c):
    """convert complex numbers in rectangular form to polar (mod,arg) form

    Parameters
    ----------
    c : complex
        complex number or array

    Returns
    -------
    (float,float)
        module and phase
    """

    amp   = np.sqrt(c.real**2+c.imag**2)
    phase = np.arctan2(c.imag, c.real)
    return amp, phase

def Cp2r(amp, phase):
    """convert complex numbers in polar form to rectangular form (real,imag)

    Parameters
    ----------
    amp : float
        module
    phase : float
        phase

    Returns
    -------
    complex
        complex number or array
    """
    real = amp*np.cos(phase)
    imag = amp*np.sin(phase)

    c = np.zeros(len(amp), Complex)
    c.real = real
    c.imag = imag

    return c


# ---------------------------------------------------------------------------------
# Utilities related to PCA
# ---------------------------------------------------------------------------------

def principalComponentAnalysis (rawdata, order):
    """principal component cleanning of the data

    Parameters
    ----------
    rawdata : array
        the input array as an NxM array
                 where M - number of channels
                       N - number of time samples
    order : int
        the number of principal components to remove

    Returns
    -------
    array
        data with principal components removed
    """

    # TODO: function should eventually be moved to fortran
    nTime, nChan = rawdata.shape

    # rawDataAdjust, originalMean = adjustDataPCA(rawdata)
    whitenedData, rawMean, rawStd = arrayWhiten(np.transpose(rawdata), axis=1)

    # compute corrlation matrix
    corr = fUtilities.matrixmultiply(whitenedData, np.transpose(whitenedData))

    # eigenvals,eigenvect=LinearAlgebra.eigenvectors(corr)
    eigenvals, eigenvect = np.linalg.eig(corr)

    # eigenvect = np.transpose(eigenvect) # Difference between Numeric and numpy
    eig_index = np.argsort(abs(eigenvals))

    featureVector = np.take(eigenvect, eig_index[0:nChan-order], axis=1)

    whitenedFilteredData = fUtilities.matrixmultiply(featureVector,
                                                    fUtilities.matrixmultiply(
                                                        np.transpose(featureVector), whitenedData))

    # ... and reconstruct the data
    # rowOrigData = fUtilities.matrixmultiply(featureVector, desiredFeature)+originalMean
    filteredData = np.transpose(arrayDeWhiten(whitenedFilteredData, rawMean, rawStd))

    return filteredData, np.take(eigenvals, eig_index), np.take(eigenvect, eig_index, axis=0)


def principalComponentAnalysis2(rawdata, order):
    """principal component cleanning of the data

    Parameters
    ----------
    rawdata : array
        the input array as an NxM array
                 where M - number of channels
                       N - number of time samples
    order : int
        the number of principal components to remove

    Returns
    -------
    array
        data with principal components removed
    """

    # TODO: function should eventually be moved to fortran
    nTime, nChan = rawdata.shape

    # rawDataAdjust, originalMean = adjustDataPCA(rawdata)
    whitenedData, rawMean, rawStd = arrayWhiten(rawdata, axis=0)

    # compute corrlation matrix
    corr = fUtilities.matrixmultiply(np.transpose(whitenedData), whitenedData)

    # eigenvals,eigenvect=LinearAlgebra.eigenvectors(corr)
    eigenvals, eigenvect = np.linalg.eig(corr)

    # eigenvect = np.transpose(eigenvect) # Difference between Numeric and numpy
    eig_index = np.argsort(abs(eigenvals))

    featureVector = np.take(eigenvect, eig_index[0:nChan-order], axis=1)

    whitenedFilteredData = fUtilities.matrixmultiply(fUtilities.matrixmultiply(
                                                         whitenedData, featureVector), np.transpose(featureVector))

    # ... and reconstruct the data
    # rowOrigData = fUtilities.matrixmultiply(featureVector, desiredFeature)+originalMean
    filteredData = arrayDeWhiten(whitenedFilteredData, rawMean, rawStd)

    return filteredData, np.take(eigenvals, eig_index), np.take(eigenvect, eig_index, axis=1)

def arrayWhiten(array, axis=0):
    """withening of array, for use in PCA for e.g.

    Parameters
    ----------
    array : 2D array
        the array to whiten
    axis : {0, 1}
        the axis along which to whiten

    Returns
    -------
    tuple of arrays
        (whitened array, mean array, std array)
        to retrieve the original array just compute
        whiten*std+mean
    """
    mean = array.mean(axis=axis)
    std  = array.std(axis=axis)

    if axis == 0:
        whiten = (array-mean)/std
    elif axis == 1:
        whiten = (array-np.repeat(mean[:, np.newaxis], array.shape[1], axis=1))/np.repeat(std[:, np.newaxis], array.shape[1], axis=1)

    return whiten, mean, std

def arrayDeWhiten(whiten, mean, std):
    """withening of array, for use in PCA for e.g.

    Parameters
    ----------
    whiten : 2D array
        the array to de-whiten
    mean, std, 1D array
        the mean and std along one direction

    Returns
    -------
    array
        de-whitened array
    """

    if whiten.shape[0] == mean.shape[0]:
        array = whiten*np.repeat(std[:, np.newaxis], whiten.shape[1], axis=1)+np.repeat(mean[:, np.newaxis], whiten.shape[1], axis=1)
    elif whiten.shape[1] == mean.shape[0]:
        array = whiten*std+mean

    return array

#----------------------------------------------------------------------------
# functions to get tau and calib correction at a given time
def getCalCorr(refmjd, method, calFile):
    """
    NAM: getCalCorr
    DES: get calibration correction factor at a given time from a file
    INP: (f) refmjd: the time (MJD) requested
         (str) method: method used to compute the calibration, can be:
               'linear': linear interpolation between two closest points
               anything else: returns the closest point
         (str) calFile: file name where MJDs and calCorr values are stored
    OUT: (f) returns the calibration correction factor at the required time
    """

    try:
        f = file(calFile)
    except IOError:
        self.__MessHand.error("could not open file %s"%(calFile))
        return

    # read and process CAL file
    param = f.readlines()
    f.close()
    scannumber, date, calmjd, corr, opacitycorr = [], [], [], [], []   # local lists to store MJD and TAU

    for i in np.arange(len(param)):	        # -1: skip last line
        if param[i][0] != '!':              # skip comments
            tmp = string.split(param[i])
            scannumber.append(string.atof(tmp[0]))
            calmjd.append(string.atof(tmp[2]))
            corr.append(string.atof(tmp[3]))
            opacitycorr.append(string.atof(tmp[4]))


    mjd = np.array(calmjd)
    calcorr = np.array(corr)


    entries = len(mjd)

    mindiff = 1000000.
    mindiffafter = 1000000.
    mindiffbefore = 1000000.
    cbok = 0
    caok = 0
    if method == 'linear':
        for i in np.arange(entries):
            timediff = mjd[i]-refmjd
            if timediff < 0:
                if -1*timediff < mindiffbefore:
                    calbefore = calcorr[i]
                    timebefore = mjd[i]
                    mindiffbefore = -1*timediff
                    cbok = 1
            if timediff > 0:
                if timediff < mindiffafter:
                    calafter = calcorr[i]
                    timeafter = mjd[i]
                    mindiffafter = timediff
                    caok = 1
            if timediff == 0.000:
                resultcalcorr = calcorr[i]
                return resultcalcorr

        if cbok == 1 and caok == 1:
            resultcalcorr = ((calafter-calbefore)/(timeafter-timebefore))*(refmjd-timebefore)+calbefore
        else:
            if cbok == 1:
                resultcalcorr = calbefore
            else:
                resultcalcorr = calafter

    else:
        for i in np.arange(entries):
            timediff = np.sqrt((mjd[i]-refmjd)**2)
            if timediff < mindiff:
                resultcalcorr = calcorr[i]
                mindiff = timediff


    return resultcalcorr

def getTau(refmjd, method, tauFile):
    """
    NAM: getTau
    DES: get zenith opacity (tau) at a given time from a file
    INP: (f) refmjd: the time (MJD) requested
         (str) method: method used to compute the tau, can be:
               'linear': linear interpolation between two closest points
               anything else: returns the closest point
         (str) tauFile: file name where MJDs and tau values are stored
    OUT: (f) returns the tau at the required time
    """

    try:
        f = file(tauFile)
    except IOError:
        self.__MessHand.error("could not open file %s"%(tauFile))
        return

    # read and process TAU file
    param = f.readlines()
    f.close()
    scannumber, date, taumjd, opacity = [], [], [], []   # local lists to store MJD and TAU

    for i in np.arange(len(param)):	        # -1: skip last line
        if param[i][0] != '!':              # skip comments
            tmp = string.split(param[i])
            scannumber.append(string.atof(tmp[0]))
            taumjd.append(string.atof(tmp[2]))
            opacity.append(string.atof(tmp[3]))


    mjd = np.array(taumjd)
    tau = np.array(opacity)

    entries = len(mjd)

    mindiff = 1000000.
    mindiffafter = 1000000.
    mindiffbefore = 1000000.
    tbok = 0
    taok = 0
    if method == 'linear':
        for i in np.arange(entries):
            timediff = mjd[i]-refmjd
            if timediff < 0:
                if -1*timediff < mindiffbefore:
                    taubefore = tau[i]
                    timebefore = mjd[i]
                    mindiffbefore = -1*timediff
                    tbok = 1
            if timediff > 0:
                if timediff < mindiffafter:
                    tauafter = tau[i]
                    timeafter = mjd[i]
                    mindiffafter = timediff
                    taok = 1
            if timediff == 0.000:
                resulttau = tau[i]
                return resulttau
        if tbok == 1 and taok == 1:
            resulttau = ((tauafter-taubefore)/(timeafter-timebefore))*(refmjd-timebefore)+taubefore
        else:
            if tbok == 1:
                resulttau = taubefore
            else:
                resulttau = tauafter

    else:
        for i in np.arange(entries):
            timediff = np.sqrt((mjd[i]-refmjd)**2)
            if timediff < mindiff:
                resulttau = tau[i]
                mindiff = timediff


    return resulttau

def newRestoreData(fileName='ReaData.sav'):
    """
    DES: restore a TimelineData object previously saved in a file, and
    set it as the currData attribute of ReaB
    INP: (string) fileName: name of the input file
    optional - default value = 'ReaData.sav'
    """
    # fileName = self.outDir+fileName
    try:
        f = file(fileName)
    except IOError:
        messages.error(" could not open file %s"%(fileName))
        return
    tmp = cPickle.load(f)
    f.close()

    if hasattr(tmp, 'DataFlags'):
        tmp.FlagHandler = ReaFlagHandler.createFlagHandler(tmp.DataFlags.astype(np.int8))
        tmp.DataFlags = None

        tmp.ScanParam.FlagHandler = ReaFlagHandler.createFlagHandler(tmp.ScanParam.Flags.astype(np.int32))
        tmp.ScanParam.Flags = None

        tmp.ReceiverArray.FlagHandler = ReaFlagHandler.createFlagHandler(tmp.ReceiverArray.Flags.astype(np.int32))
        tmp.ReceiverArray.Flags = None




    # tmp.FillF90()
    return tmp

# ---------------------------------------------------------------------------------
# Utilities related to polygons
# ---------------------------------------------------------------------------------

def inPolygon(x, y, poly):
    """
    DES: check whether point (x,y) is inside a polygon
    INP: (float)        x/y : coordinates of point
          (float array) poly : vertices of polygon
    OUT: (int)              : 0=outside, 1=inside polygon
    """
    counter = 0
    p1 = poly[0]
    for i in np.arange(1, len(poly)+1):
        p2 = poly[i % len(poly)]
        if y > min(p1[1], p2[1]):
            if y <= max(p1[1], p2[1]):
                if x <= max(p1[0], p2[0]):
                    if p1[1] != p2[1]:
                        xinters = (y-p1[1])*(p1[0]-p2[0])/(p1[1]-p2[1])+p1[0]
                        if p1[0] == p2[0] or x <= xinters:
                            counter = counter+1
        p1 = p2
    return counter % 2

    #--------------------------------------------------------------------------------

def outPolygon(x, y, poly):
    """
    DES: check whether point (x,y) is outside a polygon
    INP: (float)        x/y : coordinates of point
         (float array) poly : vertices of polygon
    OUT: (int)              : 1=outside, 0=inside polygon
    """
    counter = 0
    p1 = poly[0]
    for i in np.arange(1, len(poly)+1):
        p2 = poly[i % len(poly)]
        if y > min(p1[1], p2[1]):
            if y <= max(p1[1], p2[1]):
                if x <= max(p1[0], p2[0]):
                    if p1[1] != p2[1]:
                        xinters = (y-p1[1])*(p1[0]-p2[0])/(p1[1]-p2[1])+p1[0]
                        if p1[0] == p2[0] or x <= xinters:
                            counter = counter+1
        p1 = p2
    return (counter+1) % 2

def as_column_major_storage(obj):
    return np.asarray(obj, order='F')
