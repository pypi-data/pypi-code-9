
# The change in the CMB intensity due to Compton scattering of CMB
# photons off of thermal electrons in galaxy clusters, otherwise known as the
# Sunyaev-Zeldovich (S-Z) effect, can to a reasonable approximation be represented by a
# projection of the pressure field of a cluster. However, the *full* S-Z signal is a combination of thermal and kinetic
# contributions, and for large frequencies and high temperatures
# relativistic effects are important. For computing the full S-Z signal
# incorporating all of these effects, there is a library:
# SZpack ([Chluba et al 2012](http://adsabs.harvard.edu/abs/2012MNRAS.426..510C)). 
# 
# The `sunyaev_zeldovich` analysis module in yt makes it possible
# to make projections of the full S-Z signal given the properties of the
# thermal gas in the simulation using SZpack. SZpack has several different options for computing the S-Z signal, from full
# integrations to very good approximations.  Since a full or even a
# partial integration of the signal for each cell in the projection
# would be prohibitively expensive, we use the method outlined in
# [Chluba et al 2013](http://adsabs.harvard.edu/abs/2013MNRAS.430.3054C) to expand the
# total S-Z signal in terms of moments of the projected optical depth $\tau$, projected electron temperature $T_e$, and
# velocities $\beta_{c,\parallel}$ and $\beta_{c,\perp}$ (their equation 18):

# $$S(\tau, T_{e},\beta_{c,\parallel},\beta_{\rm c,\perp}) \approx S_{\rm iso}^{(0)} + S_{\rm iso}^{(2)}\omega^{(1)} + C_{\rm iso}^{(1)}\sigma^{(1)} + D_{\rm iso}^{(2)}\kappa^{(1)} + E_{\rm iso}^{(2)}\beta_{\rm c,\perp,SZ}^2 +~...$$
# 

# yt makes projections of the various moments needed for the
# calculation, and then the resulting projected fields are used to
# compute the S-Z signal. In our implementation, the expansion is carried out to first-order
# terms in $T_e$ and zeroth-order terms in $\beta_{c,\parallel}$ by default, but terms up to second-order in can be optionally
# included. 

### Installing SZpack

# SZpack can be downloaded [here](http://www.cita.utoronto.ca/~jchluba/Science_Jens/SZpack/SZpack.html). Make
# sure you install a version later than v1.1.1. For computing the S-Z
# integrals, SZpack requires the [GNU Scientific Library](http://www.gnu.org/software/gsl/). For compiling
# the Python module, you need to have a recent version of [swig](http://www.swig.org>) installed. After running `make` in the top-level SZpack directory, you'll need to run it in the `python` subdirectory, which is the
# location of the `SZpack` module. You may have to include this location in the `PYTHONPATH` environment variable.
# 

### Creating S-Z Projections

# Once you have SZpack installed, making S-Z projections from yt
# datasets is fairly straightforward:

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import yt
from yt.analysis_modules.sunyaev_zeldovich.api import SZProjection

ds = yt.load("enzo_tiny_cosmology/DD0046/DD0046")

freqs = [90.,180.,240.]
szprj = SZProjection(ds, freqs)


# `freqs` is a list or array of frequencies in GHz at which the signal
# is to be computed. The `SZProjection` constructor also accepts the
# optional keywords, `mue` (mean molecular weight for computing the
# electron number density, 1.143 is the default) and `high_order` (set
# to True to compute terms in the S-Z signal expansion up to
# second-order in $T_{e,SZ}$ and $\beta$). 

# Once you have created the `SZProjection` object, you can use it to
# make on-axis and off-axis projections:

# In[ ]:

# An on-axis projection along the z-axis with width 10 Mpc, centered on the gas density maximum
szprj.on_axis("z", center="max", width=(10.0, "Mpc"), nx=400)


# To make an off-axis projection, `szprj.off_axis` is called in the same way, except that the first argument is a three-component normal vector. 
# 
# Currently, only one projection can be in memory at once. These methods
# create images of the projected S-Z signal at each requested frequency,
# which can be accessed dict-like from the projection object (e.g.,
# `szprj["90_GHz"]`). Projections of other quantities may also be
# accessed; to see what fields are available call `szprj.keys()`. The methods also accept standard yt
# keywords for projections such as `center`, `width`, and `source`. The image buffer size can be controlled by setting `nx`.  
# 

### Writing out the S-Z Projections

# You may want to output the S-Z images to figures suitable for
# inclusion in a paper, or save them to disk for later use. There are a
# few methods included for this purpose. For PNG figures with a colorbar
# and axes, use `write_png`:

# In[ ]:

szprj.write_png("SZ_example")


# For simple output of the image data to disk, call `write_hdf5`:

# In[ ]:

szprj.write_hdf5("SZ_example.h5")


# Finally, for output to FITS files which can be opened or analyzed
# using other programs (such as ds9), call `export_fits`.

# In[ ]:

szprj.write_fits("SZ_example.fits", clobber=True)


# which would write all of the projections to a single FITS file,
# including coordinate information in kpc. The optional keyword
# `clobber` allows a previous file to be overwritten. 
# 
