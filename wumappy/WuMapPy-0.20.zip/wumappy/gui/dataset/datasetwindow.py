# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.datasetwindow
    ---------------------------------

    Data set window management.

    :copyright: Copyright 2014 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
from wumappy.gui.dataset.georefdlgbox import *
from wumappy.gui.common.cartodlgbox import *
from wumappy.gui.common.menubar import *
from wumappy.gui.dataset.dispsettingsdlgbox import *
from wumappy.gui.dataset.peakfiltdlgbox import *
from wumappy.gui.dataset.medianfiltdlgbox import *
from wumappy.gui.dataset.festoonfiltdlgbox import *
from wumappy.gui.dataset.regtrendfiltdlgbox import *
from wumappy.gui.dataset.wallisfiltdlgbox import *
from wumappy.gui.dataset.ploughfiltdlgbox import *
from wumappy.gui.dataset.constdestripdlgbox import *
from wumappy.gui.dataset.cubicdestripdlgbox import *
from wumappy.gui.dataset.logtransformdlgbox import *
from wumappy.gui.dataset.polereductiondlgbox import *
from wumappy.gui.dataset.continuationdlgbox import *
from wumappy.gui.dataset.eulerdeconvolutiondlgbox import *
from wumappy.gui.dataset.datasetinformationsdlgbox import *
from wumappy.gui.dataset.analyticsignaldlgbox import *
from wumappy.gui.dataset.susceptibilitydlgbox import *
from wumappy.gui.dataset.gradmagfieldconversiondlgbox import *

import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

ITEM_FILES = 1
ITEM_SETTINGS = 2
ITEM_PROCESSING = 3
ITEM_MAGPROCESSING = 4
ITEM_INFORMATIONS = 5
ITEM_GEOREFERENCING = 6
ITEM_CLOSE = 10
ITEM_PRINT = 11
ITEM_EXPORT = 12
ITEM_EXPORT_PICTURE = 13
ITEM_EXPORT_KML = 14
ITEM_EXPORT_RASTER = 15
ITEM_SAVE = 16
ITEM_PEAKFILT = 30
ITEM_MEDIANFILT = 31
ITEM_FESTOONFILT = 32
ITEM_CONSTDESTRIP = 33
ITEM_CUBICDESTRIP = 34
ITEM_REGTRENDFILT = 35
ITEM_WALLISFILT = 36
ITEM_PLOUGHFILT = 37
ITEM_LOGTRANSFORM = 40
ITEM_POLEREDUCTION = 41
ITEM_EQUATORREDUCTION = 42
ITEM_CONTINUATION = 43
ITEM_EULERDECONVOLUTION = 44
ITEM_ANALYTICSIGNAL = 45
ITEM_SUSCEPTIBILITY = 46
ITEM_GRADMAGFIELDCONV = 47
    

