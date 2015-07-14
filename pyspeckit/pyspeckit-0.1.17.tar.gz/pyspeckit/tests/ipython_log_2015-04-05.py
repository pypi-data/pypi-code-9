########################################################
# Started Logging At: 2015-04-05 18:39:10
########################################################

cube = SpectralCube.read('G203.04+1.76_h2co.fits')
simpleFakeCube = np.empty([25,2,2])
xarr = np.linspace(-20,20,25)
simpleFakeCube[0,0] = np.exp(-(xarr-1)**2/(2*3.**2))
simpleFakeCube[:,0,0] = np.exp(-(xarr-1)**2/(2*3.**2))
simpleFakeCube[:,1,0] = np.exp(-(xarr+1)**2/(2*3.**2))
simpleFakeCube[:,0,1] = np.exp(-(xarr+1)**2/(2*4.**2))
simpleFakeCube[:,1,1] = np.exp(-(xarr-1)**2/(2*4.**2))
get_ipython().set_next_input(u'sc = SpectralCube');get_ipython().magic(u'pinfo SpectralCube')
sc = SpectralCube(data=data, wcs=wcs.WCS(), meta={'BUNIT': 'K'})
sc = SpectralCube(data=simpleFakeCube, wcs=wcs.WCS(), meta={'BUNIT': 'K'})
sc = SpectralCube(data=simpleFakeCube, wcs=wcs.WCS(naxis=3), meta={'BUNIT': 'K'})
wcs.WCS(naxis=3)
get_ipython().magic(u'pinfo wcs.WCS')
wcs.WCS(naxis=3, header={'CUNIT1': 'km s-1', 'CDELT1':1.0, 'CRVAL1': 0, 'CRPIX1': 12.5, 'CTYPE2':'DEC--TAN', 'CTYPE3': 'RA---TAN', 'CDELT2':1./3600, 'CDELT3': 1/3600., 'CRVAL2': 25.0, 'CRVAL3': 12.0, 'CRPIX2': 1, 'CRPIX3': 1})
w = wcs.WCS(naxis=3, header={'CUNIT1': 'km s-1', 'CDELT1':1.0, 'CRVAL1': 0, 'CRPIX1': 12.5, 'CTYPE2':'DEC--TAN', 'CTYPE3': 'RA---TAN', 'CDELT2':1./3600, 'CDELT3': 1/3600., 'CRVAL2': 25.0, 'CRVAL3': 12.0, 'CRPIX2': 1, 'CRPIX3': 1})
sc = SpectralCube(data=simpleFakeCube, wcs=wcs.WCS(naxis=3), meta={'BUNIT': 'K'})
sc = SpectralCube(data=simpleFakeCube, wcs=w, meta={'BUNIT': 'K'})
get_ipython().magic(u'history ')
get_ipython().magic(u'paste')
import numpy as np

def make_fake_cube():
    from spectral_cube import SpectralCube

    simpleFakeCube = np.empty([25,2,2])
    xarr = np.linspace(-20,20,25)
    simpleFakeCube[:,0,0] = np.exp(-(xarr-1)**2/(2*3.**2))
    simpleFakeCube[:,1,0] = np.exp(-(xarr+1)**2/(2*3.**2))
    simpleFakeCube[:,0,1] = np.exp(-(xarr+1)**2/(2*4.**2))
    simpleFakeCube[:,1,1] = np.exp(-(xarr-1)**2/(2*4.**2))

    w = wcs.WCS(naxis=3, header={'CUNIT1': 'km s-1', 'CDELT1':1.0, 'CRVAL1': 0,
                                 'CRPIX1': 12.5, 'CTYPE2':'DEC--TAN', 'CTYPE3':
                                 'RA---TAN', 'CDELT2':1./3600, 'CDELT3':
                                 1/3600., 'CRVAL2': 25.0, 'CRVAL3': 12.0,
                                 'CRPIX2': 1, 'CRPIX3': 1})
    sc = SpectralCube(data=simpleFakeCube, wcs=w, meta={'BUNIT': 'K'})

    return sc
