# -*- coding: utf-8 -*-
"""
Functions to plot maps and calculate distances.

TODO:
 - Replace box value given in aspect_ratio by a box parameter
 - make color attribute work with connect_points
 - Return ax
"""

from math import radians, cos, sin, asin, sqrt
import mpl_toolkits.basemap as bm
import matplotlib.pyplot as plt

import numpy as np
import gc


def plot_path_from_above(lon, lat, padding=1., show_map=True, color='red', aspect_ratio=3./4, ax=None):
    """Plot a path (a list of points) over a map using maps provided by ``Basemap``.

    This functions uses very simple ``Basemap`` standard parameters. More options to customize the map should be added in the
    future.

    Parameters
    ----------
    lon : pd.Series
        Series containing the list of longitudes.
    lat : pd.Series
        Series containing the list of latitudes.
    padding : float
        Space to add around path (in degrees). Default is 2 degrees.
    show_map : boolean
        Whether to draw the map around the path. Default is True.
    color : color or list of colors.
        The color of the path. Default is red. Optionally, if the parameter connect_points is False, a list of colors
        can be passed (having the same size as the number of dots). Example:

        >>> colors = plt.cm.get_cmap('coolwarm', number_of_colors)
        >>> color_idx = [ int(i) for i in color_values ]
        >>> geo.plot_path_from_above(lon, lat, color=colors(color_idxs))

    aspect_ratio : float or str or tuple
        Aspect ration of the map. Default is 3/4. The values 'square' and 'fit_extremities' can also be specified. The first
        creates a square map. The second, adds just enough space to fit the extremities (still adding the padding). The coordinates
        of the box containing the map can also be specified as ``(min_lat, max_lat, min_lon, max_lon)``.
    ax : AxesSubplot
        Axes where to plot the map.

    """

    # Determine min and max longitude and latitude and add padding around them
    min_lat = lat.min()
    max_lat = lat.max()
    min_lon = lon.min()
    max_lon = lon.max()


    # Determine the rightmost point of the graph
    if aspect_ratio=='fit_extremities':

        # The rightmost point is just the max lat added with the padding
        max_lat = max_lat # What's this?
        pass

    elif aspect_ratio=='square':

        # The rightmost point the the that make the map a squared box
        max_lat = min_lat + np.abs(max_lon - min_lon) * 3/4 # The 3/4 is need to take into account the different scales between longitudes and latitudes

    elif isinstance(aspect_ratio, float):

        # We reduce some space from the latitude dimension to make the map obey the aspect ration given in the parameter aspect_ratio
        max_lat = min_lat + np.abs(max_lon - min_lon) * 3/4
        min_lat = min_lat + np.abs(max_lat - min_lat) * (0.5 - aspect_ratio/2) # make the min_lat a little higher
        max_lat = max_lat - np.abs(max_lat - min_lat) * (0.5 - aspect_ratio/2) # make the max_lat a little lower

    elif len(aspect_ratio)==4:

        # Get the coordinates provided
        min_lat, max_lat, min_lon, max_lon = aspect_ratio

    else:
        raise Exception('Invalid value for parameter aspect_ratio: %s' % aspect_ratio)


    # Add some space around the path
    min_lat = min_lat - padding * 3/4 # The fator 3/4 is needed to take into account the different scales between longitudes and latitudes
    max_lat = max_lat + padding * 3/4
    min_lon = min_lon - padding
    max_lon = max_lon + padding




    # Draw map, if specified
    if show_map:

        # Create map centered around the path
        m = bm.Basemap(projection='merc',
            resolution = 'l', area_thresh = 1,
            llcrnrlon= min_lon,
            urcrnrlon= max_lon,
            llcrnrlat= min_lat,
            urcrnrlat= max_lat,
            ax=ax
        )

        # Draw paralles and meridians
        m.drawparallels(np.arange(-80.,81.,2.))
        m.drawmeridians(np.arange(-180.,181.,2.))

        # Draw relief and rivers
        m.shadedrelief()
        m.drawrivers()

        # Draw coordinates on map
        m.scatter(lon.values, lat.values, latlon=True, color=color, ax=ax)
    else:

        # Draw coordinates without using a mp
        ax.scatter(lon.values, lat.values, color=color)

    gc.collect()


def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)
    
    This function found was found in many different sites on the internet.
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def _lineMagnitude (x1, y1, x2, y2):
    """Returns the euclidean distance between two points."""
    lineMagnitude = sqrt(pow((x2 - x1), 2)+ pow((y2 - y1), 2))
    return lineMagnitude


def distance_from_point_to_segment (px, py, x1, y1, x2, y2):
    """Returns the minimum distance between a point (px, py) and a line segment (x1, y1, x2, y2).

    Method adapted from Map Rantala, available at:
    https://nodedangles.wordpress.com/2010/05/16/measuring-distance-from-a-point-to-a-line-segment/
    """
    LineMag = _lineMagnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):
        #// closest point does not fall within the line segment, take the shorter distance
        #// to an endpoint
        ix = _lineMagnitude(px, py, x1, y1)
        iy = _lineMagnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = _lineMagnitude(px, py, ix, iy)

    return DistancePointLine



if __name__=='__main__':

    pass
