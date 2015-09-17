# -*- coding: utf-8 -*-
'''
    geophpy.plotting.colormap
    -------------------------

    Color map managing.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import matplotlib.pyplot as plt
import numpy as np

# list of interpolations availables
cmap_list = ['Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'GnBu', 'Greens', 'Greys', 'OrRd', 'Oranges', 'PRGn', 'PiYG', 'PuBu', 'PuOr', 'PuRd','Purples','RdBu','RdGy','RdPu','RdYlBu', 'RdYlGn', 'Reds', 'Spectral', 'Wistia', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 'autumn', 'binary', 'bone', 'bwr', 'copper', 'gist_earth', 'gist_gray', 'gist_heat', 'gist_yarg', 'gnuplot', 'gray', 'hot', 'hsv', 'jet', 'ocean', 'pink', 'spectral', 'terrain']    


def getlist():
   '''Getting the colormap list.
   
   '''

#   colormapslist = sorted(m for m in plt.cm.datad if not m.endswith("_r"))
   colormapslist = sorted(m for m in cmap_list)

   return colormapslist



def plot(cmname, creversed = False, fig=None, filename=None, dpi=None, transparent=False):
   '''
        plotting the colormap.
    
        Parameters :

        :cmname: Name of the colormap, 'gray_r' for example.

        :creversed: True to add '_r' at the cmname to reverse the color map

        :filename: Name of the color map file to save, None if no file to save. 
    
        :dpi: 'dot per inch' definition of the picture file if filename != None

        :transparent: True to manage the transparency.

        Returns : figure and color map plot object.

   '''
   
   gradient = np.linspace(0, 1, 256)
   gradient = np.vstack((gradient, gradient))

   if (fig == None):
      fig = plt.figure( figsize=(1,0.1))
   else :
      fig.clf()            # clears figure
      
   ax = fig.add_subplot(1,1,1)
   fig.subplots_adjust(top=0.99, bottom=0.01, left=0.001, right=0.999)

   if (creversed == True):
      cmname = cmname + '_r'

   ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(cmname))
   ax.set_axis_off()

   if (filename != None):
      plt.savefig(filename, dpi=dpi, transparent=transparent)

   return fig
