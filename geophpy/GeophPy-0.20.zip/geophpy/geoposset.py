# -*- coding: utf-8 -*-
'''
    GeophPy.geoposset
    -----------------

    Geographics Positioning Set management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
import shapefile   # pyshp for reading and writing shapefiles
import geophpy.geopositioning.kml as kml
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import glob                         # for managing severals files thanks to "*." extension
import utm                          # to convert utm and wgs84 coordinates
import os, csv

# definitions
POINT_PARAMS = 'bo'

refsystem_list = ['UTM', 'WGS84']           # list of reference systems availables
filetype_list = ['asciifile', 'shapefile']  # list of file types availables
utm_minletter = 'E'
utm_minnumber = 1
utm_maxletter = 'X'
utm_maxnumber = 60


#---------------------------------------------------------------------------#
# Geographics Positioning Set Object                                        #
#---------------------------------------------------------------------------#
class GeoPosSet(object):
    '''
    Builds a geographic positioning set to display or use to georeferencing data set.
    '''

    refsystem = None                # Geographic positioning Reference System (None, 'UTM', 'WGS84', ...)
    utm_letter = None               # utm letter if refsystem='UTM', None else
    utm_number = None               # utm number if refsystem='UTM', None else
    points_list = []                # List of points, [lat, lon, x, y]

    def __init__(self):
        pass    

    @classmethod
    def from_file(cls, refsystem, utm_zoneletter, utm_zonenumber, filetype, filenameslist):
        '''Builds a geographic positioning set from a list of files.
        
        Parameters :

        :refsystem: geographic positioning reference system, None, 'UTM', 'WGS84', ...

        :utm_zoneletter: E -> X

        :utm_zonenumber: 1 -> 60
        
        :filetype: type of files, 'asciifile', 'shapefile', ...
        
        :filenameslist: list of files to open,
        
        ['shapefile1', 'shapefile2', ...] or,
        ['shapefile*'] to open all files with a filename beginning by "shapefile" (without extensions).

        Returns :
        :success: true if geoposset built, false if not.
        
        :geoposset: geographics positioning set built with file(s).
        
        Example :
        success, geoposset = GeoPosSet.from_file('UTM', 'shapefile', "shapefile1.shp")
        
        '''
        
        geoposset = cls()
        geoposset.type = type
        geoposset.refsystem = refsystem
        geoposset.utm_letter = utm_zoneletter
        geoposset.utm_number = utm_zonenumber
        geoposset.points_list = []
        point_num = 0

        success = True                                                      # by default
        if (filetype == 'shapefile') :
            for filenames in filenameslist :                                # for each file in the list
                try:
                    filenamewithoutextension, extension = os.path.splitext(filenames)
                    filenamesextended = glob.glob(filenamewithoutextension+".shp")         # extension if the filenames if '*' is contained
                    for filename in filenamesextended :
                        sf = shapefile.Reader(filename)
                        shapes = sf.shapes()

                        for shape in shapes :                # for each shape in the file
                            if ((shape.shapeType == shapefile.POINT) or (shape.shapeType == shapefile.POINTZ) or (shape.shapeType == shapefile.POINTM)) :
                                geoposset.points_list.append([point_num, shape.points[0][0], shape.points[0][1], None, None])
                                point_num = point_num + 1
                except IOError:
                    print("File Read Error (",filename,")")
                    success = False
                    break                                                   # exits the loop
        elif (filetype == 'asciifile'):
            for filenames in filenameslist :                                # for each file in the list
                filenamewithoutextension, extension = os.path.splitext(filenames)
                filenamesextended = glob.glob(filenamewithoutextension+extension)         # extension if the filenames if '*' is contained
                for filename in filenamesextended :
                    reader = csv.reader(open(filename,"r", newline=''), delimiter=';')
                    # reads the first line of the file with reference system ('UTM', 'E', 1 or 'WGS84)
                    fullrefsystem = reader.__next__()
                    refsystem = fullrefsystem[0]
                    if (refsystem == 'UTM'):
                        geoposset.refsystem = refsystem
                        try :
                            utm_zoneletter = fullrefsystem[1]
                            if (utm_zoneletter.isalpha() and (utm_zoneletter >= utm_minletter) and (utm_zonletter <= utm_maxletter)) :
                                geoposset.utm_letter = utm_zoneletter
                            utm_zonenumber = fullrefsystem[2]
                            if (utm_zonenumber.isdigit() and (utm_zonenumber >= utm_minnumber) and (utm_zonenumber <= utm_maxnumber)) :
                                geoposset.utm_number = utm_zonenumber
                        except :
                            pass
                    elif (refsystem == 'WGS84'):
                        geoposset.refsystem = refsystem
                    else:                       # consideres the first row as a point description
                        row = fullrefsystem
                        try :
                            x = float(row[3])
                        except :
                            x = None
                        try :
                            y = float(row[4])
                        except :
                            y = None
                        try :
                            geoposset.points_list.append([point_num, float(row[1]), float(row[2]), x, y])
                            point_num = point_num + 1
                        except :
                            print("File Read Error (",filename,": ",row, ")")
                            success = False
                        
                    for row in reader:          # reads the others rows as point descriptions
                        try :
                            x = float(row[3])
                        except :
                            x = None
                        try :
                            y = float(row[4])
                        except :
                            y = None
                        try :
                            geoposset.points_list.append([point_num, float(row[1]), float(row[2]), x, y])
                            point_num = point_num + 1
                        except :
                            print("File Read Error (",filename,": ",row, ")")
                            success = False
        else :
            success = False

        geoposset.points_list.append([-1, 0, 0, None, None])            # trick to convert np.array in good format
        geoposset.points_list = np.array(geoposset.points_list)
        geoposset.points_list = np.delete(geoposset.points_list, -1, 0) # to delete last row added 
        return success, geoposset



    def save(self, filename):
        '''
        Saves the geographic positions set in a csv file with ';' as delimiter and :
        At the first line : Reference System, 'UTM', 'WGS84', ...array and if 'UTM':
            UTM Zone letter and UTM Zone number, ['UTM', zoneletter, zonenumber], or ['WGS84'].
        At the next lines, list of points, [[numpoint, longitude or easting, latitude or northing, X, Y] ...]
        
        Parameters :
        
        :csvfilename: name of the file to save the geographic positions set
        
        Returns :

        :success: True if success, False if not
        
        '''
        
        ResultFile = csv.writer(open(filename,"w", newline=''), delimiter=';')
        # writes the first line of the file with reference system ('UTM', 'WGS84', ...)
        fullrefsystem = [self.refsystem]
        # if 'UTM' ref system, writes the second and third lines with UTM zone letter and number
        if (self.refsystem == 'UTM'):
            fullrefsystem = [self.refsystem, self.utm_letter, self.utm_number]
        else :
            fullrefsystem = [self.refsystem]            
        ResultFile.writerow(fullrefsystem)
        # writes points list in the file.
        ResultFile.writerows(self.points_list)



    def plot(self, picturefilename=None, dpi=None, transparent=False, i_xmin=None, i_xmax=None, i_ymin=None, i_ymax=None):
        '''
        display map of points, lines, and surfaces described in geographic positioning list

        Parameters :
        
        :picturefilename: name of the file to save the picture. If None, no picture saved in a file
        
        :dpi:
        
        :transparent: if True, picture display points not plotted as transparents
        
        :i_xmin: x minimal value to display, None by default
        
        :i_xmax: x maximal value to display, None by default
        
        :i_ymin: y minimal value to display, None by default
        
        :i_ymax: y maximal value to display, None by default

        Returns :

        :success: True if no error

        :fig: figure object

        '''

        fig = plt.figure()                                  # creation of the empty figure

        for point in self.points_list:
            plt.plot(point[1], point[2], POINT_PARAMS)
            plt.text(point[1], point[2], point[0])

        xmin = min(self.points_list.T[0])
        xmax = max(self.points_list.T[0])
        ymin = min(self.points_list.T[1])
        ymax = max(self.points_list.T[1])

        success = True
        if (success == True):
            # for each x or y limit not configured in input, initialisation of the value with the limits of points displayed
            nolimits = True
            if (i_xmin == None) :
                i_xmin = xmin
            else :
                nolimits = False
            if (i_xmax == None) :
                i_xmax = xmax
            else :
                nolimits = False
            if (i_ymin == None) :
                i_ymin = ymin
            else :
                nolimits = False
            if (i_ymax == None) :
                i_ymax = ymax
            else :
                nolimits = False

            if (nolimits == False) :                    # sets the axis limits                                
                xmin, xmax, ymin, ymax = plt.axis([i_xmin, i_xmax, i_ymin, i_ymax])
            else :                                      # gets the axis limits
                xmin, xmax, ymin, ymax = plt.axis()

            # to have the same scale in X and Y axis
            dy = ymax - ymin
            dx = xmax - xmin
            if (dy > dx):
                xmax = xmin + dy
            elif (dx > dy):
                ymax = ymin + dx
            plt.axis([xmin, xmax, ymin, ymax])
  
            ax = plt.gca()
            ax.ticklabel_format(useOffset=False)

            if (picturefilename != None) :               # if picturefilename in input, saves in a picture file
                plt.savefig(picturefilename, dpi=dpi, transparent=transparent)
            
        return success, fig



    def to_kml(self, kmlfilename):
        """
        Builds a kml file with points described in a list of geographic positioning set

        Parameters :

        :kmlfilename: Name of the kml file to save

        Returns :

        :success: True if operation done

        """
        success = True                                      # by default
        kml.geoposset_to_kmlfile(self.points_list, kmlfilename)

        return success



#===========================================================================#

#---------------------------------------------------------------------------#
# General Geographic Positioning Set Environments functions                 #
#---------------------------------------------------------------------------#

def refsys_getlist():
    """
    Returns list of reference systems availables, 'UTM', 'WGS84', ...
    """
    return refsystem_list


def filetype_getlist():
    """
    Returns list of geographic positioning file type, 'asciifile', 'shapefile', ...
    """
    return filetype_list


def utm_to_wgs84(easting, northing, zonenumber, zoneletter):
    """
    Converts UTM to WGS84 coordinates

    Parameters :

    :easting: east UTM coordinate

    :northing: north UTM coordinate

    :zonenumber: zone number

    :zone letter: zone letter

    Returns :

    :latitude: WGS84 latitude coordinate

    :longitude: WGS84 longitude coordinate
    """
    return utm.to_latlon(easting, northing, zonenumber, zoneletter)



def wgs84_to_utm(latitude, longitude):
    """
    Converts WGS84 to UTM coordinates

    Parameters :

    :latitude: WGS84 latitude coordinate

    :longitude: WGS84 longitude coordinate

    Returns :

    :easting: east UTM coordinate

    :northing: north UTM coordinate

    :zonenumber: zone number

    :zone letter: zone letter
    """
    return utm.from_latlon(latitude, longitude)


def utm_getzonelimits():
    """
    Gets the min and max numbers and letters of the UTM coordinates system

    Returns:

    :min_number: minimal number of the UTM zone, 1.

    :min_letter: minimal letter of the UTM zone, E.

    :max_numbre: maximal number of the UTM zone, 60.

    :max letter: maximal letter of the UTM zone, X.
    
    """
    return utm_minnumber, utm_minletter, utm_maxnumber, utm_maxletter
