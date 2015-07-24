
## Full Halo Analysis

#### Creating a Catalog

# Here we put everything together to perform some realistic analysis. First we load a full simulation dataset.

# In[ ]:

import yt
from yt.analysis_modules.halo_analysis.api import *
import tempfile
import shutil
import os

# Create temporary directory for storing files
tmpdir = tempfile.mkdtemp()

# Load the data set with the full simulation information
data_ds = yt.load('Enzo_64/RD0006/RedshiftOutput0006')


# Now we load a rockstar halos binary file. This is the output from running the rockstar halo finder on the dataset loaded above. It is also possible to require the HaloCatalog to find the halos in the full simulation dataset at runtime by specifying a `finder_method` keyword.

# In[ ]:

# Load the rockstar data files
halos_ds = yt.load('rockstar_halos/halos_0.0.bin')


# From these two loaded datasets we create a halo catalog object. No analysis is done at this point, we are simply defining an object we can add analysis tasks to. These analysis tasks will be run in the order they are added to the halo catalog object.

# In[ ]:

# Instantiate a catalog using those two paramter files
hc = HaloCatalog(data_ds=data_ds, halos_ds=halos_ds, 
                 output_dir=os.path.join(tmpdir, 'halo_catalog'))


# The first analysis task we add is a filter for the most massive halos; those with masses great than $10^{14}~M_\odot$. Note that all following analysis will only be performed on these massive halos and we will not waste computational time calculating quantities for halos we are not interested in. This is a result of adding this filter first. If we had called `add_filter` after some other `add_quantity` or `add_callback` to the halo catalog, the quantity and callback calculations would have been performed for all halos, not just those which pass the filter.

# In[ ]:

# Filter out less massive halos
hc.add_filter("quantity_value", "particle_mass", ">", 1e14, "Msun")


#### Finding Radial Profiles

# Our first analysis goal is going to be constructing radial profiles for our halos. We would like these profiles to be in terms of the virial radius. Unfortunately we have no guarantee that values of center and virial radius recorded by the halo finder are actually physical. Therefore we should recalculate these quantities ourselves using the values recorded by the halo finder as a starting point.

# The first step is going to be creating a sphere object that we will create radial profiles along. This attaches a sphere data object to every halo left in the catalog.

# In[ ]:

# attach a sphere object to each halo whose radius extends to twice the radius of the halo
hc.add_callback("sphere", factor=2.0)


# Next we find the radial profile of the gas overdensity along the sphere object in order to find the virial radius. `radius` is the axis along which we make bins for the radial profiles. `[("gas","overdensity")]` is the quantity that we are profiling. This is a list so we can profile as many quantities as we want. The `weight_field` indicates how the cells should be weighted, but note that this is not a list, so all quantities will be weighted in the same way. The `accumulation` keyword indicates if the profile should be cummulative; this is useful for calculating profiles such as enclosed mass. The `storage` keyword indicates the name of the attribute of a halo where these profiles will be stored. Setting the storage keyword to "virial_quantities_profiles" means that the profiles will be stored in a dictionary that can be accessed by `halo.virial_quantities_profiles`.

# In[ ]:

# use the sphere to calculate radial profiles of gas density weighted by cell volume in terms of the virial radius
hc.add_callback("profile", x_field="radius",
                y_fields=[("gas", "overdensity")],
                weight_field="cell_volume", 
                accumulation=False,
                storage="virial_quantities_profiles")


# Now we calculate the virial radius of halo using the sphere object. As this is a callback, not a quantity, the virial radius will not be written out with the rest of the halo properties in the final halo catalog. This also has a `profile_storage` keyword to specify where the radial profiles are stored that will allow the callback to calculate the relevant virial quantities. We supply this keyword with the same string we gave to `storage` in the last `profile` callback.

# In[ ]:

# Define a virial radius for the halo.
hc.add_callback("virial_quantities", ["radius"], 
                profile_storage = "virial_quantities_profiles")


# Now that we have calculated the virial radius, we delete the profiles we used to find it.

# In[ ]:

hc.add_callback('delete_attribute','virial_quantities_profiles')


# Now that we have calculated virial quantities we can add a new sphere that is aware of the virial radius we calculated above.

# In[ ]:

hc.add_callback('sphere', radius_field='radius_200', factor=5,
                field_parameters=dict(virial_radius=('quantity', 'radius_200')))


# Using this new sphere, we calculate a gas temperature profile along the virial radius, weighted by the cell mass.

# In[ ]:

hc.add_callback('profile', 'virial_radius', [('gas','temperature')],
                storage='virial_profiles',
                weight_field='cell_mass', 
                accumulation=False, output_dir='profiles')


# As profiles are not quantities they will not automatically be written out in the halo catalog; thus in order to be reloadable we must write them out explicitly through a callback of `save_profiles`. This makes sense because they have an extra dimension for each halo along the profile axis. 

# In[ ]:

# Save the profiles
hc.add_callback("save_profiles", storage="virial_profiles", output_dir="profiles")


# We then create the halo catalog. Remember, no analysis is done before this call to create. By adding callbacks and filters we are simply queuing up the actions we want to take that will all run now.

# In[ ]:

hc.create()


#### Reloading HaloCatalogs

# Finally we load these profiles back in and make a pretty plot. It is not strictly necessary to reload the profiles in this notebook, but we show this process here to illustrate that this step may be performed completely separately from the rest of the script. This workflow allows you to create a single script that will allow you to perform all of the analysis that requires the full dataset. The output can then be saved in a compact form where only the necessarily halo quantities are stored. You can then download this smaller dataset to a local computer and run any further non-computationally intense analysis and design the appropriate plots.

# We can load a previously saved halo catalog by using the `load` command. We then create a `HaloCatalog` object from just this dataset.

# In[ ]:

halos_ds =  yt.load(os.path.join(tmpdir, 'halo_catalog/halo_catalog.0.h5'))

hc_reloaded = HaloCatalog(halos_ds=halos_ds,
                          output_dir=os.path.join(tmpdir, 'halo_catalog'))


#  Just as profiles are saved seperately throught the `save_profiles` callback they also must be loaded separately using the `load_profiles` callback.

# In[ ]:

hc_reloaded.add_callback('load_profiles', storage='virial_profiles',
                         output_dir='profiles')


# Calling `load` is the equivalent of calling `create` earlier, but defaults to to not saving new information. This means that the callback to `load_profiles` is not run until we call `load` here.

# In[ ]:

hc_reloaded.load()


#### Plotting Radial Profiles

# In the future ProfilePlot will be able to properly interpret the loaded profiles of `Halo` and `HaloCatalog` objects, but this functionality is not yet implemented. In the meantime, we show a quick method of viewing a profile for a single halo.

# The individual `Halo` objects contained in the `HaloCatalog` can be accessed through the `halo_list` attribute. This gives us access to the dictionary attached to each halo where we stored the radial profiles.

# In[ ]:

halo = hc_reloaded.halo_list[0]

radius = halo.virial_profiles['virial_radius']
temperature = halo.virial_profiles[u"('gas', 'temperature')"]

# Remove output files, that are no longer needed
shutil.rmtree(tmpdir)


# Here we quickly use matplotlib to create a basic plot of the radial profile of this halo. When `ProfilePlot` is properly configured to accept Halos and HaloCatalogs the full range of yt plotting tools will be accessible.

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import numpy as np

plt.plot(np.array(radius), np.array(temperature))

plt.semilogy()
plt.xlabel(r'$\rm{R/R_{vir}}$')
plt.ylabel(r'$\rm{Temperature\/\/(K)}$')

plt.show()

