
# In[ ]:

get_ipython().magic(u'matplotlib inline')
import yt
import numpy as np


# This notebook shows how to use yt to make plots and examine FITS X-ray images and events files. 

### Sloshing, Shocks, and Bubbles in Abell 2052

# This example uses data provided by [Scott Randall](http://hea-www.cfa.harvard.edu/~srandall/), presented originally in [Blanton, E.L., Randall, S.W., Clarke, T.E., et al. 2011, ApJ, 737, 99](http://adsabs.harvard.edu/cgi-bin/bib_query?2011ApJ...737...99B). They consist of two files, a "flux map" in counts/s/pixel between 0.3 and 2 keV, and a spectroscopic temperature map in keV. 

# In[ ]:

ds = yt.load("xray_fits/A2052_merged_0.3-2_match-core_tmap_bgecorr.fits", 
             auxiliary_files=["xray_fits/A2052_core_tmap_b1_m2000_.fits"])


# Since the flux and projected temperature images are in two different files, we had to use one of them (in this case the "flux" file) as a master file, and pass in the "temperature" file with the `auxiliary_files` keyword to `load`. 

# Next, let's derive some new fields for the number of counts, the "pseudo-pressure", and the "pseudo-entropy":

# In[ ]:

def _counts(field, data):
    exposure_time = data.get_field_parameter("exposure_time")
    return data["flux"]*data["pixel"]*exposure_time
ds.add_field(name="counts", function=_counts, units="counts", take_log=False)

def _pp(field, data):
    return np.sqrt(data["counts"])*data["projected_temperature"]
ds.add_field(name="pseudo_pressure", function=_pp, units="sqrt(counts)*keV", take_log=False)

def _pe(field, data):
    return data["projected_temperature"]*data["counts"]**(-1./3.)
ds.add_field(name="pseudo_entropy", function=_pe, units="keV*(counts)**(-1/3)", take_log=False)


# Here, we're deriving a "counts" field from the "flux" field by passing it a `field_parameter` for the exposure time of the time and multiplying by the pixel scale. Second, we use the fact that the surface brightness is strongly dependent on density ($S_X \propto \rho^2$) to use the counts in each pixel as a "stand-in". Next, we'll grab the exposure time from the primary FITS header of the flux file and create a `YTQuantity` from it, to be used as a `field_parameter`:

# In[ ]:

exposure_time = ds.quan(ds.primary_header["exposure"], "s")


# Now, we can make the `SlicePlot` object of the fields we want, passing in the `exposure_time` as a `field_parameter`. We'll also set the width of the image to 250 pixels.

# In[ ]:

slc = yt.SlicePlot(ds, "z", 
                   ["flux","projected_temperature","pseudo_pressure","pseudo_entropy"], 
                   origin="native", field_parameters={"exposure_time":exposure_time})
slc.set_log("flux",True)
slc.set_log("pseudo_pressure",False)
slc.set_log("pseudo_entropy",False)
slc.set_width(250.)
slc.show()


# To add the celestial coordinates to the image, we can use `PlotWindowWCS`, if you have the [WCSAxes](http://wcsaxes.readthedocs.org/en/latest/) package installed:

# In[ ]:

from yt.frontends.fits.misc import PlotWindowWCS
wcs_slc = PlotWindowWCS(slc)
wcs_slc.show()


# We can make use of yt's facilities for profile plotting as well.

# In[ ]:

v, c = ds.find_max("flux") # Find the maxmimum flux and its center
my_sphere = ds.sphere(c, (100.,"code_length")) # Radius of 150 pixels
my_sphere.set_field_parameter("exposure_time", exposure_time)


# Such as a radial profile plot:

# In[ ]:

radial_profile = yt.ProfilePlot(my_sphere, "radius", 
                                ["counts","pseudo_pressure","pseudo_entropy"], 
                                n_bins=50, weight_field="ones")
