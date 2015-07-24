
## Using yt to view and analyze Tipsy outputs from Gasoline

### Loading Files

# Alright, let's start with some basics.  Before we do anything, we will need to load a snapshot.  You can do this using the ```load``` convenience function.  yt will autodetect that you have a tipsy snapshot, and automatically set itself up appropriately.

# In[ ]:

import yt


# We will be looking at a fairly low resolution dataset.  In the next cell, the `ds` object has an atribute called `n_ref` that tells the oct-tree how many particles to refine on.  The default is 64, but we'll get prettier plots (at the expense of a deeper tree) with 8.  Just passing the argument `n_ref=8` to load does this for us.

# >This dataset is available for download at http://yt-project.org/data/TipsyGalaxy.tar.gz (10 MB).

# In[ ]:

ds = yt.load('TipsyGalaxy/galaxy.00300', n_ref=8)


# We now have a `TipsyDataset` object called `ds`.  Let's see what fields it has.

# In[ ]:

ds.field_list


# yt also defines so-called "derived" fields.  These fields are functions of the on-disk fields that live in the `field_list`.  There is a `derived_field_list` attribute attached to the `Dataset` object - let's take look at the derived fields in this dataset:

# In[ ]:

ds.derived_field_list


# All of the field in the `field_list` are arrays containing the values for the associated particles.  These haven't been smoothed or gridded in any way. We can grab the array-data for these particles using `ds.all_data()`. For example, let's take a look at a temperature-colored scatterplot of the gas particles in this output.

# In[ ]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:

dd = ds.all_data()
xcoord = dd['Gas','Coordinates'][:,0].v
ycoord = dd['Gas','Coordinates'][:,1].v
logT = np.log10(dd['Gas','Temperature'])
plt.scatter(xcoord, ycoord, c=logT, s=2*logT, marker='o', edgecolor='none', vmin=2, vmax=6)
plt.xlim(-20,20)
plt.ylim(-20,20)
cb = plt.colorbar()
cb.set_label('$\log_{10}$ Temperature')
plt.gcf().set_size_inches(15,10)


### Making Smoothed Images

# yt will automatically generate smoothed versions of these fields that you can use to plot.  Let's make a temperature slice and a density projection.

# In[ ]:

yt.SlicePlot(ds, 'z', ('gas','density'), width=(40, 'kpc'), center='m')


# In[ ]:

yt.ProjectionPlot(ds, 'z', ('gas','density'), width=(40, 'kpc'), center='m')


# Not only are the values in the tipsy snapshot read and automatically smoothed, the auxiliary files that have physical significance are also smoothed.  Let's look at a slice of Iron mass fraction.

# In[ ]:

yt.SlicePlot(ds, 'z', ('gas', 'FeMassFrac'), width=(40, 'kpc'), center='m')

