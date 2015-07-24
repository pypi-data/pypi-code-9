
# yt has capabilities for writing 2D and 3D uniformly gridded data generated from datasets to FITS files. This is via the `FITSImageBuffer` class, which has subclasses `FITSSlice` and `FITSProjection` to write slices and projections directly to FITS. We'll test this out on an Athena dataset.

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import yt
from yt.utilities.fits_image import FITSImageBuffer, FITSSlice, FITSProjection


# In[ ]:

ds = yt.load("MHDSloshing/virgo_low_res.0054.vtk", parameters={"length_unit":(1.0,"Mpc"),
                                                               "mass_unit":(1.0e14,"Msun"),
                                                               "time_unit":(1.0,"Myr")})


# To demonstrate a useful example of creating a FITS file, let's first make a `ProjectionPlot`:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["temperature"], weight_field="density", width=(500.,"kpc"))
prj.show()


# Suppose that we wanted to write this projection to a FITS file for analysis and visualization in other programs, such as ds9. We can do that using `FITSProjection`:

# In[ ]:

prj_fits = FITSProjection(ds, "z", ["temperature"], weight_field="density")


# which took the same parameters as `ProjectionPlot` except the width, because `FITSProjection` and `FITSSlice` always make slices and projections of the width of the domain size, at the finest resolution available in the simulation, in a unit determined to be appropriate for the physical size of the dataset. `prj_fits` is a full-fledged FITS file in memory, specifically an [AstroPy `HDUList`](http://astropy.readthedocs.org/en/latest/io/fits/api/hdulists.html) object. This means that we can use all of the methods inherited from `HDUList`:

# In[ ]:

prj_fits.info()


# `info` shows us the contents of the virtual FITS file. We can also look at the header for the `"temperature"` image, like so:

# In[ ]:

prj_fits["temperature"].header


# where we can see that the temperature units are in Kelvin and the cell widths are in kiloparsecs. The projection can be written to disk using the `writeto` method:

# In[ ]:

prj_fits.writeto("sloshing.fits", clobber=True)


# Since yt can read FITS image files, it can be loaded up just like any other dataset:

# In[ ]:

ds2 = yt.load("sloshing.fits")


# and we can make a `SlicePlot` of the 2D image, which shows the same data as the previous image:

# In[ ]:

slc2 = yt.SlicePlot(ds2, "z", ["temperature"], width=(500.,"kpc"))
slc2.set_log("temperature", True)
slc2.show()


# If you want more fine-grained control over what goes into the FITS file, you can call `FITSImageBuffer` directly, with various kinds of inputs. For example, you could use a `FixedResolutionBuffer`, and specify you want the units in parsecs instead:

# In[ ]:

slc3 = ds.slice(0, 0.0)
frb = slc3.to_frb((500.,"kpc"), 800)
fib = FITSImageBuffer(frb, fields=["density","temperature"], units="pc")


# Finally, a 3D FITS cube can be created from a covering grid:

# In[ ]:

cvg = ds.covering_grid(ds.index.max_level, [-0.5,-0.5,-0.5], [64, 64, 64], fields=["density","temperature"])
fib = FITSImageBuffer(cvg, fields=["density","temperature"], units="Mpc")

