
# Even if your data is not strictly related to fields commonly used in
# astrophysical codes or your code is not supported yet, you can still feed it to
# yt to use its advanced visualization and analysis facilities. The only
# requirement is that your data can be represented as three-dimensional NumPy arrays with a consistent grid structure. What follows are some common examples of loading in generic array data that you may find useful. 

### Generic Unigrid Data

# The simplest case is that of a single grid of data spanning the domain, with one or more fields. The data could be generated from a variety of sources; we'll just give three common examples:

#### Data generated "on-the-fly"

# The most common example is that of data that is generated in memory from the currently running script or notebook. 

# In[ ]:

import yt
import numpy as np


# In this example, we'll just create a 3-D array of random floating-point data using NumPy:

# In[ ]:

arr = np.random.random(size=(64,64,64))


# To load this data into yt, we need associate it with a field. The `data` dictionary consists of one or more fields, each consisting of a tuple of a NumPy array and a unit string. Then, we can call `load_uniform_grid`:

# In[ ]:

data = dict(density = (arr, "g/cm**3"))
bbox = np.array([[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5]])
ds = yt.load_uniform_grid(data, arr.shape, length_unit="Mpc", bbox=bbox, nprocs=64)


# `load_uniform_grid` takes the following arguments and optional keywords:
# 
# * `data` : This is a dict of numpy arrays, where the keys are the field names
# * `domain_dimensions` : The domain dimensions of the unigrid
# * `length_unit` : The unit that corresponds to `code_length`, can be a string, tuple, or floating-point number
# * `bbox` : Size of computational domain in units of `code_length`
# * `nprocs` : If greater than 1, will create this number of subarrays out of data
# * `sim_time` : The simulation time in seconds
# * `mass_unit` : The unit that corresponds to `code_mass`, can be a string, tuple, or floating-point number
# * `time_unit` : The unit that corresponds to `code_time`, can be a string, tuple, or floating-point number
# * `velocity_unit` : The unit that corresponds to `code_velocity`
# * `magnetic_unit` : The unit that corresponds to `code_magnetic`, i.e. the internal units used to represent magnetic field strengths.
# * `periodicity` : A tuple of booleans that determines whether the data will be treated as periodic along each axis
# 
# This example creates a yt-native dataset `ds` that will treat your array as a
# density field in cubic domain of 3 Mpc edge size and simultaneously divide the 
# domain into `nprocs` = 64 chunks, so that you can take advantage
# of the underlying parallelism. 
# 
# The optional unit keyword arguments allow for the default units of the dataset to be set. They can be:
# * A string, e.g. `length_unit="Mpc"`
# * A tuple, e.g. `mass_unit=(1.0e14, "Msun")`
# * A floating-point value, e.g. `time_unit=3.1557e13`
# 
# In the latter case, the unit is assumed to be cgs. 
# 
# The resulting `ds` functions exactly like a dataset like any other yt can handle--it can be sliced, and we can show the grid boundaries:

# In[ ]:

slc = yt.SlicePlot(ds, "z", ["density"])
slc.set_cmap("density", "Blues")
slc.annotate_grids(cmap=None)
slc.show()


# Particle fields are detected as one-dimensional fields. The number of
# particles is set by the `number_of_particles` key in
# `data`. Particle fields are then added as one-dimensional arrays in
# a similar manner as the three-dimensional grid fields:

# In[ ]:

posx_arr = np.random.uniform(low=-1.5, high=1.5, size=10000)
posy_arr = np.random.uniform(low=-1.5, high=1.5, size=10000)
posz_arr = np.random.uniform(low=-1.5, high=1.5, size=10000)
data = dict(density = (np.random.random(size=(64,64,64)), "Msun/kpc**3"), 
            number_of_particles = 10000,
            particle_position_x = (posx_arr, 'code_length'), 
            particle_position_y = (posy_arr, 'code_length'),
            particle_position_z = (posz_arr, 'code_length'))
bbox = np.array([[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5]])
ds = yt.load_uniform_grid(data, data["density"][0].shape, length_unit=(1.0, "Mpc"), mass_unit=(1.0,"Msun"), 
                       bbox=bbox, nprocs=4)