#---------------------------------------------------------------------------#
# Data set Window Object                                                    #
#---------------------------------------------------------------------------#
class DatasetWindow(QtGui.QWidget):
    def __init__(self):
        self.wid = None                  # window id
        self.dataset = None              
        self.plottype = None             
        self.colormap = None
        self.reverseflag = False
        self.interpolation = 'bilinear'
        self.dpi = None
        self.axisdisplayflag = False
        self.cbardisplay = False
        self.zmin = None
        self.zmax = None
        self.fig = None
        self.menubarid = None
        self.layoutid = None
        

    @classmethod
    def new(cls, parent, title, dataset, geopossetwindowslist, plottype, colormap, interpolation = 'bilinear', dpi = 600, axisdisplayflag = False, colorbardisplayflag = False, zmin=None, zmax=None, colorbarlogscaleflag=False, reverseflag=False):
        '''
        creates data window associated at a data set
        '''
        
        window = cls()

        window.parent = parent
        window.wid = QtGui.QWidget()                    # builds the windows to insert the canvas
        window.layoutid = QtGui.QVBoxLayout(window.wid) # implements Layout to display canvas inside
        window.title = title
                                                        # updates the windows settings
        window.dataset = dataset
                                                        # memorizes the list of geographic positions set to georeference the data set
        window.geopossetwindowslist = geopossetwindowslist
        window.plottype = plottype
        window.colormap = colormap
        window.interpolation = interpolation
        window.dpi = dpi
        window.axisdisplayflag = axisdisplayflag
        window.colorbardisplayflag = colorbardisplayflag
        window.reverseflag = reverseflag
        window.zmin = zmin
        window.zmax = zmax
        window.colorbarlogscaleflag = colorbarlogscaleflag
        window.configset = parent.configset
        window.icon = parent.icon
        window.asciiset = parent.asciiset
                        # item number, item name, "Menu", function, or None, comment, parent item number, isEnabled function
        window.ItemList = [[ITEM_FILES, 'FILES_ID', "Menu", "", None, True], 
                         [ITEM_SAVE, 'SAVE_ID', window.save, "Saves the data set", ITEM_FILES, True], 
                         [ITEM_CLOSE, 'CLOSE_ID', window.close, "Closes the data set", ITEM_FILES, True], 
#                         [ITEM_PRINT, 'PRINT_ID', window.print, "Print the data set picture", ITEM_FILES, True], 
                         [ITEM_EXPORT, 'EXPORT_ID', "Menu", "", ITEM_FILES, True], 
                         [ITEM_EXPORT_PICTURE, 'EXPORTIMAGE_ID', window.exportPictureFile, "Exports the data set image in an image format file", ITEM_EXPORT, True], 
                         [ITEM_EXPORT_KML, 'EXPORTKML_ID', window.exportKmlFile, "Exports the data set picture in a kmz file to open it in google-earth", ITEM_EXPORT, window.isDatasetGeoreferenced], \
                         [ITEM_EXPORT_RASTER, 'EXPORTRASTER_ID', window.exportRasterFile, "Exports the data set picture in a raster file (picture file + worldfile) to open it in a SIG software", ITEM_EXPORT, window.isDatasetGeoreferenced], \
                         [ITEM_SETTINGS, 'DISPLAYSETTINGS_ID', window.displaySettings, "", None, True], 
                         [ITEM_PROCESSING, 'PROCESSING_ID', "Menu", "", None, True], 
                         [ITEM_PEAKFILT, 'PEAKFILT_ID', window.peakFiltering, "", ITEM_PROCESSING, True], 
                         [ITEM_MEDIANFILT, 'MEDIANFILT_ID', window.medianFiltering, "", ITEM_PROCESSING, True], 
                         [ITEM_FESTOONFILT, 'FESTOONFILT_ID', window.festoonFiltering, "", ITEM_PROCESSING, True], 
                         [ITEM_REGTRENDFILT, 'REGTRENDFILT_ID', window.regtrendFiltering, "", ITEM_PROCESSING, True], 
                         [ITEM_WALLISFILT, 'WALLISFILT_ID', window.wallisFiltering, "", ITEM_PROCESSING, True], 
                         [ITEM_PLOUGHFILT, 'PLOUGHFILT_ID', window.ploughFiltering, "", ITEM_PROCESSING, True], 
                         [ITEM_CONSTDESTRIP, 'CONSTDESTRIP_ID', window.constDestriping, "", ITEM_PROCESSING, True], 
                         [ITEM_CUBICDESTRIP, 'CUBICDESTRIP_ID', window.cubicDestriping, "", ITEM_PROCESSING, True], 
                         [ITEM_MAGPROCESSING, 'MAGPROCESSING_ID', "Menu", "", None, True], 
                         [ITEM_LOGTRANSFORM, 'LOGTRANSFORM_ID', window.logTransform, "", ITEM_MAGPROCESSING, True], 
                         [ITEM_POLEREDUCTION, 'POLEREDUCTION_ID', window.poleReduction, "", ITEM_MAGPROCESSING, True], 
                         [ITEM_CONTINUATION, 'CONTINUATION_ID', window.continuation, "", ITEM_MAGPROCESSING, True],
                         [ITEM_ANALYTICSIGNAL, 'ANALYTICSIGNAL_ID', window.analyticSignal, "", ITEM_MAGPROCESSING, True], 
                         [ITEM_SUSCEPTIBILITY, 'SUSCEPTIBILITY_ID', window.susceptibility, "", ITEM_MAGPROCESSING, True], 
                         [ITEM_GRADMAGFIELDCONV, 'GRADMAGFIELDCONV_ID', window.gradMagFieldConversion, "", ITEM_MAGPROCESSING, True], 
                         [ITEM_EULERDECONVOLUTION, 'EULERDECONV_ID', window.eulerDeconvolution, "", ITEM_MAGPROCESSING, True],
                         [ITEM_GEOREFERENCING, 'GEOREFERENCING_ID', window.georeferenceDataSet, "To geo-reference the data set", None, window.isGeoreferencingAvailable]]
