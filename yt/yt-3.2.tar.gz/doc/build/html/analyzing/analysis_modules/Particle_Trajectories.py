
# The `particle_trajectories` analysis module enables the construction of particle trajectories from a time series of datasets for a specified list of particles identified by their unique indices. 

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import yt
import glob
from yt.analysis_modules.particle_trajectories.api import ParticleTrajectories
from yt.config import ytcfg
path = ytcfg.get("yt", "test_data_dir")
import matplotlib.pyplot as plt


# First, let's start off with a FLASH dataset containing only two particles in a mutual circular orbit. We can get the list of filenames this way:

# In[ ]:

my_fns = glob.glob(path+"/Orbit/orbit_hdf5_chk_00[0-9][0-9]")
my_fns.sort()


# And let's define a list of fields that we want to include in the trajectories. The position fields will be included by default, so let's just ask for the velocity fields:

# In[ ]:

fields = ["particle_velocity_x", "particle_velocity_y", "particle_velocity_z"]


# There are only two particles, but for consistency's sake let's grab their indices from the dataset itself:

# In[ ]:

ds = yt.load(my_fns[0])
dd = ds.all_data()
indices = dd["particle_index"].astype("int")
print indices


# which is what we expected them to be. Now we're ready to create a `ParticleTrajectories` object:

# In[ ]:

trajs = ParticleTrajectories(my_fns, indices, fields=fields)


# The `ParticleTrajectories` object `trajs` is essentially a dictionary-like container for the particle fields along the trajectory, and can be accessed as such:

# In[ ]:

print trajs["particle_position_x"]
print trajs["particle_position_x"].shape


# Note that each field is a 2D NumPy array with the different particle indices along the first dimension and the times along the second dimension. As such, we can access them individually by indexing the field:

# In[ ]:

plt.plot(trajs["particle_position_x"][0].ndarray_view(), trajs["particle_position_y"][0].ndarray_view())
plt.plot(trajs["particle_position_x"][1].ndarray_view(), trajs["particle_position_y"][1].ndarray_view())


# And we can plot the velocity fields as well:

# In[ ]:

plt.plot(trajs["particle_velocity_x"][0].ndarray_view(), trajs["particle_velocity_y"][0].ndarray_view())
plt.plot(trajs["particle_velocity_x"][1].ndarray_view(), trajs["particle_velocity_y"][1].ndarray_view())


# If we want to access the time along the trajectory, we use the key `"particle_time"`:

# In[ ]:

plt.plot(trajs["particle_time"].ndarray_view(), trajs["particle_velocity_x"][1].ndarray_view())
plt.plot(trajs["particle_time"].ndarray_view(), trajs["particle_velocity_y"][1].ndarray_view())


# Alternatively, if we know the particle index we'd like to examine, we can get an individual trajectory corresponding to that index:

# In[ ]:

particle1 = trajs.trajectory_from_index(1)
plt.plot(particle1["particle_time"].ndarray_view(), particle1["particle_position_x"].ndarray_view())
plt.plot(particle1["particle_time"].ndarray_view(), particle1["particle_position_y"].ndarray_view())


# Now let's look at a more complicated (and fun!) example. We'll use an Enzo cosmology dataset. First, we'll find the maximum density in the domain, and obtain the indices of the particles within some radius of the center. First, let's have a look at what we're getting:

# In[ ]:

ds = yt.load("enzo_tiny_cosmology/DD0046/DD0046")
slc = yt.SlicePlot(ds, "x", ["density","dark_matter_density"], center="max", width=(3.0, "Mpc"))
slc.show()


# So far, so good--it looks like we've centered on a galaxy cluster. Let's grab all of the dark matter particles within a sphere of 0.5 Mpc (identified by `"particle_type == 1"`):

# In[ ]:

sp = ds.sphere("max", (0.5, "Mpc"))
indices = sp["particle_index"][sp["particle_type"] == 1]


# Next we'll get the list of datasets we want, and create trajectories for these particles:

# In[ ]:

my_fns = glob.glob(path+"/enzo_tiny_cosmology/DD*/*.hierarchy")
my_fns.sort()
trajs = ParticleTrajectories(my_fns, indices)


# Matplotlib can make 3D plots, so let's pick three particle trajectories at random and look at them in the volume:

# In[ ]:

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(8.0, 8.0))
ax = fig.add_subplot(111, projection='3d')
ax.plot(trajs["particle_position_x"][100].ndarray_view(), trajs["particle_position_z"][100].ndarray_view(), 
        trajs["particle_position_z"][100].ndarray_view())
ax.plot(trajs["particle_position_x"][8].ndarray_view(), trajs["particle_position_z"][8].ndarray_view(), 
        trajs["particle_position_z"][8].ndarray_view())
ax.plot(trajs["particle_position_x"][25].ndarray_view(), trajs["particle_position_z"][25].ndarray_view(), 
        trajs["particle_position_z"][25].ndarray_view())


# It looks like these three different particles fell into the cluster along different filaments. We can also look at their x-positions only as a function of time:

# In[ ]:

plt.plot(trajs["particle_time"].ndarray_view(), trajs["particle_position_x"][100].ndarray_view())
plt.plot(trajs["particle_time"].ndarray_view(), trajs["particle_position_x"][8].ndarray_view())
plt.plot(trajs["particle_time"].ndarray_view(), trajs["particle_position_x"][25].ndarray_view())


# Suppose we wanted to know the gas density along the particle trajectory, but there wasn't a particle field corresponding to that in our dataset. Never fear! If the field exists as a grid field, yt will interpolate this field to the particle positions and add the interpolated field to the trajectory. To add such a field (or any field, including additional particle fields) we can call the `add_fields` method:

# In[ ]:

trajs.add_fields(["density"])


# We also could have included `"density"` in our original field list. Now, plot up the gas density for each particle as a function of time:

# In[ ]:

plt.plot(trajs["particle_time"].ndarray_view(), trajs["density"][100].ndarray_view())
plt.plot(trajs["particle_time"].ndarray_view(), trajs["density"][8].ndarray_view())
plt.plot(trajs["particle_time"].ndarray_view(), trajs["density"][25].ndarray_view())
plt.yscale("log")


# Finally, the particle trajectories can be written to disk. Two options are provided: ASCII text files with a column for each field and the time, and HDF5 files:

# In[ ]:

trajs.write_out("halo_trajectories") # This will write a separate file for each trajectory
trajs.write_out_h5("halo_trajectories.h5") # This will write all trajectories to a single file

