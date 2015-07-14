########################################################
# Started Logging At: 2015-03-25 08:39:51
########################################################

get_ipython().magic(u'pinfo pyspeckit.moments.moments')
amp,cen,wid = pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
amp
sp.specfit(negamp=False,debug=True,fittype='gaussian', guesses=[amp,cen,wid])
amp
sp[-100:300]
get_ipython().magic(u'pinfo sp.slice')
sp_whole = pyspeckit.Spectrum('G031.947+00.076_nh3_11_Tastar.fits')#,wcstype='F')
sp = sp_whole.slice(-100, 300, units='km/s', copy=False)
amp,cen,wid = pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
amp
cen
wid
sp.specfit(negamp=False,debug=True,fittype='gaussian', guesses=[amp,cen,wid])
get_ipython().magic(u'run test_nh3.py')
get_ipython().magic(u'run test_nh3.py')
sp
amp
amp,cen,wid = pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
sp.plotter()
pl.draw(); pl.show()
sp = sp_whole.slice(60, 120, units='km/s', copy=False)
pl.draw(); pl.show()
sp.plotter()
get_ipython().magic(u'run test_nh3.py')
get_ipython().magic(u'run test_nh3.py')
get_ipython().magic(u'debug')
########################################################
# Started Logging At: 2015-03-25 08:46:30
########################################################

get_ipython().magic(u'debug')
########################################################
# Started Logging At: 2015-03-25 08:48:00
########################################################

taudict['oneone']
########################################################
# Started Logging At: 2015-03-25 09:28:16
########################################################

6.5/300
(0.02*u.pc/(1*u.arcsec)).to(u.pc, u.dimensionless_angles())
get_ipython().magic(u'debug')
taudict1 = ammonia.ammonia(sp.xarr, tkin=sp.specfit.parinfo.tkin0.value,
                           tex=sp.specfit.parinfo.tex0.value,
                           ntot=sp.specfit.parinfo.ntot0.value,
                           width=sp.specfit.parinfo.width0.value,
                           return_tau=True)
taudict2 = ammonia.ammonia(sp.xarr, tkin=sp.specfit.parinfo.tkin1.value,
                           tex=sp.specfit.parinfo.tex1.value,
                           ntot=sp.specfit.parinfo.ntot1.value,
                           width=sp.specfit.parinfo.width1.value,
                           return_tau=True)
taudict1
taudict2
get_ipython().magic(u'run test_nh3.py')
taudict1['oneone']
taudict2['oneone']
pl.draw(); pl.show()
########################################################
# Started Logging At: 2015-03-25 17:56:40
########################################################

########################################################
# Started Logging At: 2015-03-25 18:04:02
########################################################

########################################################
# Started Logging At: 2015-03-25 18:24:55
########################################################

get_ipython().magic(u'run test_nh3_model.py')
get_ipython().magic(u'run test_nh3_model.py')
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str, 20, 10, plot=True)
pl.draw(); pl.show()
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10)
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10, plot=True)
pl.draw(); pl.show()
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10, background_tb=2.73)
get_ipython().magic(u'run test_nh3_model.py')
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10, plot=True)
pl.draw(); pl.show()
########################################################
# Started Logging At: 2015-03-25 18:32:55
########################################################

########################################################
# Started Logging At: 2015-03-25 18:33:06
########################################################

pl.draw(); pl.show()
from pyspeckit.tests import nh3_model
from pyspeckit.tests import test_nh3_model
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10)
test_eriks_idl(testspec_idl_str=testspec_idl_str2, tex=20, tkin=30)
pl.draw(); pl.show()
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10, plot=True)
pl.draw(); pl.show()
########################################################
# Started Logging At: 2015-03-25 18:36:30
########################################################

test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=10, plot=True)
pl.draw(); pl.show()
########################################################
# Started Logging At: 2015-03-25 18:37:12
########################################################

########################################################
# Started Logging At: 2015-03-25 18:38:09
########################################################

get_ipython().magic(u'run test_nh3_model_ok.py')
pl.draw(); pl.show()
get_ipython().magic(u'run test_nh3_model_ok.py')
pl.draw(); pl.show()
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=20, plot=True)
########################################################
# Started Logging At: 2015-03-25 18:40:10
########################################################

test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=20)
test_eriks_idl(testspec_idl_str=testspec_idl_str2, tex=10, tkin=30)
########################################################
# Started Logging At: 2015-03-25 18:41:32
########################################################

get_ipython().magic(u'run test_nh3_model.py')
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str=testspec_idl_str,  tex=20, tkin=20)
test_eriks_idl(testspec_idl_str=testspec_idl_str2, tex=10, tkin=30)
get_ipython().magic(u'run test_nh3_multi.py')
get_ipython().magic(u'run test_nh3_multi.py')
get_ipython().magic(u'run test_nh3_multi.py')
get_ipython().magic(u'run test_nh3_multi.py')
pl.draw(); pl.show()
taudict
########################################################
# Started Logging At: 2015-03-25 18:55:20
########################################################

mask = fits.getdata('/Users/adam/work/cara/vla/hotclump_11_mask.fits')
mask
mask.shape
pl.imshow(mask)
pl.draw(); pl.show()
pl.clf()
pl.imshow(mask)
pl.draw(); pl.show()
pl.draw(); pl.show()
pl.draw(); pl.show()
mask[200:202,200:202]
mask[150:152,200:202]
mask = np.isfinite(mask) * (mask > 0)
pl.imshow(mask)
mask[150:152,150:152]
cube = SpectralCube.read('/Users/adam/work/cara/vla/hotclump_11.cube_r0.5_rerun.image.fits')
cube = SpectralCube.read('/Users/adam/work/cara/vla/hotclump_11.cube_r0.5_3sig_32_220_v2.image.fitscube_r0.5_rerun.image.fits')
cube = SpectralCube.read('/Users/adam/work/cara/vla/hotclump_11.cube_r0.5_3sig_32_220_v2.image.fits')
cube = SpectralCube.read('/Users/adam/work/cara/vla/hotclump_11.cube_r0.5_3sig_32_220_v2.image.fits')
get_ipython().magic(u"ls -lh ('/Users/adam/work/cara/vla/hotclump_11.cube_r0.5_3sig_32_220_v2.image.fits')")
get_ipython().magic(u'ls -lh /Users/adam/work/cara/vla/hotclump_11.cube_r0.5_3sig_32_220_v2.image.fits')
