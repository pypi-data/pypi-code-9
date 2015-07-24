
# This example creates a fake in-memory particle dataset and then loads it as a yt dataset using the `load_particles` function.
# 
# Our "fake" dataset will be numpy arrays filled with normally distributed randoml particle positions and uniform particle masses.  Since real data is often scaled, I arbitrarily multiply by 1e6 to show how to deal with scaled data.

# In[ ]:

import numpy as np

n_particles = 5e6

ppx, ppy, ppz = 1e6*np.random.normal(size=[3, n_particles])

ppm = np.ones(n_particles)


# The `load_particles` function accepts a dictionary populated with particle data fields loaded in memory as numpy arrays or python lists:

# In[ ]:

data = {'particle_position_x': ppx,
        'particle_position_y': ppy,
        'particle_position_z': ppz,
        'particle_mass': ppm}


# To hook up with yt's internal field system, the dictionary keys must be 'particle_position_x', 'particle_position_y', 'particle_position_z', and 'particle_mass', as well as any other particle field provided by one of the particle frontends.

# The `load_particles` function transforms the `data` dictionary into an in-memory yt `Dataset` object, providing an interface for further analysis with yt. The example below illustrates how to load the data dictionary we created above.

# In[ ]:

import yt
from yt.units import parsec, Msun

bbox = 1.1*np.array([[min(ppx), max(ppx)], [min(ppy), max(ppy)], [min(ppy), max(ppy)]])

ds = yt.load_particles(data, length_unit=parsec, mass_unit=1e8*Msun, n_ref=256, bbox=bbox)


# The `length_unit` and `mass_unit` are the conversion from the units used in the `data` dictionary to CGS.  I've arbitrarily chosen one parsec and 10^8 Msun for this example. 
# 
# The `n_ref` parameter controls how many particle it takes to accumulate in an oct-tree cell to trigger refinement.  Larger `n_ref` will decrease poisson noise at the cost of resolution in the octree.  
# 
# Finally, the `bbox` parameter is a bounding box in the units of the dataset that contains all of the particles.  This is used to set the size of the base octree block.

# This new dataset acts like any other yt `Dataset` object, and can be used to create data objects and query for yt fields.  This example shows how to access "deposit" fields:

# In[ ]:

ad = ds.all_data()

# This is generated with "cloud-in-cell" interpolation.
cic_density = ad["deposit", "all_cic"]

# These three are based on nearest-neighbor cell deposition
nn_density = ad["deposit", "all_density"]
nn_deposited_mass = ad["deposit", "all_mass"]
particle_count_per_cell = ad["deposit", "all_count"]


# In[ ]:

ds.field_list


# In[ ]:

ds.derived_field_list


# In[ ]:

slc = yt.SlicePlot(ds, 2, ('deposit', 'all_cic'))
slc.set_width((8, 'Mpc'))

