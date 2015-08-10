import time
import numpy as np
import pyfilm as pf
import matplotlib.pyplot as plt

x = -np.random.rand(10,10,10)                                              
print(np.min(x), np.max(x))
pf.make_film_2d(x, plot_options={'levels':np.linspace(np.min(x),np.max(x),10), 'cmap':'seismic'}, 
        options={'cbar_ticks':10, 'ylabel':r'$\delta n / n $', 'dpi':110}) 

