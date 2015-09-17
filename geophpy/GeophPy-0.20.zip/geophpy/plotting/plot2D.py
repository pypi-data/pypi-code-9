# -*- coding: utf-8 -*-
'''
    geophpy.plotting.plot2D
    -----------------------

    Map Plotting in 2D dimensions.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from geophpy.misc.utils import *

from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata


def plot_surface(dataset, cmapname, creversed=False, fig=None, filename=None, cmmin=None, cmmax=None, interpolation='none', cmapdisplay=True, axisdisplay=True, pointsdisplay=False, dpi=600, transparent=False, logscale=False, rects=None, points=None):
   """
   plotting in 2D-dimensions a surface
   """

   if (creversed == True):             # if reverse flag is True
      cmapname = cmapname + '_r'       # adds '_r' at the colormap name to use the reversed colormap

   cmap = plt.get_cmap(cmapname)       # gets the colormap
   
   if (fig == None) :                  # if first display
      fig = plt.figure()               # creates fthe figure
   else :                              # if not first display
      fig.clf()                        # clears figure
      
   ax = fig.add_subplot(111)

   Z = (dataset.data.z_image)          # reads the z_image of the dataset

   plt.xlabel(dataset.data.fields[0])
   plt.ylabel(dataset.data.fields[1])
   if (axisdisplay == True):           # displays the axis if required
      plt.suptitle(dataset.data.fields[2])
   else:
      plt.suptitle("")
   ax.get_xaxis().set_visible(axisdisplay)
   ax.get_yaxis().set_visible(axisdisplay)

   if (logscale == True):
      norm = colors.LogNorm()
   else:
      norm = colors.Normalize()

                                       # builds the image
   im = ax.imshow(Z, extent=(dataset.info.x_min-(dataset.info.x_gridding_delta/2),dataset.info.x_max+(dataset.info.x_gridding_delta/2),dataset.info.y_min-(dataset.info.y_gridding_delta/2),dataset.info.y_max+(dataset.info.y_gridding_delta/2)), interpolation=interpolation, cmap=cmap, vmin=cmmin, vmax=cmmax, norm=norm, origin='lower', aspect='auto')

   if (cmapdisplay == True):           # displays the color bar if required
      divider = make_axes_locatable(ax)
      cax = divider.append_axes("right", size="5%", pad=0.1)
      colormap = plt.colorbar(im,cax=cax)
   else:
      colormap = None

   if (pointsdisplay == True):         # displays the gridding points if required
      if (dataset.info.gridding_interpolation != 'none'):
         x_decimal_maxnb = getdecimalsnb(dataset.info.x_gridding_delta)
         y_decimal_maxnb = getdecimalsnb(dataset.info.y_gridding_delta)   
         xi = np.linspace(dataset.info.x_min, dataset.info.x_max, 1 + (np.around((dataset.info.x_max-dataset.info.x_min)/dataset.info.x_gridding_delta)), endpoint = True)         
         yi = np.linspace(dataset.info.y_min, dataset.info.y_max, 1 + (np.around((dataset.info.y_max-dataset.info.y_min)/dataset.info.y_gridding_delta)), endpoint = True)
         xi, yi = np.around(xi, decimals=x_decimal_maxnb), np.around(yi, decimals=y_decimal_maxnb)      
         X, Y = np.meshgrid(xi, yi)                                     # builds the (X, Y) gridded matrix
         for i in range(len(X)):
            ax.scatter(X[i], Y[i], s=1, c='k')
      else:
         x=dataset.data.values[:,0]
         y=dataset.data.values[:,1]         
         ax.plot(x, y, 'k.', ms=1)

   ax.set_xlim(dataset.info.x_min, dataset.info.x_max)
   ax.set_ylim(dataset.info.y_min, dataset.info.y_max)

   if (transparent == True):           # if transparent display asked for 'nan' values
      ax.patch.set_alpha(0.0)          # set alpha mode

                                       # displays selection rectangle if required
   if (rects != None):
       for rect in rects:
          if (len(rect) == 4 ):
             x = rect[0]
             y = rect[1]
             w = rect[2]
             h = rect[3]
             
             if (x < dataset.info.x_min):
                x = dataset.info.x_min
             if ((x+w) > dataset.info.x_max):
                w = dataset.info.x_max - x
             if (y < dataset.info.y_min):
                y = dataset.info.y_min
             if ((y+h) > dataset.info.y_max):
                h = dataset.info.y_max - y         
             ax.add_patch(patches.Rectangle((x, y), w, h, fill=False, edgecolor="red"))

   if (points != None):
       for point in points:
          if (len(point) == 2 ):
             x = point[0]
             y = point[1]
             
             if (x < dataset.info.x_min):
                x = dataset.info.x_min
             if (y < dataset.info.y_min):
                y = dataset.info.y_min
             ax.plot([x-0.5,x+0.5],[y,y], color='green', linestyle='solid')
             ax.plot([x,x],[y-0.5,y+0.5], color='green', linestyle='solid')

   if (filename != None):
      if ((axisdisplay == False) and (cmapdisplay == False)):        # the plotting has to be displayed in the full picture         
         plt.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight', pad_inches=0)
      else:
         plt.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight')

   fig.canvas.draw()
   return fig, colormap



def plot_contour(dataset, cmapname, creversed=False, fig=None, filename=None, cmmin=None, cmmax=None, cmapdisplay=True, axisdisplay=True, pointsdisplay=False, dpi=600, transparent=False, logscale=False, rects=None, points=None):
   """
   plotting in 2D-dimensions contours
   """

   if (creversed == True):             
      cmapname = cmapname + '_r'
   cmap = plt.get_cmap(cmapname)
   if (fig == None):
      fig = plt.figure()
   else :
      fig.clf()            # clears figure
      
   ax = fig.add_subplot(111)

   x_decimal_maxnb = getdecimalsnb(dataset.info.x_gridding_delta)
   y_decimal_maxnb = getdecimalsnb(dataset.info.y_gridding_delta)
   
   Z = (dataset.data.z_image)
   xi = np.linspace(dataset.info.x_min, dataset.info.x_max, 1 + (np.around((dataset.info.x_max-dataset.info.x_min)/dataset.info.x_gridding_delta)), endpoint = True)
   yi = np.linspace(dataset.info.y_min, dataset.info.y_max, 1 + (np.around((dataset.info.y_max-dataset.info.y_min)/dataset.info.y_gridding_delta)), endpoint = True)
   xi, yi = np.around(xi, decimals=x_decimal_maxnb), np.around(yi, decimals=y_decimal_maxnb)

   X, Y = np.meshgrid(xi, yi)                          # builds the (X, Y) gridded matrix

   if (axisdisplay == True):
      plt.xlabel(dataset.data.fields[0])
      plt.ylabel(dataset.data.fields[1])
      ax.get_xaxis().set_visible(True)
      ax.get_yaxis().set_visible(True)
      plt.title(dataset.data.fields[2])
   else:
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)

   if (transparent == True):           # if transparent display asked for 'nan' values
      ax.patch.set_alpha(0.0)          # set alpha mode

   if (logscale == True):
      norm = colors.LogNorm()
   else:
      norm = colors.Normalize()

   contour = ax.contour(X, Y, Z, extent=(dataset.info.x_min-(dataset.info.x_gridding_delta/2),dataset.info.x_max+(dataset.info.x_gridding_delta/2),dataset.info.y_min-(dataset.info.y_gridding_delta/2),dataset.info.y_max+(dataset.info.y_gridding_delta/2)), cmap=cmap, vmin=cmmin, vmax=cmmax, norm=norm, origin='lower', aspect='auto')

   if (cmapdisplay == True):
      divider = make_axes_locatable(ax)
      cax = divider.append_axes("right", size="5%", pad=0.1)
      colormap = plt.colorbar(contour,cax=cax, ax=ax, ticks=[cmmin, cmmax])
   else:
      colormap = None

   if (pointsdisplay == True):
      x_decimal_maxnb = getdecimalsnb(dataset.info.x_gridding_delta)
      y_decimal_maxnb = getdecimalsnb(dataset.info.y_gridding_delta)   
      xi = np.linspace(dataset.info.x_min, dataset.info.x_max, 1 + (np.around((dataset.info.x_max-dataset.info.x_min)/dataset.info.x_gridding_delta)), endpoint = True)
      yi = np.linspace(dataset.info.y_min, dataset.info.y_max, 1 + (np.around((dataset.info.y_max-dataset.info.y_min)/dataset.info.y_gridding_delta)), endpoint = True)
      xi, yi = np.around(xi, decimals=x_decimal_maxnb), np.around(yi, decimals=y_decimal_maxnb)      
      X, Y = np.meshgrid(xi, yi)                          # builds the (X, Y) gridded matrix
      for i in range(len(X)):
         ax.scatter(X[i], Y[i], s=1, c='b')
                  
   ax.set_xlim(dataset.info.x_min, dataset.info.x_max)
   ax.set_ylim(dataset.info.y_min, dataset.info.y_max)

   if (transparent == True):           # if transparent display asked for 'nan' values
      ax.patch.set_alpha(0.0)          # set alpha mode

   if (rects != None):
       for rect in rects:
          if (len(rect) == 4 ):
             x = rect[0]
             y = rect[1]
             w = rect[2]
             h = rect[3]
             
             if (x < dataset.info.x_min):
                x = dataset.info.x_min
             if ((x+w) > dataset.info.x_max):
                w = dataset.info.x_max - x
             if (y < dataset.info.y_min):
                y = dataset.info.y_min
             if ((y+h) > dataset.info.y_max):
                h = dataset.info.y_max - y         
             ax.add_patch(patches.Rectangle((x, y), w, h, fill=False, edgecolor="red"))
                  
   if (points != None):
       for point in points:
          if (len(point) == 2 ):
             x = point[0]
             y = point[1]
             
             if (x < dataset.info.x_min):
                x = dataset.info.x_min
             if (y < dataset.info.y_min):
                y = dataset.info.y_min
             ax.plot([x-0.5,x+0.5],[y,y], color='green', linestyle='solid')
             ax.plot([x,x],[y-0.5,y+0.5], color='green', linestyle='solid')

   if (filename != None):
      if ((axisdisplay == False) and (cmapdisplay == False)):        # the plotting has to be displayed in the full picture
         plt.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight', pad_inches=0)
      else:
         plt.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight')

   fig.canvas.draw()
   return fig, colormap



def plot_contourf(dataset, cmapname, creversed=False, fig=None, filename=None, cmmin=None, cmmax=None, cmapdisplay=True, axisdisplay=True, pointsdisplay=False, dpi=600, transparent=False, logscale=False, rects=None):
   """
   plotting in 2D-dimensions fill contours
   """

   if (creversed == True):
      cmapname = cmapname + '_r'
   cmap = plt.get_cmap(cmapname)
   if (fig == None):
      fig = plt.figure()
   else :
      fig.clf()            # clears figure
      
   ax = fig.add_subplot(111)

   x_decimal_maxnb = getdecimalsnb(dataset.info.x_gridding_delta)
   y_decimal_maxnb = getdecimalsnb(dataset.info.y_gridding_delta)
   
   Z = (dataset.data.z_image)
   xi = np.linspace(dataset.info.x_min, dataset.info.x_max, 1 + (np.around((dataset.info.x_max-dataset.info.x_min)/dataset.info.x_gridding_delta)), endpoint = True)
   yi = np.linspace(dataset.info.y_min, dataset.info.y_max, 1 + (np.around((dataset.info.y_max-dataset.info.y_min)/dataset.info.y_gridding_delta)), endpoint = True)
   xi, yi = np.around(xi, decimals=x_decimal_maxnb), np.around(yi, decimals=y_decimal_maxnb)

   X, Y = np.meshgrid(xi, yi)                          # builds the (X, Y) gridded matrix

   if (axisdisplay == True):
      plt.xlabel(dataset.data.fields[0])
      plt.ylabel(dataset.data.fields[1])
      plt.title(dataset.data.fields[2])
      ax.get_xaxis().set_visible(True)
      ax.get_yaxis().set_visible(True)
   else:
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)

   if (logscale == True):      
      norm = colors.LogNorm()
   else:
      norm = colors.Normalize()
      
   contour = ax.contourf(X, Y, Z, extent=(dataset.info.x_min-(dataset.info.x_gridding_delta/2),dataset.info.x_max+(dataset.info.x_gridding_delta/2),dataset.info.y_min-(dataset.info.y_gridding_delta/2),dataset.info.y_max+(dataset.info.y_gridding_delta/2)), cmap=cmap, vmin=cmmin, vmax=cmmax, norm=norm, origin='lower', aspect='auto')

   if (cmapdisplay == True):
      divider = make_axes_locatable(ax)
      cax = divider.append_axes("right", size="5%", pad=0.1)
      colormap = plt.colorbar(contour,cax=cax, ax=ax, norm=norm, boundaries=[cmmin, cmmax], ticks=[cmmin, cmmax])
   else:
      colormap = None

   if (pointsdisplay == True):
      x_decimal_maxnb = getdecimalsnb(dataset.info.x_gridding_delta)
      y_decimal_maxnb = getdecimalsnb(dataset.info.y_gridding_delta)   
      xi = np.linspace(dataset.info.x_min, dataset.info.x_max, 1 + (np.around((dataset.info.x_max-dataset.info.x_min)/dataset.info.x_gridding_delta)), endpoint = True)
      yi = np.linspace(dataset.info.y_min, dataset.info.y_max, 1 + (np.around((dataset.info.y_max-dataset.info.y_min)/dataset.info.y_gridding_delta)), endpoint = True)
      xi, yi = np.around(xi, decimals=x_decimal_maxnb), np.around(yi, decimals=y_decimal_maxnb)      
      X, Y = np.meshgrid(xi, yi)                          # builds the (X, Y) gridded matrix
      for i in range(len(X)):
         ax.scatter(X[i], Y[i], s=1, c='b')
      
   ax.set_xlim(dataset.info.x_min, dataset.info.x_max)
   ax.set_ylim(dataset.info.y_min, dataset.info.y_max)
                  
   if (transparent == True):           # if transparent display asked for 'nan' values
      ax.patch.set_alpha(0.0)          # set alpha mode

   if (rects != None):
       for rect in rects:
          if (len(rect) == 4 ):
             x = rect[0]
             y = rect[1]
             w = rect[2]
             h = rect[3]
             
             if (x < dataset.info.x_min):
                x = dataset.info.x_min
             if ((x+w) > dataset.info.x_max):
                w = dataset.info.x_max - x
             if (y < dataset.info.y_min):
                y = dataset.info.y_min
             if ((y+h) > dataset.info.y_max):
                h = dataset.info.y_max - y         
             ax.add_patch(patches.Rectangle((x, y), w, h, fill=False, edgecolor="red"))
                  
   if (points != None):
       for point in points:
          if (len(point) == 2 ):
             x = point[0]
             y = point[1]
             
             if (x < dataset.info.x_min):
                x = dataset.info.x_min
             if (y < dataset.info.y_min):
                y = dataset.info.y_min
             ax.plot([x-0.5,x+0.5],[y,y], color='green', linestyle='solid')
             ax.plot([x,x],[y-0.5,y+0.5], color='green', linestyle='solid')

   if (filename != None):
      if ((axisdisplay == False) and (cmapdisplay == False)):        # the plotting has to be displayed in the full picture
         plt.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight', pad_inches=0)
      else:
         plt.savefig(filename, dpi=dpi, transparent=transparent, bbox_inches='tight')

   fig.canvas.draw()
   return fig, colormap
