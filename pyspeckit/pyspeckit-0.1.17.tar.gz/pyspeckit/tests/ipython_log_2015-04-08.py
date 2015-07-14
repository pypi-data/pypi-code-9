########################################################
# Started Logging At: 2015-04-08 13:23:52
########################################################

########################################################
# # Started Logging At: 2015-04-08 13:23:52
########################################################
sp.xarr
sp.xarr.equivalencies
########################################################
# Started Logging At: 2015-04-08 19:19:38
########################################################

########################################################
# # Started Logging At: 2015-04-08 19:19:39
########################################################
########################################################
# Started Logging At: 2015-04-08 19:24:33
########################################################

########################################################
# # Started Logging At: 2015-04-08 19:24:33
########################################################
test_everything()
u.Hz
from astropy import units as u
u.Hz
u.Hz.physical_type
x = np.arange(5)*u.Hz
np.zeros_like(x)
pl.plot(x, x*u.Jt)
pl.plot(x, x*u.Jy)
import pylab as pl
pl.plot(x, x*u.Jy)
fig = pl.gcf()
#event2 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,850,280,button=1)
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', fig.canvas,850,280,button=1)
event2.ydata
event2.xdata
get_ipython().magic(u'pinfo matplotlib.backend_bases.MouseEvent')
pl.draw(); pl.show()
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', fig.canvas,850,280,button=1)
event2.xdata
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', pl.gcf().canvas,850,280,button=1)
event2.xdata
get_ipython().magic(u'pinfo matplotlib.backend_bases.MouseEvent')
event2 = matplotlib.backend_bases.MouseEvent(name='button_press_event', canvas=pl.gcf().canvas, x=850, y=280,button=1)
event2.xdata
fig = plt.figure()
import pylab as plt
get_ipython().magic(u'paste')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
pl.ion()
get_ipython().magic(u'paste')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
event2.xdata
event2.xdata = 850
event2.xdata
########################################################
# Started Logging At: 2015-04-08 19:49:01
########################################################

get_ipython().magic(u'ls *fit')
get_ipython().magic(u'ls *fits')
get_ipython().magic(u'ls data/')
import pyspeckit
spc = pyspeckit.Cube('data/region5_hcn_crop.fits')
spc.mapplot()
sp1 = spc.get_spectrum(30,30)
sp1
sp1.xarr
spc.xarr
########################################################
# Started Logging At: 2015-04-08 20:12:49
########################################################

cube = SpectralCube.read('data/region5_hcn_crop.fits')
cube.wcs.wcs.spec
cube.wcs.wcs
cube.wcs.wcs.ctype
cube.wcs.wcs.spec
cube.wcs.wcs.spec
cube = SpectralCube.read('data/region5_hcn_crop.fits')
cube.wcs.wcs.spec
cube.wcs.wcs.spec
cube.wcs.wcs.spec
cube.wcs.wcs
cube.wcs.wcs.spec
cube = SpectralCube.read('data/region5_hcn_crop.fits')
cube.wcs.wcs.spcfix()
cube.wcs.wcs.spec
cube.wcs.wcs.fix()
cube.wcs.wcs.spec
cube = SpectralCube.read('data/region5_hcn_crop.fits')
cube.wcs.wcs.fix()
cube.wcs.wcs.spec
get_ipython().magic(u'pinfo cube.wcs.wcs.fix')
cube.wcs.wcs.celfix
cube.wcs.wcs.axis_types
cube.wcs.get_axis_types()
cube.wcs.wcs.ctype
2200 // 1000
cube.wcs.wcs.axis_types