#                         [ITEM_INFORMATIONS, 'INFORMATIONS_ID', window.informations, "Gets informations about data set", None, True]]

                                                        # builds the menubar to insert in the windows
        window.menubar = MenuBar.from_list(window.ItemList, window)
        window.wid.setMinimumSize(window.wid.geometry().size())

        window.layoutid.setMenuBar(window.menubar.id)   # to display layout under menu bar

        window.wid.setWindowTitle(title)                # sets the windows title
        window.wid.setWindowIcon(window.icon)           # sets the wumappy logo as window icon

        # sets the window position under the parent window position
        parentGeometry = parent.wid.geometry()
        windowGeometry = window.wid.geometry()
        windowGeometry.setRect(parentGeometry.x(), parentGeometry.y(), windowGeometry.width(), windowGeometry.height())
        window.wid.setGeometry(windowGeometry)        

        window.updateDisplay()


        return window


    def updateDisplay(self):
        self.fig, cmap = self.dataset.plot(self.plottype, self.colormap, self.reverseflag, fig=self.fig, interpolation = self.interpolation, dpi=self.dpi, axisdisplay=self.axisdisplayflag, cmapdisplay=self.colorbardisplayflag, cmmin=self.zmin, cmmax=self.zmax, logscale=self.colorbarlogscaleflag)
                                                                
        self.layoutid.addWidget(self.fig.canvas)        # adds the canvas in the layout
        
        

    def view(self):
        self.wid.show()


    def close(self):
        '''
        Closes the data set window
        '''
        self.parent.datasetwindowslist.remove(self)
        self.wid.close()


    def save(self):
        '''
        Saves the data set window
        '''
        success = True
        dir = self.configset.get('DIRECTORIES', 'savefiledir')

        initcursor = self.wid.cursor()                                          # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                                # sets the wait cursor

        qfiledlg = QtGui.QFileDialog(self.wid, directory = dir, filter = "*.nc")
        qfiledlg.setFont(self.asciiset.font)
        qfiledlg.setGeometry(self.wid.geometry().left(), self.wid.geometry().top(), qfiledlg.geometry().width(), qfiledlg.geometry().height())
        qfiledlg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        qfiledlg.show()
        qfiledlg.exec()
        if (qfiledlg.result() == QtGui.QDialog.Accepted):
            fullfilename = qfiledlg.selectedFiles()
            self.configset.set('DIRECTORIES', 'savefiledir', os.path.dirname(fullfilename[0]))
            self.dataset.to_file(fullfilename[0], fileformat='netcdf')
        else:
            success = False
            
        self.wid.setCursor(initcursor)                                          # resets the init cursor
        return success


    def print(self):
        '''
        Prints the data set graphic representation
        '''
        success = False