make_fake_cube9)
make_fake_cube()
get_ipython().magic(u'run ~/repos/pyspeckit/pyspeckit/tests/test_spectral_cube.py')
make_fake_cube()
get_ipython().magic(u'run ~/repos/pyspeckit/pyspeckit/tests/test_spectral_cube.py')
make_fake_cube()
get_ipython().magic(u'run ~/repos/pyspeckit/pyspeckit/tests/test_spectral_cube.py')
make_fake_cube()
get_ipython().magic(u'run ~/repos/pyspeckit/pyspeckit/tests/test_spectral_cube.py')
pc = test_load_cube_from_spectralcube()
pc
pc.mapplot()
pc.unit
pc.xarr
pc.xarr.unit
########################################################
# Started Logging At: 2015-04-05 18:55:24
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
sp.plotter()
sp.specfit.moments
get_ipython().magic(u'pinfo sp.specfit.moments')
get_ipython().magic(u'pinfo2 sp.specfit.moments')
sp.specfit.moments()
sp.specfit.selectregion(xmin=60, xmax=130)
sp.specfit.moments()
sp.specfit.moments()
sp.specfit.moments()
sp.specfit.highlight_fitregion()
sp.specfit.moments(fittype='gaussian')
sp.specfit.Registry.multifitters['gaussian'].moments
get_ipython().set_next_input(u"sp.specfit.Registry.multifitters['gaussian'].moments");get_ipython().magic(u'pinfo2 moments')
m = sp.specfit.Registry.multifitters['gaussian'].moments
get_ipython().magic(u'pinfo2 m')
sp.specfit.spectofit.shape
sp.specfit.spectofit
sp.specfit.xmin
sp.specfit.xmax
pyspeckit.moments.moments(sp.xarr[sp.specfit.xmin:sp.specfit.xmax], sp.data[sp.specfit.xmin:sp.specfit.xmax])
sp.specfit.moments(fittype='gaussian')
get_ipython().magic(u'pinfo2 m')
sp.specfit.moments(fittype='gaussian')
g = sp.specfit.Registry.multifitters['gaussian']
g
get_ipython().magic(u'pinfo2 g')
m(sp.xarr[sp.specfit.xmin:sp.specfit.xmax], sp.data[sp.specfit.xmin:sp.specfit.xmax])
sp.specfit.moments(fittype='gaussian')
m = sp.specfit.Registry.multifitters['gaussian'].moments
None or 'yes'
'no' or 'yes'
'no' or None
None or None
sp.specfit.fittype
get_ipython().magic(u'history ')
########################################################
# Started Logging At: 2015-04-05 19:09:49
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
sp.plotter()
sp.specfit.selectregion(xmin=60, xmax=130)
sp.specfit.highlight_fitregion()
sp.specfit.moments()
sp.specfit.moments(fittype='gaussian')
m = sp.specfit.Registry.multifitters['gaussian'].moments
m(sp.xarr[sp.specfit.xmin:sp.specfit.xmax], sp.data[sp.specfit.xmin:sp.specfit.xmax])
m(sp.xarr[sp.specfit.xmin:sp.specfit.xmax], sp.specfit.spectofit[sp.specfit.xmin:sp.specfit.xmax])
sp.specfit.spectofit.shape
sp.specfit.xmin, sp.specfit.xmax
sp.specfit.spectofit == sp.data
sp.baseline
sp.baseline.subtracted
sp.baseline.basespec
sp.baseline.basespec.max()
sp.baseline.basespec.size
sp.specfit.errspec
pl.figure()
pl.plot(sp.specfit.spectofit-sp.data)
pl.plot(sp.specfit.spectofit)
pl.plot(sp.specfit.data)
pl.plot(sp.data)
self = sp.specfit
self.spectofit[self.xmin:self.xmax].max() - self.spectofit[self.xmin:self.xmax].min()
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
pl.plot(sp.data)
pl.plot(sp.specfit.data)
pl.plot(sp.specfit.spectofit)
get_ipython().magic(u'history ')
sp.xarr
sp.data
sp.specfit.spectofit
np.ma.copy(sp.data)
sp.data.sum()
y = np.ma.copy(sp.data)
y - sp.baseline.basespec
y -= sp.baseline.basespec
y
sp.specfit.xmin
sp.specfit.xmax
sp.data == sp.specfit.spectofit
sp.data == sp.specfit.spectofit[::-1]
get_ipython().magic(u'history ')
########################################################
# Started Logging At: 2015-04-05 19:24:18
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
sp.data == sp.specfit.spectofit
sp.data == sp.specfit.spectofit[::-1]
get_ipython().magic(u'history ')
########################################################
# Started Logging At: 2015-04-05 19:27:03
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
########################################################
# Started Logging At: 2015-04-05 19:28:27
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
sp.plotter()
sp.specfit.selectregion(xmin=60, xmax=130)
sp.specfit.highlight_fitregion()
sp.specfit.moments()
from pyspeckit.wrappers import fitnh3
fitnh3.fitnh3tkin({'oneone':'G032.020+00.065_nh3_11_Tastar.fits', 'twotwo':'G032.020+00.065_nh3_22_Tastar.fits'})
get_ipython().magic(u'history ')
########################################################
# Started Logging At: 2015-04-05 19:31:58
########################################################

