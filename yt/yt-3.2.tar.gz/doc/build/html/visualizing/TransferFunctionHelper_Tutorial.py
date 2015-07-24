
# Here, we explain how to use TransferFunctionHelper to visualize and interpret yt volume rendering transfer functions.  TransferFunctionHelper is a utility class that makes it easy to visualize he probability density functions of yt fields that you might want to volume render.  This makes it easier to choose a nice transfer function that highlights interesting physical regimes.
# 
# First, we set up our namespace and define a convenience function to display volume renderings inline in the notebook.  Using `%matplotlib inline` makes it so matplotlib plots display inline in the notebook.

# In[ ]:

import yt
import numpy as np
from IPython.core.display import Image
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper

def showme(im):
    # screen out NaNs
    im[im != im] = 0.0
    
    # Create an RGBA bitmap to display
    imb = yt.write_bitmap(im, None)
    return Image(imb)


# Next, we load up a low resolution Enzo cosmological simulation.

# In[ ]:

ds = yt.load('Enzo_64/DD0043/data0043')


# Now that we have the dataset loaded, let's create a `TransferFunctionHelper` to visualize the dataset and transfer function we'd like to use.

# In[ ]:

tfh = yt.TransferFunctionHelper(ds)


# `TransferFunctionHelpler` will intelligently choose transfer function bounds based on the data values.  Use the `plot()` method to take a look at the transfer function.

# In[ ]:

# Build a transfer function that is a multivariate gaussian in Density
tfh = yt.TransferFunctionHelper(ds)
tfh.set_field('temperature')
tfh.set_log(True)
tfh.set_bounds()
tfh.build_transfer_function()
tfh.tf.add_layers(5)
tfh.plot()


# Let's also look at the probability density function of the `cell_mass` field as a function of `temperature`.  This might give us an idea where there is a lot of structure. 

# In[ ]:

tfh.plot(profile_field='cell_mass')


# It looks like most of the gas is hot but there is still a lot of low-density cool gas.  Let's construct a transfer function that highlights both the rarefied hot gas and the dense cool gas simultaneously.

# In[ ]:

tfh = yt.TransferFunctionHelper(ds)
tfh.set_field('temperature')
tfh.set_bounds()
tfh.set_log(True)
tfh.build_transfer_function()
tfh.tf.add_layers(8, w=0.01, mi=4.0, ma=8.0, col_bounds=[4.,8.], alpha=np.logspace(-1,2,7), colormap='RdBu_r')
tfh.tf.map_to_colormap(6.0, 8.0, colormap='Reds', scale=10.0)
tfh.tf.map_to_colormap(-1.0, 6.0, colormap='Blues_r', scale=1.)

tfh.plot(profile_field='cell_mass')


# Finally, let's take a look at the volume rendering.

# In[ ]:

L = [-0.1, -1.0, -0.1]
c = ds.domain_center
W = 1.5*ds.domain_width
Npixels = 512 
cam = ds.camera(c, L, W, Npixels, tfh.tf, fields=['temperature'],
                  north_vector=[1.,0.,0.], steady_north=True, 
                  sub_samples=5, no_ghost=False)

# Here we substitute the TransferFunction we constructed earlier.
cam.transfer_function = tfh.tf


im = cam.snapshot()
showme(im[:,:,:3])


# We can clearly see that the hot gas is mostly associated with bound structures while the cool gas is associated with low-density voids.
