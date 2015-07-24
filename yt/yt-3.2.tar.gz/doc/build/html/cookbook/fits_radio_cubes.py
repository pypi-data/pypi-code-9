
# In[ ]:

get_ipython().magic(u'matplotlib inline')
import yt


# This notebook demonstrates some of the capabilties of yt on some FITS "position-position-spectrum" cubes of radio data. 

### M33 VLA Image

# The dataset `"m33_hi.fits"` has `NaN`s in it, so we'll mask them out by setting `nan_mask` = 0:

# In[ ]:

ds = yt.load("radio_fits/m33_hi.fits", nan_mask=0.0, z_axis_decomp=True)


# First, we'll take a slice of the data along the z-axis, which is the velocity axis of the FITS cube:

# In[ ]:

slc = yt.SlicePlot(ds, "z", ["intensity"], origin="native")
slc.show()


# The x and y axes are in units of the image pixel. When making plots of FITS data, to see the image coordinates as they are in the file, it is helpful to set the keyword `origin = "native"`. If you want to see the celestial coordinates along the axes, you can import the `PlotWindowWCS` class and feed it the `SlicePlot`. For this to work, the [WCSAxes](http://wcsaxes.readthedocs.org/en/latest/) package needs to be installed.

# In[ ]:

from yt.frontends.fits.misc import PlotWindowWCS
PlotWindowWCS(slc)


# Generally, it is best to get the plot in the shape you want it before feeding it to `PlotWindowWCS`. Once it looks the way you want, you can save it just like a normal `PlotWindow` plot:

# In[ ]:

slc.save()


# We can also take slices of this dataset at a few different values along the "z" axis (corresponding to the velocity), so let's try a few. To pick specific velocity values for slices, we will need to use the dataset's `spec2pixel` method to determine which pixels to slice on:

# In[ ]:

import yt.units as u
new_center = ds.domain_center
new_center[2] = ds.spec2pixel(-250000.*u.m/u.s)


# Now we can use this new center to create a new slice:

# In[ ]:

slc = yt.SlicePlot(ds, "z", ["intensity"], center=new_center, origin="native")
slc.show()


# We can do this a few more times for different values of the velocity:

# In[ ]:

new_center[2] = ds.spec2pixel(-100000.*u.m/u.s)
slc = yt.SlicePlot(ds, "z", ["intensity"], center=new_center, origin="native")
slc.show()


# In[ ]:

new_center[2] = ds.spec2pixel(-150000.*u.m/u.s)
slc = yt.SlicePlot(ds, "z", ["intensity"], center=new_center, origin="native")
slc.show()


# These slices demonstrate the intensity of the radio emission at different line-of-sight velocities. 

# We can also make a projection of all the emission along the line of sight. Since we're not doing an integration along a path length, we needed to specify `proj_style = "sum"`:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["intensity"], proj_style="sum", origin="native")
prj.show()


# We can also look at the slices perpendicular to the other axes, which will show us the structure along the velocity axis:

# In[ ]:

slc = yt.SlicePlot(ds, "x", ["intensity"], origin="native", window_size=(8,8))
slc.show()


# In[ ]:

slc = yt.SlicePlot(ds, "y", ["intensity"], origin="native", window_size=(8,8))
slc.show()


# In these cases, we needed to explicitly declare a square `window_size` to get a figure that looks good. 

### $^{13}$CO GRS Data

# This next example uses one of the cubes from the [Boston University Galactic Ring Survey](http://www.bu.edu/galacticring/new_index.htm). 

# In[ ]:

ds = yt.load("radio_fits/grs-50-cube.fits", nan_mask=0.0)


# We can use the `quantities` methods to determine derived quantities of the dataset. For example, we could find the maximum and minimum temperature:

# In[ ]:

dd = ds.all_data() # A region containing the entire dataset
extrema = dd.quantities.extrema("temperature")
print extrema


# We can compute the average temperature along the "velocity" axis for all positions by making a `ProjectionPlot`:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["temperature"], origin="native", 
                        weight_field="ones") # "ones" weights each cell by 1
prj.set_log("temperature", True)
prj.show()


# We can also make a histogram of the temperature field of this region:

# In[ ]:

pplot = yt.ProfilePlot(dd, "temperature", ["ones"], weight_field=None, n_bins=128)
pplot.show()


# We can see from this histogram and our calculation of the dataset's extrema that there is a lot of noise. Suppose we wanted to make a projection, but instead make it only of the cells which had a positive temperature value. We can do this by doing a "field cut" on the data:

# In[ ]:

fc = dd.cut_region(["obj['temperature'] > 0"])


# Now let's check the extents of this region:

# In[ ]:

print fc.quantities.extrema("temperature")


# Looks like we were successful in filtering out the negative temperatures. To compute the average temperature of this new region:

# In[ ]:

fc.quantities.weighted_average_quantity("temperature", "ones")


# Now, let's make a projection of the dataset, using the field cut `fc` as a `data_source`:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["temperature"], data_source=fc, origin="native", 
                        weight_field="ones") # "ones" weights each cell by 1
prj.set_log("temperature", True)
prj.show()


# Finally, we can also take an existing [ds9](http://ds9.si.edu/site/Home.html) region and use it to create a "cut region" as well, using `ds9_region` (the [pyregion](http://leejjoon.github.io/pyregion/) package needs to be installed for this):

# In[ ]:

from yt.frontends.fits.misc import ds9_region


# For this example we'll create a ds9 region from scratch and load it up:

# In[ ]:

region = 'galactic;box(+49:26:35.150,-0:30:04.410,1926.1927",1483.3701",0.0)'
box_reg = ds9_region(ds, region)


# This region may now be used to compute derived quantities:

# In[ ]:

print box_reg.quantities.extrema("temperature")


# Or in projections:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["temperature"], origin="native", 
                        data_source=box_reg, weight_field="ones") # "ones" weights each cell by 1
prj.set_log("temperature", True)
prj.show()