# In this example only the particle position fields have been assigned. `number_of_particles` must be the same size as the particle
# arrays. If no particle arrays are supplied then `number_of_particles` is assumed to be zero. Take a slice, and overlay particle positions:

# In[ ]:

slc = yt.SlicePlot(ds, "z", ["density"])
slc.set_cmap("density", "Blues")
slc.annotate_particles(0.25, p_size=12.0, col="Red")
slc.show()


#### HDF5 data

# HDF5 is a convenient format to store data. If you have unigrid data stored in an HDF5 file, it is possible to load it into memory and then use `load_uniform_grid` to get it into yt:

# In[ ]:

import h5py
from yt.config import ytcfg
data_dir = ytcfg.get('yt','test_data_dir')
from yt.utilities.physical_ratios import cm_per_kpc
f = h5py.File(data_dir+"/UnigridData/turb_vels.h5", "r") # Read-only access to the file


# The HDF5 file handle's keys correspond to the datasets stored in the file:

# In[ ]:

print f.keys()


# We need to add some unit information. It may be stored in the file somewhere, or we may know it from another source. In this case, the units are simply cgs:

# In[ ]:

units = ["gauss","gauss","gauss", "g/cm**3", "erg/cm**3", "K", 
         "cm/s", "cm/s", "cm/s", "cm/s", "cm/s", "cm/s"]


# We can iterate over the items in the file handle and the units to get the data into a dictionary, which we will then load:

# In[ ]:

data = {k:(v.value,u) for (k,v), u in zip(f.items(),units)}
bbox = np.array([[-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5]])


# In[ ]:

ds = yt.load_uniform_grid(data, data["Density"][0].shape, length_unit=250.*cm_per_kpc, bbox=bbox, nprocs=8, 
                       periodicity=(False,False,False))


# In this case, the data came from a simulation which was 250 kpc on a side. An example projection of two fields:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["z-velocity","Temperature","Bx"], weight_field="Density")
prj.set_log("z-velocity", False)
prj.set_log("Bx", False)
prj.show()


#### Volume Rendering Loaded Data

# Volume rendering requires defining a `TransferFunction` to map data to color and opacity and a `camera` to create a viewport and render the image.

# In[ ]:

#Find the min and max of the field
mi, ma = ds.all_data().quantities.extrema('Temperature')
#Reduce the dynamic range
mi = mi.value + 1.5e7
ma = ma.value - 0.81e7


# Create a Transfer Function that goes from the minimum to the maximum of the data:

# In[ ]:

tf = yt.ColorTransferFunction((mi, ma), grey_opacity=False)


# Define the properties and size of the `camera` viewport:

# In[ ]:

# Choose a vector representing the viewing direction.
L = [0.5, 0.5, 0.5]
# Define the center of the camera to be the domain center
c = ds.domain_center[0]
# Define the width of the image
W = 1.5*ds.domain_width[0]
# Define the number of pixels to render
Npixels = 512 


# Create a `camera` object and 

# In[ ]:

cam = ds.camera(c, L, W, Npixels, tf, fields=['Temperature'],
                north_vector=[0,0,1], steady_north=True, 
                sub_samples=5, log_fields=[False])

cam.transfer_function.map_to_colormap(mi,ma, 
                                      scale=15.0, colormap='algae')


# In[ ]:

cam.show()


#### FITS image data

# The FITS file format is a common astronomical format for 2-D images, but it can store three-dimensional data as well. The [AstroPy](http://www.astropy.org) project has modules for FITS reading and writing, which were incorporated from the [PyFITS](http://www.stsci.edu/institute/software_hardware/pyfits) library.

# In[ ]:

import astropy.io.fits as pyfits
# Or, just import pyfits if that's what you have installed


# Using `pyfits` we can open a FITS file. If we call `info()` on the file handle, we can figure out some information about the file's contents. The file in this example has a primary HDU (header-data-unit) with no data, and three HDUs with 3-D data. In this case, the data consists of three velocity fields:

# In[ ]:

f = pyfits.open(data_dir+"/UnigridData/velocity_field_20.fits")
f.info()


# We can put it into a dictionary in the same way as before, but we slice the file handle `f` so that we don't use the `PrimaryHDU`. `hdu.name` is the field name and `hdu.data` is the actual data. Each of these velocity fields is in km/s. We can check that we got the correct fields. 