import pyspeckit
sp.plotter()
sp.specfit.selectregion(xmin=60, xmax=130)
sp.specfit.highlight_fitregion()
sp.specfit.moments()
from pyspeckit.wrappers import fitnh3
fitnh3.fitnh3tkin({'oneone':'G032.020+00.065_nh3_11_Tastar.fits', 'twotwo':'G032.020+00.065_nh3_22_Tastar.fits'})
import pyspeckit
sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')
sp.plotter()
sp.specfit.selectregion(xmin=60, xmax=130)
sp.specfit.highlight_fitregion()
sp.specfit.moments()
from pyspeckit.wrappers import fitnh3
fitnh3.fitnh3tkin({'oneone':'G032.020+00.065_nh3_11_Tastar.fits', 'twotwo':'G032.020+00.065_nh3_22_Tastar.fits'})
get_ipython().magic(u'debug')
fitnh3.fitnh3tkin({'oneone':'G032.020+00.065_nh3_11_Tastar.fits', 'twotwo':'G032.020+00.065_nh3_22_Tastar.fits'}, crop=[60,130])
get_ipython().magic(u'run test_nh3_multi.py')
get_ipython().magic(u'run test_nh3_multi.py')
pl.draw(); pl.show()
guesses = sp2.specfit.moments(fittype='gaussian')[1:]
guesses = sp2.specfit.moments(fittype='gaussian')[1:]
guesses = sp2.specfit.moments(fittype='gaussian')[1:]
sp2.plotter()
sp2.plotter.axis
sp2.plotter.figure.number
sp2.specfit.spectofit
sp2.specfit.spectofit.shape
sp2.data.shape
########################################################
# Started Logging At: 2015-04-05 19:35:39
########################################################

get_ipython().magic(u'run test_nh3_multi.py')
sp2.data.shape
sp2.specfit.spectofit.shape
sp2.specfit.setfitspec()
sp2.data.shape
########################################################
# Started Logging At: 2015-04-05 19:37:18
########################################################

get_ipython().magic(u'run test_nh3_multi.py')
get_ipython().magic(u'run test_nh3_multi.py')
########################################################
# Started Logging At: 2015-04-05 19:39:27
########################################################

pl.draw(); pl.show()
########################################################
# Started Logging At: 2015-04-05 19:40:01
########################################################

import log
import logging
from astropy import log
########################################################
# Started Logging At: 2015-04-05 19:41:38
########################################################

########################################################
# Started Logging At: 2015-04-05 19:44:13
########################################################

