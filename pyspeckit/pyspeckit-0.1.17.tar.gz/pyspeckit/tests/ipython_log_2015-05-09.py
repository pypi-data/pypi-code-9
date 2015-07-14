########################################################
# Started Logging At: 2015-05-09 09:15:07
########################################################

sp.specfit.parinfo
get_ipython().magic(u'run test_masking.py')
sp.specfit.parinfo
sp.specfit.parinfo
chi2_a
get_ipython().magic(u'run test_masking.py')
chi2_a
np.ma.masked_where
y2 = np.ma.masked_where(np.abs(x)>40, y)
y2
y
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
(sp2.data-y)**2/error**2
get_ipython().magic(u'run test_masking.py')
((sp2.data-y)**2/error**2)
((sp2.data-y)**2/error**2).sum()
get_ipython().magic(u'run test_masking.py')
chi2b - chi2_b_correct
chi2_b - chi2_b_correct
sp2.specfit.model
sp2.specfit.model.shape
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
sp2.specfit.model.shape
sp2.specfit.model.shape
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
sp.specfit.chi2
sp.specfit.dof
sp2.specfit.dof
mask_out.sum()
get_ipython().magic(u'paste')
x = np.linspace(-50,50)
y = np.exp(-x**2/(5.**2*2))
error = np.ones_like(x,dtype='float')/10.
e = np.random.randn(x.size) * error

sp = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y+e,
                        error=error, header={})
sp.specfit(fittype='gaussian', guesses=[1,0,1])

chi2_a = sp.specfit.chi2
chi2_a = sp.specfit.chi2
chi2_a_correct = ((sp.data-sp.specfit.model)**2/error**2).sum()
np.testing.assert_almost_equal(chi2_a, chi2_a_correct)

mask_out = np.abs(x)>40
y2 = np.ma.masked_where(mask_out, y)
sp2 = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y2+e,
                         error=error, header={})
sp2.specfit(fittype='gaussian', guesses=[1,0,1])
assert sp2.specfit.dof

chi2_b = sp2.specfit.chi2
chi2_b_correct = ((sp2.data-sp2.specfit.model)**2/error**2).sum()
np.testing.assert_almost_equal(chi2_b, chi2_b_correct)
chi2_b_correct2 = ((sp2.data[~mask_out] - sp2.specfit.model[~mask_out])**2
                   / error[~mask_out]**2).sum()
np.testing.assert_almost_equal(chi2_b_correct, chi2_b_correct2)
mask_out.sum()
sp2.specfit.fitter.npars
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
sp.specfit.includemask()
sp.specfit.includemask
sp.specfit.includemask.shape
sp2.specfit.includemask.shape
sp2.specfit.mask
sp2.specfit.mask.shape
sp.specfit.mask.shape
sp2.specfit.spectofit
sp2.specfit.spectofit.mask
self=sp2.specfit
(hasattr(self.spectofit, 'mask') and
            self.spectofit.shape==self.spectofit.mask.shape)
sp2.data
sp.data.sum()
sp.data
np.ma.copy(sp2.data)
sp2.data
sp2.baseline
sp2.baseline.subtracted
sp2.baseline.basespec
cop = np.ma.copy(sp2.data)
kcop
cop
cop -= sp2.baseline.basespec
sop
sop
cop
OKmask
OKmask = cop==cop
OKmask
cop[~OKmask]
cop[~OKmask] = 0
cop
mask_out = np.abs(x)>40
y2 = np.ma.masked_where(mask_out, y)
sp2 = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y2+e,
                         error=error, header={})
sp2.specfit.spectofit
y2
y2+e
sp.data
sp2.data
sp2.data.mask
sp2.spectofit.mask
sp2.specfit.spectofit.mask
get_ipython().magic(u'run test_masking.py')
########################################################
# Started Logging At: 2015-05-09 09:35:02
########################################################

get_ipython().magic(u'debug')
########################################################
# Started Logging At: 2015-05-09 12:37:55
########################################################

get_ipython().magic(u'debug')
########################################################
# Started Logging At: 2015-05-09 12:43:01
########################################################

get_ipython().magic(u'debug')
sp2.plotter()
get_ipython().magic(u'paste')
sp = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y+e,
                        error=error, header={})
sp.specfit(fittype='gaussian', guesses=[1,0,1])
assert sp.specfit.dof == x.size - sp.specfit.fitter.npars

chi2_a = sp.specfit.chi2
chi2_a = sp.specfit.chi2
chi2_a_correct = ((sp.data-sp.specfit.model)**2/error**2).sum()
np.testing.assert_almost_equal(chi2_a, chi2_a_correct)

mask_out = np.abs(x)>40
y2 = np.ma.masked_where(mask_out, y)
sp2 = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y2+e,
                         error=error, header={})
sp2.specfit(fittype='gaussian', guesses=[1,0,1])
assert sp2.specfit.dof == x.size - mask_out.sum() - sp2.specfit.fitter.npars

chi2_b = sp2.specfit.chi2
chi2_b_correct = ((sp2.data-sp2.specfit.model)**2/error**2).sum()
np.testing.assert_almost_equal(chi2_b, chi2_b_correct)
chi2_b_correct2 = ((sp2.data[~mask_out] - sp2.specfit.model[~mask_out])**2
                   / error[~mask_out]**2).sum()
np.testing.assert_almost_equal(chi2_b_correct, chi2_b_correct2)
sp2.plotter()
sp2.specfit(fittype='gaussian', guesses=[1,0,1])
sp2.specfit.plotresiduals()
sp2.specfit.get_full_model()
sp2.specfit.get_full_model().shape
get_ipython().magic(u'run test_masking.py')
get_ipython().magic(u'run test_masking.py')
########################################################
# Started Logging At: 2015-05-09 12:48:08
########################################################

########################################################
# Started Logging At: 2015-05-09 12:49:14
########################################################