# In[ ]:

data = {}
for hdu in f:
    name = hdu.name.lower()
    data[name] = (hdu.data,"km/s")
print data.keys()


# The velocity field names in this case are slightly different than the standard yt field names for velocity fields, so we will reassign the field names:

# In[ ]:

data["velocity_x"] = data.pop("x-velocity")
data["velocity_y"] = data.pop("y-velocity")
data["velocity_z"] = data.pop("z-velocity")


# Now we load the data into yt. Let's assume that the box size is a Mpc. Since these are velocity fields, we can overlay velocity vectors on slices, just as if we had loaded in data from a supported code. 

# In[ ]:

ds = yt.load_uniform_grid(data, data["velocity_x"][0].shape, length_unit=(1.0,"Mpc"))
slc = yt.SlicePlot(ds, "x", ["velocity_x","velocity_y","velocity_z"])
for ax in "xyz":
    slc.set_log("velocity_%s" % (ax), False)
slc.annotate_velocity()
slc.show()


### Generic AMR Data

# In a similar fashion to unigrid data, data gridded into rectangular patches at varying levels of resolution may also be loaded into yt. In this case, a list of grid dictionaries should be provided, with the requisite information about each grid's properties. This example sets up two grids: a top-level grid (`level == 0`) covering the entire domain and a subgrid at `level == 1`. 

# In[ ]:

grid_data = [
    dict(left_edge = [0.0, 0.0, 0.0],
         right_edge = [1.0, 1.0, 1.0],
         level = 0,
         dimensions = [32, 32, 32]), 
    dict(left_edge = [0.25, 0.25, 0.25],
         right_edge = [0.75, 0.75, 0.75],
         level = 1,
         dimensions = [32, 32, 32])
   ]


# We'll just fill each grid with random density data, with a scaling with the grid refinement level.

# In[ ]:

for g in grid_data: g["density"] = np.random.random(g["dimensions"]) * 2**g["level"]


# Particle fields are supported by adding 1-dimensional arrays to each `grid` and
# setting the `number_of_particles` key in each `grid`'s dict. If a grid has no particles, set `number_of_particles = 0`, but the particle fields still have to be defined since they are defined elsewhere; set them to empty NumPy arrays:

# In[ ]:

grid_data[0]["number_of_particles"] = 0 # Set no particles in the top-level grid
grid_data[0]["particle_position_x"] = np.array([]) # No particles, so set empty arrays
grid_data[0]["particle_position_y"] = np.array([])
grid_data[0]["particle_position_z"] = np.array([])
grid_data[1]["number_of_particles"] = 1000
grid_data[1]["particle_position_x"] = np.random.uniform(low=0.25, high=0.75, size=1000)
grid_data[1]["particle_position_y"] = np.random.uniform(low=0.25, high=0.75, size=1000)
grid_data[1]["particle_position_z"] = np.random.uniform(low=0.25, high=0.75, size=1000)


# We need to specify the field units in a `field_units` dict:

# In[ ]:

field_units = {"density":"code_mass/code_length**3",
               "particle_position_x":"code_length",
               "particle_position_y":"code_length",
               "particle_position_z":"code_length",}


# Then, call `load_amr_grids`:

# In[ ]:

ds = yt.load_amr_grids(grid_data, [32, 32, 32], field_units=field_units)


# `load_amr_grids` also takes the same keywords `bbox` and `sim_time` as `load_uniform_grid`. We could have also specified the length, time, velocity, and mass units in the same manner as before. Let's take a slice:

# In[ ]:

slc = yt.SlicePlot(ds, "z", ["density"])
slc.annotate_particles(0.25, p_size=15.0, col="Pink")
slc.show()


### Caveats for Loading Generic Array Data

# * Units will be incorrect unless the data has already been converted to cgs.
# * Particles may be difficult to integrate.
# * Data must already reside in memory before loading it in to yt, whether it is generated at runtime or loaded from disk. 
# * Some functions may behave oddly, and parallelism will be disappointing or non-existent in most cases.
# * No consistency checks are performed on the hierarchy
# * Consistency between particle positions and grids is not checked; `load_amr_grids` assumes that particle positions associated with one grid are not bounded within another grid at a higher level, so this must be ensured by the user prior to loading the grid data. 
