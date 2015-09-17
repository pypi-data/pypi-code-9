# -*- coding: utf-8 -*-
'''
    wumappy.gui.geoposset.geopossetwindow
    -------------------------------------

    Geographic Position set window management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from geophpy.geoposset import *
from PySide import QtCore, QtGui
from wumappy.gui.common.menubar import *
from wumappy.gui.geoposset.geopossetconfigdlgbox import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

ITEM_FILES = 1
ITEM_CLOSE = 10
ITEM_PRINT = 11
ITEM_EXPORT = 12
ITEM_EXPORT_PICTURE = 13
ITEM_EXPORT_KML = 14
ITEM_EXPORT_RASTER = 15
ITEM_SAVE = 16
ITEM_CONFIG = 2
    

#---------------------------------------------------------------------------#
# Geographic Position set Window Object                                     #
#---------------------------------------------------------------------------#
class GeopossetWindow():
    wid = None                  # window id
    dataset = None              
    plottype = None             
    cmap = None
    interpolation = None
    dpi = None
    axisdisplay = False
    cmapdisplay = False
    cmmin = None
    cmmax = None
    fig = None

    def __init__(self):
        self.ItemList = [[ITEM_FILES, 'FILES_ID', "Menu", "", None, True], 
#                         [ITEM_PRINT, 'PRINT_ID', self.print, "Print the geographic position set picture", ITEM_FILES, True], 
                         [ITEM_SAVE, 'SAVE_ID', self.save, "Saves the geographic position set", ITEM_FILES, True],
                         [ITEM_EXPORT, 'EXPORT_ID', "Menu", "", ITEM_FILES, True], 
                         [ITEM_EXPORT_PICTURE, "EXPORTIMAGE_ID", self.exportPictureFile, "Exports the geographic position set picture in a picture format file", ITEM_EXPORT, True], 
                         [ITEM_EXPORT_KML, 'EXPORTKML_ID', self.exportKmlFile, "Exports the geographic position set picture in a kmz file to open it in google-earth", ITEM_EXPORT, True],
                         [ITEM_CLOSE, 'CLOSE_ID', self.close, "Closes the geographic position set", ITEM_FILES, True],
                         [ITEM_CONFIG, 'CONFIG_ID', self.config, "", None, True]]



    @classmethod
    def new(cls, parent, title, geoposset, dpi):
        '''
        creates geographic position window associated at a geographic position set
        '''
        
        window = cls()

        window.parent = parent
        success, window.fig = geoposset.plot(dpi=dpi)
        window.title = title
        window.icon = parent.icon
        
        window.wid = QtGui.QWidget()                # builds the windows to insert the canvas
        window.wid.setWindowTitle(window.title)     # sets the windows title
        window.wid.setWindowIcon(window.icon)           # sets the wumappy logo as window icon
        #window.wid.setWindowFlags(type)             # disables the window closing
        window.layoutid = QtGui.QVBoxLayout(window.wid) # implements Layout to display canvas inside
        
        canvas = FigureCanvas(window.fig)           # builds the canvas to display the plot        
        window.layoutid.addWidget(canvas)
                                                    # updates the windows settings
        window.geoposset = geoposset                    
        window.dpi = dpi
        window.asciiset = parent.asciiset
                                            # builds the menubar to insert in the windows
        window.menubar = MenuBar.from_list(window.ItemList, window)
        
        window.layoutid.setMenuBar(window.menubar.id)    # to display layout under menu bar


        return window


    def view(self):
        self.wid.show()


    def save(self):
        '''
        Saves the geographic positions set
        '''
        filename = QtGui.QFileDialog.getSaveFileName(filter = "*.csv")
        if (len(filename[0])>0):
            self.geoposset.save(filename[0])
            

    def close(self):
        '''
        Closes the geographic positions set window
        '''
        self.parent.geopossetwindowslist.remove(self)
        for datasetwindow in self.parent.datasetwindowslist:
            datasetwindow.menubar.update()
        self.wid.close()


    def print(self):
        '''
        Prints the geographic positions set graphic representation
        '''
        None
        

    def exportPictureFile(self):
        '''
        Exports the geographic positions set in a picture format file
        '''
        list = pictureformat_getlist()
        filter = "Image Files ("
        for format in list:
            filter = filter + " *" + format
        filter = filter + ")"

        success = True        
        fullfilename = QtGui.QFileDialog.getSaveFileName(filter = filter)
        filename, extension = os.path.splitext(fullfilename[0])
        if (extension in list):
            self.geoposset.plot(picturefilename = fullfilename[0])
        else:
            success = False
            
        return success

  
    def exportKmlFile(self):
        '''
        Exports the geographic positions set in a kml file
        '''
        success = True        
        kmlfilename = QtGui.QFileDialog.getSaveFileName(filter = "*.kml")
        if (kmlfilename[0] != ''):
            self.geoposset.to_kml(kmlfilename[0])
        else:
            success = False

        return success


    def config(self):
        '''
        Configures the geographics positions set
        '''
        r, config = ConfigGeopossetDlgBox.new("Configures Geographics Positions Set", self)
        if (r == QtGui.QDialog.Accepted):
            self.geoposset = config.geoposset
        else:
            QtGui.QErrorMessage()
