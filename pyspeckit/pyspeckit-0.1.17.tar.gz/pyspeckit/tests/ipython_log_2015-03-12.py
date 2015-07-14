########################################################
# Started Logging At: 2015-03-12 18:16:48
########################################################

########################################################
# # Started Logging At: 2015-03-12 18:16:48
########################################################
import pylab as pl
pl.draw(); pl.show()
########################################################
# Started Logging At: 2015-03-12 18:18:01
########################################################

########################################################
# # Started Logging At: 2015-03-12 18:18:01
########################################################
########################################################
# Started Logging At: 2015-03-12 18:18:53
########################################################

########################################################
# # Started Logging At: 2015-03-12 18:18:53
########################################################
########################################################
# Started Logging At: 2015-03-12 18:27:22
########################################################

########################################################
# # Started Logging At: 2015-03-12 18:27:23
########################################################
get_ipython().magic(u'run test_fits.py')
sp.specfit()
sp.specfit(guesses=[0,1,2])
sp.plotter()
sp.specfit(guesses=[0,1,2])
sp.specfit(guesses=[1,70000,2000])
sp.specfit.parinfo
sp.specfit.parinfo.WIDTH0
fitted_fwhm = sp.specfit.parinfo.WIDTH0*np.sqrt(np.log(2)*8)
measured_fwhm2 = sp.specfit.measure_approximate_fwhm(interpolate_factor=10)
fitted_fwhm
measured_fwhm2
########################################################
# Started Logging At: 2015-03-12 18:30:04
########################################################

########################################################
# # Started Logging At: 2015-03-12 18:30:04
########################################################
sp.specfit.plot_fit()
sp.specfit.parinfo
get_ipython().magic(u'paste')
import pyspeckit
import numpy as np

if not 'interactive' in globals():
    interactive=False
if not 'savedir' in globals():
    savedir = ''

sp = pyspeckit.Spectrum('sample_13CO.fits')

print "Does it have an axis? ",sp.plotter.axis
sp.plotter()
print "How about now? ",sp.plotter.axis


# set the baseline to zero to prevent variable-height fitting
# (if you don't do this, the best fit to the spectrum is dominated by the
# background level)
sp.baseline.order = 0
sp.specfit()
########################################################
# Started Logging At: 2015-03-12 18:34:45
########################################################

get_ipython().magic(u'ls *fits')
import pyspeckit
sp = pyspeckit.Spectrum('test.fits')
sp.plotter()
sp = pyspeckit.Spectrum('sample_sdss.fits')
sp.plotter()
sp.specfit.add_sliders()
pl.figure()
