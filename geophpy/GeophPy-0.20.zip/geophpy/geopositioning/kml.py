# -*- coding: utf-8 -*-
'''
    geophpy.geopositioning.kml
    --------------------------

    Kml files managing, reading and writing.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import simplekml
import shapefile   # pyshp for reading and writing shapefiles

def geoposset_to_kmlfile(points_list, kmlfilename):
   '''Construct a kml file with points described in a list of points.'''

   kml = simplekml.Kml()

   for point in points_list :                   # for each point
      coords = [(point[1], point[2])]
      kml.newpoint(name=str(point[0]), coords=coords)

   kml.save(kmlfilename)                        # saves the kml file



def picture_to_kml(picturefilename, quadcoords, kmlfilename):
   '''
   Builds a kml file with an image to display.
   '''

   kml = simplekml.Kml()
   picture = kml.newgroundoverlay(name=picturefilename)
   picture.icon.href = picturefilename
   picture.gxlatlonquad.coords = quadcoords
   kml.save(kmlfilename)


