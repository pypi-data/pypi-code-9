
# It's now easy to adjust the units of a field you are plotting.
# 
# > Note: the following examples use `SlicePlot`, but the same thing should work for `ProjectionPlot`, `OffAxisSlicePlot`, and `OffAxisProjectionPlot`.

# First, let's create a new `SlicePlot`.

# In[ ]:

import yt
ds = yt.load('IsolatedGalaxy/galaxy0030/galaxy0030')
slc = yt.SlicePlot(ds, 2, 'density', center=[0.5, 0.5, 0.5], width=(15, 'kpc'))
slc.set_figure_size(6)


# The units used to scale the colorbar can be adjusted by calling the `set_unit` function that is attached to the plot object.  This example creates a plot of density in code units:

# In[ ]:

slc.set_unit('density', 'code_mass/code_length**3')


# This example creates a plot of gas density in solar masses per cubic parsec:

# In[ ]:

slc.set_unit('density', 'Msun/pc**3')


# The `set_unit` function will accept any unit string that is dimensionally equivalent to the plotted field.  If it is supplied a unit that is not dimensionally equivalent, it will raise an error:

# In[ ]:

from yt.utilities.exceptions import YTUnitConversionError

try:
    slc.set_unit('density', 'Msun')
except YTUnitConversionError as e:
    print e


# Similarly, set_unit is defined for `ProfilePlot` and `PhasePlot` instances as well.
# 
# To illustrate this point, let's first create a new `ProfilePlot`:

# In[ ]:

dd = ds.all_data()
plot = yt.ProfilePlot(dd, 'density', 'temperature', weight_field='cell_mass')
plot.show()


# And adjust the unit of the y-axis:

# In[ ]:

plot.set_unit('density', 'Msun/pc**3')


# Similarly for PhasePlot:

# In[ ]:

plot = yt.PhasePlot(dd, 'density', 'temperature', 'cell_mass')
plot.set_figure_size(6)


# In[ ]:

plot.set_unit('cell_mass', 'Msun')
plot.set_unit('density', 'Msun/pc**3')

