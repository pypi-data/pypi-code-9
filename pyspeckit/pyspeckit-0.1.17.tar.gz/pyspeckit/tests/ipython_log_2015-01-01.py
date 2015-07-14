########################################################
# Started Logging At: 2015-01-01 13:15:34
########################################################

from pyspeckit.spectrum.models import ammonia
get_ipython().magic(u'pinfo ammonia.ammonia')
amp_idl = [0.074073D, 0.037037D, 0.083333D, 0.009260D, 0.046297D, 0.016667D, 0.046297D, 0.233333D, 0.009260D,
 0.150000D, 0.016667D, 0.009260D, 0.018518D, 0.009260D, 0.083333D, 0.046297D, 0.074073D, 0.037037D]
amp_idl = [float(x) for x in "0.074073D, 0.037037D, 0.083333D, 0.009260D, 0.046297D, 0.016667D, 0.046297D, 0.233333D, 0.009260D,
 0.150000D, 0.016667D, 0.009260D, 0.018518D, 0.009260D, 0.083333D, 0.046297D, 0.074073D, 0.037037D".replace("D","").split(", ")]
amp_idl = [float(x) for x in "0.074073D, 0.037037D, 0.083333D, 0.009260D, 0.046297D, 0.016667D, 0.046297D, 0.233333D, 0.009260D, 0.150000D, 0.016667D, 0.009260D, 0.018518D, 0.009260D, 0.083333D, 0.046297D, 0.074073D, 0.037037D".replace("D","").split(", ")]
vel_idl = [float(x) for x in "[-19.5492D,-19.4106D, -7.8153D, -7.3732D, -7.2340D, -0.2515D, -0.2131D, -0.1327D, -0.0745D, $
0.1909D,  0.3099D,  0.3226D,  0.4613D,  7.3507D,  7.4695D,  7.8865D, 19.3177D, 19.8516D]
vel_idl = [float(x) for x in "-19.5492D,-19.4106D, -7.8153D, -7.3732D, -7.2340D, -0.2515D, -0.2131D, -0.1327D, -0.0745D, 0.1909D,  0.3099D,  0.3226D,  0.4613D,  7.3507D,  7.4695D,  7.8865D, 19.3177D, 19.8516D".replace("D","").split(", ")]
vel_idl = [float(x) for x in "-19.5492D,-19.4106D, -7.8153D, -7.3732D, -7.2340D, -0.2515D, -0.2131D, -0.1327D, -0.0745D, 0.1909D,  0.3099D,  0.3226D,  0.4613D,  7.3507D,  7.4695D,  7.8865D, 19.3177D, 19.8516D".replace("D","").split(",")]
dict(vel_idl, amp_idl)
dict(zip(vel_idl, amp_idl))
didl = dict(zip(vel_idl, amp_idl))
dpy = dict(zip([19.8513, 19.3159, 7.88669, 7.46967, 7.35132, 0.460409, 0.322042,
        -0.0751680, -0.213003, 0.311034, 0.192266, -0.132382, -0.250923, -7.23349,
        -7.37280, -7.81526, -19.4117, -19.5500],[0.0740740, 0.148148, 0.0925930, 0.166667, 0.0185190, 0.0370370,
        0.0185190, 0.0185190, 0.0925930, 0.0333330, 0.300000, 0.466667,
        0.0333330, 0.0925930, 0.0185190, 0.166667, 0.0740740, 0.148148]))
dpy
didl
np.sum(dpy.values())
dpy = dict(zip([19.8513, 19.3159, 7.88669, 7.46967, 7.35132, 0.460409, 0.322042,
        -0.0751680, -0.213003, 0.311034, 0.192266, -0.132382, -0.250923, -7.23349,
        -7.37280, -7.81526, -19.4117, -19.5500], np.array([0.0740740, 0.148148, 0.0925930, 0.166667, 0.0185190, 0.0370370,
        0.0185190, 0.0185190, 0.0925930, 0.0333330, 0.300000, 0.466667,
        0.0333330, 0.0925930, 0.0185190, 0.166667, 0.0740740, 0.148148])/2.))
dpy
didl
get_ipython().magic(u'run test_nh3_model.py')
get_ipython().magic(u'run test_nh3_model.py')
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str, 20, 20)
test_eriks_idl(testspec_idl_str, 10, 30)
get_ipython().magic(u'pdb')
test_eriks_idl(testspec_idl_str, 10, 30)
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str, 20, 20, plot=True)
test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
get_ipython().magic(u'run test_nh3_model.py')
afd = test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
afd
np.array(afd)
get_ipython().magic(u'r')
get_ipython().magic(u'run test_nh3_model.py')
afd = test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
get_ipython().magic(u'run test_nh3_model.py')
afd = test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
ad
afd
afd = test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
np.nanmax(afd)
get_ipython().magic(u'run test_nh3_model.py')
np.nanmax(afd)
afd = test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
get_ipython().magic(u'pinfo ammonia.ammonia')
get_ipython().magic(u'pinfo ammonia.ammonia')
refX = 23.6944955e9 # from nh3model.pro
refX = 23.694506e9 # from modelspec.pro
xarr11 = pyspeckit.units.SpectroscopicAxis(np.arange(-30,30,0.4),
        units='km/s', refX=refX, refX_units='Hz', frame='LSRK',
        xtype='Frequency')
# The two arrays are shifted in frequency because nh3model.pro converts to
# frequency with a different reference; the reference frequency is not centered
# on any of the individual lines
#print np.array(xarr11.as_unit('Hz')) - idl_test_xarr
ps_spectrum = ammonia.ammonia(xarr11, tkin=tkin, tex=tex, ntot=14, width=1,
                              xoff_v=0.0, fortho=0.5, )
tkin=30
tex=20
ps_spectrum = ammonia.ammonia(xarr11, tkin=tkin, tex=tex, ntot=14, width=1,
                              xoff_v=0.0, fortho=0.5, )
ps_spectrum
np.array(ps_spectrum)
get_ipython().magic(u'run test_nh3_model.py')
test_eriks_idl(testspec_idl_str2, tex=10, tkin=30, plot=True)
#amp_idl = [float(x) for x in "0.074073D, 0.037037D, 0.083333D, 0.009260D, 0.046297D, 0.016667D, 0.046297D, 0.233333D, 0.009260D, 0.150000D, 0.016667D, 0.009260D, 0.018518D, 0.009260D, 0.083333D, 0.046297D, 0.074073D, 0.037037D".replace("D","").split(", ")]
amp_idl.sum()
np.array(amp_idl).sum()
ammonia.tau_wts_dict['oneone']
ammonia.tau_wts_dict['oneone'].sum()
np.sum(ammonia.tau_wts_dict['oneone'].sum())
np.sum(ammonia.tau_wts_dict['oneone'])
np.array(amp_idl).max()
get_ipython().magic(u'cd ')
