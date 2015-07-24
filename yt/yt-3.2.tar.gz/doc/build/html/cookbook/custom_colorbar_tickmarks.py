
# In[ ]:

import yt


# In[ ]:

ds = yt.load('IsolatedGalaxy/galaxy0030/galaxy0030')
slc = yt.SlicePlot(ds, 'x', 'density')
slc


# `PlotWindow` plots are containers for plots, keyed to field names.  Below, we get a copy of the plot for the `Density` field.

# In[ ]:

plot = slc.plots['density']


# The plot has a few attributes that point to underlying `matplotlib` plot primites.  For example, the `colorbar` object corresponds to the `cb` attribute of the plot.

# In[ ]:

colorbar = plot.cb


# To set custom tickmarks, simply call the `matplotlib` [`set_ticks`](http://matplotlib.org/api/colorbar_api.html#matplotlib.colorbar.ColorbarBase.set_ticks) and [`set_ticklabels`](http://matplotlib.org/api/colorbar_api.html#matplotlib.colorbar.ColorbarBase.set_ticklabels) functions.

# In[ ]:

colorbar.set_ticks([1e-28])
colorbar.set_ticklabels(['$10^{-28}$'])
slc