radial_profile.set_log("counts", True)
radial_profile.set_log("pseudo_pressure", True)
radial_profile.set_log("pseudo_entropy", True)
radial_profile.show()


# Or a phase plot:

# In[ ]:

phase_plot = yt.PhasePlot(my_sphere, "pseudo_pressure", "pseudo_entropy", ["counts"], weight_field=None)
phase_plot.show()


# Finally, we can also take an existing [ds9](http://ds9.si.edu/site/Home.html) region and use it to create a "cut region", using `ds9_region` (the [pyregion](http://leejjoon.github.io/pyregion/) package needs to be installed for this):

# In[ ]:

from yt.frontends.fits.misc import ds9_region
reg_file = ["# Region file format: DS9 version 4.1\n",
            "global color=green dashlist=8 3 width=3 include=1 source=1 fk5\n",
            "circle(15:16:44.817,+7:01:19.62,34.6256\")"]
f = open("circle.reg","w")
f.writelines(reg_file)
f.close()
circle_reg = ds9_region(ds, "circle.reg", field_parameters={"exposure_time":exposure_time})


# This region may now be used to compute derived quantities:

# In[ ]:

print circle_reg.quantities.weighted_average_quantity("projected_temperature", "counts")


# Or used in projections:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", 
                   ["flux","projected_temperature","pseudo_pressure","pseudo_entropy"], 
                   origin="native", field_parameters={"exposure_time":exposure_time},
                   data_source=circle_reg,
                   proj_style="sum")
prj.set_log("flux",True)
prj.set_log("pseudo_pressure",False)
prj.set_log("pseudo_entropy",False)
prj.set_width(250.)
prj.show()


### The Bullet Cluster

# This example uses an events table file from a ~100 ks exposure of the "Bullet Cluster" from the [Chandra Data Archive](http://cxc.harvard.edu/cda/). In this case, the individual photon events are treated as particle fields in yt. However, you can make images of the object in different energy bands using the `setup_counts_fields` function. 

# In[ ]:

from yt.frontends.fits.api import setup_counts_fields


# `load` will handle the events file as FITS image files, and will set up a grid using the WCS information in the file. Optionally, the events may be reblocked to a new resolution. by setting the `"reblock"` parameter in the `parameters` dictionary in `load`. `"reblock"` must be a power of 2. 

# In[ ]:

ds2 = yt.load("xray_fits/acisf05356N003_evt2.fits.gz", parameters={"reblock":2})


# `setup_counts_fields` will take a list of energy bounds (emin, emax) in keV and create a new field from each where the photons in that energy range will be deposited onto the image grid. 

# In[ ]:

ebounds = [(0.1,2.0),(2.0,5.0)]
setup_counts_fields(ds2, ebounds)


# The "x", "y", "energy", and "time" fields in the events table are loaded as particle fields. Each one has a name given by "event\_" plus the name of the field:

# In[ ]:

dd = ds2.all_data()
print dd["event_x"]
print dd["event_y"]


# Now, we'll make a plot of the two counts fields we made, and pan and zoom to the bullet:

# In[ ]:

slc = yt.SlicePlot(ds2, "z", ["counts_0.1-2.0","counts_2.0-5.0"], origin="native")
slc.pan((100.,100.))
slc.set_width(500.)
slc.show()


# The counts fields can take the field parameter `"sigma"` and use [AstroPy's convolution routines](http://astropy.readthedocs.org/en/latest/convolution/) to smooth the data with a Gaussian:

# In[ ]:

slc = yt.SlicePlot(ds2, "z", ["counts_0.1-2.0","counts_2.0-5.0"], origin="native",
                   field_parameters={"sigma":2.}) # This value is in pixel scale
slc.pan((100.,100.))
slc.set_width(500.)
slc.set_zlim("counts_0.1-2.0", 0.01, 100.)
slc.set_zlim("counts_2.0-5.0", 0.01, 50.)
slc.show()