#        printer = QtGui.QPrinter()
#        printDlg = QtGui.QPrintDialog(printer)
#        if printDlg.exec_() == QtGui.QDialog.Accepted:
#            document = QtGui.QTextDocument(self.title)
#            document.addRessource(QtGui.QTextDocument.ImageResource, 
#            document.print_(printer)
#            success = True

        return success



    def informations(self):
        '''
        Displays the data set informations
        '''
        DatasetInformationsDlgBox.new("Informations", self)



    def exportPictureFile(self):
        '''
        Exports the data set in a picture format file
        '''
        list = pictureformat_getlist()
        filter = "Image Files ("
        for format in list:
            filter = filter + " *" + format
        filter = filter + ")"

        success = True
        dir = self.configset.get('DIRECTORIES', 'exportimagedir')

        initcursor = self.wid.cursor()                                          # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                                # sets the wait cursor

        qfiledlg = QtGui.QFileDialog(self.wid, directory = dir, filter = filter)
        qfiledlg.setFont(self.asciiset.font)
        qfiledlg.setGeometry(self.wid.geometry().left(), self.wid.geometry().top(), qfiledlg.geometry().width(), qfiledlg.geometry().height())
        qfiledlg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        qfiledlg.show()
        qfiledlg.exec()
        if (qfiledlg.result() == QtGui.QDialog.Accepted):
            fullfilename = qfiledlg.selectedFiles()
            self.configset.set('DIRECTORIES', 'exportimagedir', os.path.dirname(fullfilename[0]))
            self.dataset.plot(self.plottype, self.colormap, self.reverseflag, fig=None, filename = fullfilename[0], interpolation = self.interpolation, dpi=self.dpi, axisdisplay=self.axisdisplayflag, cmapdisplay=self.colorbardisplayflag, cmmin=self.zmin, cmmax=self.zmax)
        else:
            success = False
            
        self.wid.setCursor(initcursor)                                          # resets the init cursor
        return success


    def exportKmlFile(self):
        '''
        Exports the data set in a kmz file
        '''
        success = True        
        dir = self.configset.get('DIRECTORIES', 'exportkmldir')
        kmlfilename = QtGui.QFileDialog.getSaveFileName(dir=dir, filter = "*.kml")
        filename, extension = os.path.splitext(kmlfilename[0])
        picturefilename = filename + ".png"

        self.configset.set('DIRECTORIES', 'exportkmldir', os.path.dirname(kmlfilename[0]))
        self.dataset.to_kml(self.plottype, self.colormap, kmlfilename[0], self.reverseflag, picturefilename, cmmin=self.zmin, cmmax=self.zmax, interpolation=self.interpolation, dpi=self.dpi)

        return success

        
    def exportRasterFile(self):
        '''
        Exports the data set in a raster format file (.png + .pgw, .jpg + .jgw, .tif + .tfw)
        '''
        list = rasterformat_getlist()
        filter = "Image Files ("
        for format in list:
            filter = filter + " *" + format
        filter = filter + ")"

        success = True        
        dir = self.configset.get('DIRECTORIES', 'exportrasterdir')
        fullfilename = QtGui.QFileDialog.getSaveFileName(dir=dir, filter = filter)
        filename, extension = os.path.splitext(fullfilename[0])
        if (extension in list):
            self.configset.set('DIRECTORIES', 'exportrasterdir', os.path.dirname(fullfilename[0]))
            self.dataset.to_raster(self.plottype, self.colormap, fullfilename[0], self.reverseflag, cmmin=self.zmin, cmmax=self.zmax, interpolation=self.interpolation, dpi=self.dpi)
        else:            
            success = False

        return success


    def displaySettings(self):
        '''
        Adjusts the display settings
        '''
        r, dialogbox = DispSettingsDlgBox.new("Display Settings", self)
        if (r == QtGui.QDialog.Accepted):
            self.axisdisplayflag = dialogbox.axisdisplayflag
            self.colorbardisplayflag = dialogbox.colorbardisplayflag
            self.reverseflag = dialogbox.reverseflag
            self.interpolation = dialogbox.interpolation
            self.plottype = dialogbox.plottype
            self.colormap = dialogbox.colormap
            self.zmin = dialogbox.zmin
            self.zmax = dialogbox.zmax            
            self.colorbarlogscaleflag = dialogbox.colorbarlogscaleflag
            self.updateDisplay()
                            # updates config file
            self.configset.set('DISPSETTINGS', 'plottype', self.plottype)
            self.configset.set('DISPSETTINGS', 'interpolation', self.interpolation)
            self.configset.set('DISPSETTINGS', 'colormap', self.colormap)
            self.configset.set('DISPSETTINGS', 'reverseflag', str(self.reverseflag))
            self.configset.set('DISPSETTINGS', 'colorbardisplayflag', str(self.colorbardisplayflag))
            self.configset.set('DISPSETTINGS', 'colorbarlogscaleflag', str(self.colorbarlogscaleflag))
            self.configset.set('DISPSETTINGS', 'axisdisplayflag', str(self.axisdisplayflag))
            self.configset.set('DISPSETTINGS', 'dpi', str(self.dpi))
            

    def peakFiltering(self):
        '''
        Processes peak filtering
        '''
        nanreplacedflag = self.configset.getboolean('PROCESSING', 'peakfiltnanreplacedflag')
        medianreplacedflag = self.configset.getboolean('PROCESSING', 'peakfiltmedianreplacedflag')
        r, dialogbox = PeakFiltDlgBox.new(self.asciiset.getStringValue('PEAKFILT_ID'), self, nanreplacedflag, medianreplacedflag)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'peakfiltnanreplacedflag', str(dialogbox.nanreplacedflag))
            self.configset.set('PROCESSING', 'peakfiltmedianreplacedflag', str(dialogbox.medianreplacedflag))
            

    def medianFiltering(self):
        '''
        Processes median filtering
        '''
        nxsize = self.configset.getint('PROCESSING', 'medianfiltnxsize')
        nysize = self.configset.getint('PROCESSING', 'medianfiltnysize')
        percent = self.configset.getint('PROCESSING', 'medianfiltpercent')
        gap = self.configset.getint('PROCESSING', 'medianfiltgap')
        r, dialogbox = MedianFiltDlgBox.new(self.asciiset.getStringValue('MEDIANFILT_ID'), self, nxsize, nysize, percent, gap)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'medianfiltnxsize', str(dialogbox.nxsize))
            self.configset.set('PROCESSING', 'medianfiltnysize', str(dialogbox.nysize))
            self.configset.set('PROCESSING', 'medianfiltpercent', str(dialogbox.percent))
            self.configset.set('PROCESSING', 'medianfiltgap', str(dialogbox.gap))
            

    def festoonFiltering(self):
        '''
        Processes festoon filtering
        '''
        method = self.configset.get('PROCESSING', 'festoonfiltmethod')
        shift = self.configset.getint('PROCESSING', 'festoonfiltshift')
        r, dialogbox = FestoonFiltDlgBox.new(self.asciiset.getStringValue('FESTOONFILT_ID'), self, method, shift)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'festoonfiltmethod', dialogbox.method)
            self.configset.set('PROCESSING', 'festoonfiltshift', str(dialogbox.shift))
            

    def wallisFiltering(self):
        '''
        Processes wallis filtering
        '''
        nxsize = self.configset.getint('PROCESSING', 'wallisfiltnxsize')
        nysize = self.configset.getint('PROCESSING', 'wallisfiltnysize')
        setmean = self.configset.getint('PROCESSING', 'wallisfiltsetmean')
        setstdev = self.configset.getint('PROCESSING', 'wallisfiltsetstdev')
        setgain = self.configset.getint('PROCESSING', 'wallisfiltsetgain')
        limit = self.configset.getint('PROCESSING', 'wallisfiltlimit')
        edgefactor = self.configset.getint('PROCESSING', 'wallisfiltedgefactor')
        r, dialogbox = WallisFiltDlgBox.new(self.asciiset.getStringValue('WALLISFILT_ID'), self, nxsize, nysize, setmean, setstdev, setgain, limit, edgefactor)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'wallisfiltnxsize', str(dialogbox.nxsize))
            self.configset.set('PROCESSING', 'wallisfiltnysize', str(dialogbox.nysize))
            self.configset.set('PROCESSING', 'wallisfiltsetmean', str(dialogbox.setmean))
            self.configset.set('PROCESSING', 'wallisfiltsetstdev', str(dialogbox.setstdev))
            self.configset.set('PROCESSING', 'wallisfiltsetgain', str(dialogbox.setgain))
            self.configset.set('PROCESSING', 'wallisfiltlimit', str(dialogbox.limit))
            self.configset.set('PROCESSING', 'wallisfiltedgefactor', str(dialogbox.edgefactor))
            

    def ploughFiltering(self):
        '''
        Processes anti-plough filtering
        '''
        nxsize = self.configset.getint('PROCESSING', 'ploughfiltnxsize')
        nysize = self.configset.getint('PROCESSING', 'ploughfiltnysize')
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        angle = self.configset.getint('PROCESSING', 'ploughangle')
        cutoff = self.configset.getint('PROCESSING', 'ploughcutoff')
        r, dialogbox = PloughFiltDlgBox.new(self.asciiset.getStringValue('PLOUGHFILT_ID'), self, nxsize, nysize, apod, angle, cutoff)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'ploughfiltnxsize', str(dialogbox.nxsize))
            self.configset.set('PROCESSING', 'ploughfiltnysize', str(dialogbox.nysize))
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            self.configset.set('PROCESSING', 'ploughangle', str(dialogbox.angle))
            self.configset.set('PROCESSING', 'ploughcutoff', str(dialogbox.cutoff))
            

    def constDestriping(self):
        '''
        Processes constant destriping
        '''
        method = self.configset.get('PROCESSING', 'destripingmethod')
        nprof = self.configset.getint('PROCESSING', 'destripingprofilesnb')
        r, dialogbox = ConstDestripDlgBox.new(self.asciiset.getStringValue('CONSTDESTRIP_ID'), self, nprof, method)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'destripingmethod', dialogbox.method)
            self.configset.set('PROCESSING', 'destripingprofilesnb', str(dialogbox.nprof))
            

    def cubicDestriping(self):
        '''
        Processes cubic destriping
        '''
        ndeg = self.configset.getint('PROCESSING', 'destripingdegreesnb')
        nprof = self.configset.getint('PROCESSING', 'destripingprofilesnb')
        r, dialogbox = CubicDestripDlgBox.new(self.asciiset.getStringValue('CUBICDESTRIP_ID'), self, nprof, ndeg)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'destripingdegreesnb', str(dialogbox.ndeg))
            self.configset.set('PROCESSING', 'destripingprofilesnb', str(dialogbox.nprof))
            

    def regtrendFiltering(self):
        '''
        Processes regional trend filtering
        '''
        nxsize = self.configset.getint('PROCESSING', 'regtrendfiltnxsize')
        nysize = self.configset.getint('PROCESSING', 'regtrendfiltnysize')
        method = self.configset.get('PROCESSING', 'regtrendmethod')
        component = self.configset.get('PROCESSING', 'regtrendcomponent')
        r, dialogbox = RegTrendFiltDlgBox.new(self.asciiset.getStringValue('REGTRENDFILT_ID'), self, nxsize, nysize, method, component)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'medianfiltnxsize', str(dialogbox.nxsize))
            self.configset.set('PROCESSING', 'medianfiltnysize', str(dialogbox.nysize))
            self.configset.set('PROCESSING', 'regtrendmethod', dialogbox.method)
            self.configset.set('PROCESSING', 'regtrendcomponent', dialogbox.component)
            

    def logTransform(self):
        '''
        Do the transformation in logarithmic units
        '''
        multfactor = self.configset.getint('PROCESSING', 'multfactor')
        r, dialogbox = LogTransformDlgBox.new(self.asciiset.getStringValue('LOGTRANSFORM_ID'), self, multfactor)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'multfactor', str(dialogbox.multfactor))
            

    def poleReduction(self):
        '''
        Do the reduction at the magnetic pole
        '''
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        inclineangle = self.configset.getfloat('PROCESSING', 'maginclineangle')
        alphaangle = self.configset.getfloat('PROCESSING', 'magalphaangle')
        r, dialogbox = PoleReductionDlgBox.new(self.asciiset.getStringValue('POLEREDUCTION_ID'), self, apod, inclineangle, alphaangle)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            self.configset.set('PROCESSING', 'maginclineangle', str(dialogbox.inclineangle))
            self.configset.set('PROCESSING', 'magalphaangle', str(dialogbox.alphaangle))
            

    def continuation(self):
        '''
        Do the magnetic continuation
        '''
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        prosptech = self.configset.get('PROCESSING', 'prosptech')
        downsensoraltitude = self.configset.getfloat('PROCESSING', 'downsensoraltitude')
        upsensoraltitude = self.configset.getfloat('PROCESSING', 'upsensoraltitude')
        continuationflag = self.configset.getboolean('PROCESSING', 'continuationflag')
        continuationvalue = self.configset.getfloat('PROCESSING', 'continuationvalue')
        continuationsoilsurfaceaboveflag = self.configset.getboolean('PROCESSING', 'continuationsoilsurfaceaboveflag')
        r, dialogbox = ContinuationDlgBox.new(self.asciiset.getStringValue('CONTINUATION_ID'), self, prosptech, apod, downsensoraltitude, upsensoraltitude, continuationflag, continuationvalue, continuationsoilsurfaceaboveflag)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            self.configset.set('PROCESSING', 'prosptech', dialogbox.prosptech)
            self.configset.set('PROCESSING', 'downsensoraltitude', str(dialogbox.downsensoraltitude))
            self.configset.set('PROCESSING', 'upsensoraltitude', str(dialogbox.upsensoraltitude))
            self.configset.set('PROCESSING', 'continuationflag', str(dialogbox.continuationflag))
            self.configset.set('PROCESSING', 'continuationvalue', str(dialogbox.continuationvalue))
            self.configset.set('PROCESSING', 'continuationsoilsurfaceaboveflag', str(dialogbox.continuationsoilsurfaceaboveflag))
            

    def analyticSignal(self):
        '''
        Converts to analytic signal
        '''
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        r, dialogbox = AnalyticSignalDlgBox.new(self.asciiset.getStringValue('ANALYTICSIGNAL_ID'), self, apod)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.zmin = dialogbox.zmin
            self.zmax = dialogbox.zmax
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            

    def susceptibility(self):
        '''
        Calculation of an equivalent stratum in magnetic susceptibility
        '''
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        prosptech = self.configset.get('PROCESSING', 'prosptech')
        downsensoraltitude = self.configset.getfloat('PROCESSING', 'downsensoraltitude')
        upsensoraltitude = self.configset.getfloat('PROCESSING', 'upsensoraltitude')
        calcdepthvalue = self.configset.getfloat('PROCESSING', 'calcdepth')
        stratumthicknessvalue = self.configset.getfloat('PROCESSING', 'stratumthickness')
        inclineangle = self.configset.getfloat('PROCESSING', 'maginclineangle')
        alphaangle = self.configset.getfloat('PROCESSING', 'magalphaangle')
        r, dialogbox = SusceptibilityDlgBox.new(self.asciiset.getStringValue('SUSCEPTIBILITY_ID'), self, prosptech, apod, downsensoraltitude, upsensoraltitude, calcdepthvalue, stratumthicknessvalue, inclineangle, alphaangle)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            self.configset.set('PROCESSING', 'prosptech', dialogbox.prosptech)
            self.configset.set('PROCESSING', 'downsensoraltitude', str(dialogbox.downsensoraltitude))
            self.configset.set('PROCESSING', 'upsensoraltitude', str(dialogbox.upsensoraltitude))
            self.configset.set('PROCESSING', 'calcdepth', str(dialogbox.calcdepthvalue))
            self.configset.set('PROCESSING', 'stratumthickness', str(dialogbox.stratumthicknessvalue))
            self.configset.set('PROCESSING', 'maginclineangle', str(dialogbox.inclineangle))
            self.configset.set('PROCESSING', 'magalphaangle', str(dialogbox.alphaangle))
            

    def gradMagFieldConversion(self):
        '''
        Conversion between gradient and magnetic field values
        '''
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        prosptechused = self.configset.get('PROCESSING', 'prosptech')
        downsensoraltused = self.configset.getfloat('PROCESSING', 'downsensoraltitude')
        upsensoraltused = self.configset.getfloat('PROCESSING', 'upsensoraltitude')
        prosptechsim = self.configset.get('PROCESSING', 'prosptech')
        downsensoraltsim = self.configset.getfloat('PROCESSING', 'downsensoraltitude')
        upsensoraltsim = self.configset.getfloat('PROCESSING', 'upsensoraltitude')
        inclineangle = self.configset.getfloat('PROCESSING', 'maginclineangle')
        alphaangle = self.configset.getfloat('PROCESSING', 'magalphaangle')
        r, dialogbox = GradMagFieldConversionDlgBox.new(self.asciiset.getStringValue('GRADMAGFIELDCONV_ID'), self, prosptechused, prosptechsim, apod, downsensoraltused, upsensoraltused, downsensoraltsim, upsensoraltsim, inclineangle, alphaangle)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            self.configset.set('PROCESSING', 'prosptech', dialogbox.prosptechused)
            self.configset.set('PROCESSING', 'downsensoraltitude', str(dialogbox.downsensoraltused))
            self.configset.set('PROCESSING', 'upsensoraltitude', str(dialogbox.upsensoraltused))
            self.configset.set('PROCESSING', 'maginclineangle', str(dialogbox.inclineangle))
            self.configset.set('PROCESSING', 'magalphaangle', str(dialogbox.alphaangle))
            

    def eulerDeconvolution(self):
        '''
        Do the euler deconvolution
        '''
        apod = self.configset.getint('PROCESSING', 'apodisationfactor')
        nflag = self.configset.getboolean('PROCESSING', 'eulerstructindexflag')
        nvalue = self.configset.getint('PROCESSING', 'eulerstructindexvalue')
        r, dialogbox = EulerDeconvolutionDlgBox.new(self.asciiset.getStringValue('EULERDECONV_ID'), self, apod, nflag, nvalue)
        if (r == QtGui.QDialog.Accepted):
            self.dataset = dialogbox.dataset
            self.updateDisplay()
                            # updates config file
            self.configset.set('PROCESSING', 'apodisationfactor', str(dialogbox.apod))
            self.configset.set('PROCESSING', 'eulerstructindexflag', str(dialogbox.inclineangle))
            self.configset.set('PROCESSING', 'eulerstructindexvalue', str(dialogbox.alphaangle))
            

    def georeferenceDataSet(self):
        '''
        Georeferences the data set
        '''
        title = "Georeferencing " + self.title
        r, dlgbox = GeorefDlgBox.new(title, self, self.geopossetwindowslist)        
        if (r == QtGui.QDialog.Accepted):
            self.dataset.setgeoref(dlgbox.geoposset.refsystem, dlgbox.selectedpoints_list, dlgbox.geoposset.utm_letter, dlgbox.geoposset.utm_number)
            self.geopossetwindowslist[dlgbox.geopossetindex].geoposset = dlgbox.geoposset
            self.menubar.update()       # updates bar menu with enabled or disabled items



    def isGeoreferencingAvailable(self):
        '''
        Returns True if georeferencing is available
        '''
        if (len(self.geopossetwindowslist) > 0):    # if one or more geographic position set exist
            available = True                        # georeferencing is possible
        else:
            available = False                       # if not, georeferencing is not possible

        return available



    def isDatasetGeoreferenced(self):
        '''
        Returns Trus if data set georeferenced
        '''
        return self.dataset.georef.active

