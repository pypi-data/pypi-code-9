# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.ploughfiltdlgbox
    ------------------------------------

    Anti-Plough filtering dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Anti-Plough Filtering Dialog Box Object                                   #
#---------------------------------------------------------------------------#
class PloughFiltDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, nxsize=3, nysize=3, apod=0, angle=None, cutoff=None):
        '''
        '''
        
        window = cls()
        window.parent = parent
        window.dataset = parent.dataset
        window.originaldataset = parent.dataset
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.zmin = window.parent.zmin
        window.zmax = window.parent.zmax
        zmin, zmax = window.dataset.histo_getlimits()
        if (window.zmin == None):
            window.zmin = zmin
        if (window.zmax == None):
            window.zmax = zmax            

        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')
        window.nxsize = nxsize
        window.nysize = nysize
        window.apodisationfactor = apod
        window.angle = angle
        window.cutoff = cutoff
        window.items_list = [['Label', 'FILTERNXSIZE_ID', 0, 0, False, None, None],  
                           ['SpinBox', '', 1, 0, True, window.NxSizeInit, window.NxSizeUpdate],    
                           ['Label', 'FILTERNYSIZE_ID', 2, 0, False, None, None],  
                           ['SpinBox', '', 3, 0, True, window.NySizeInit, window.NySizeUpdate],    
                           ['Label', '', 4, 0, False, None, None],  
                           ['Label', 'APODISATIONFACTOR_ID', 5, 0, False, None, None],  
                           ['SpinBox', '', 6, 0, True, window.ApodisationFactorInit, window.ApodisationFactorUpdate],    
                           ['Label', '', 7, 0, False, None, None],  
                           ['Label', 'PLOUGHANGLE_ID', 8, 0, False, None, None],  
                           ['DoubleSpinBox', '', 9, 0, True, window.AngleInit, window.AngleUpdate],    
                           ['Label', '', 10, 0, False, None, None],  
                           ['Label', 'PLOUGHCUTOFF_ID', 11, 0, False, None, None],  
                           ['DoubleSpinBox', '', 12, 0, True, window.CutOffInit, window.CutOffUpdate],    
                           ['Label', '', 13, 0, False, None, None],  
                           ['MiscButton', 'DISPUPDATE_ID', 14, 0, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate],   
                           ['ValidButton', 'VALID_ID', 15, 0, True, window.ValidButtonInit, None],   
                           ['CancelButton', 'CANCEL_ID', 16, 0, True, window.CancelButtonInit, None],   
                           ['Image', '', 0, 1, False, window.CartoImageInit, None]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def NxSizeInit(self, id=None):
        if (id != None):
            id.setRange(0, 100)
            id.setValue(self.nxsize)
        self.NxSizeId = id
        return id


    def NxSizeUpdate(self):
        self.nxsize = self.NxSizeId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def NySizeInit(self, id=None):
        if (id != None):
            id.setRange(0, 100)
            id.setValue(self.nysize)
        self.NySizeId = id
        return id


    def NySizeUpdate(self):
        self.nysize = self.NySizeId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def NxSizeInit(self, id=None):
        if (id != None):
            id.setRange(0, 100)
            id.setValue(self.nxsize)
        self.NxSizeId = id
        return id


    def NxSizeUpdate(self):
        self.nxsize = self.NxSizeId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ApodisationFactorInit(self, id=None):
        if (id != None):
            id.setRange(0, 25)
            id.setSingleStep(5)
            id.setValue(self.apodisationfactor)
        self.ApodisationFactorId = id
        return id


    def ApodisationFactorUpdate(self):
        self.apodisationfactor = self.ApodisationFactorId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def AngleInit(self, id=None):
        if (id != None):
            id.setRange(0, 359.9)
            id.setValue(self.angle)
        self.AngleId = id
        return id


    def AngleUpdate(self):
        self.angle = self.AngleId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def CutOffInit(self, id=None):
        if (id != None):
            id.setRange(0, 10000.0)
            id.setValue(self.cutoff)
        self.CutOffId = id
        return id


    def CutOffUpdate(self):
        self.cutoff = self.CutOffId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def DispUpdateButtonInit(self, id=None):
        self.DispUpdateButtonId = id
        id.setHidden(self.realtimeupdateflag)       # Hides button if real time updating activated
        id.setEnabled(False)                        # disables the button , by default
        return id


    def DispUpdateButtonUpdate(self):
        self.CartoImageUpdate()                     # updates carto image
        

    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


    def CartoImageInit(self, id=None):
        self.cartofig = None
        self.CartoImageId = id
        self.CartoImageUpdate()
        return id


    def CartoImageUpdate(self):
        initcursor = self.wid.cursor()                                  # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                        # sets the wait cursor

        # processes data set
        self.dataset = self.originaldataset.copy()
        self.dataset.ploughfilt(self.nxsize, self.nysize, self.apodisationfactor, self.angle, self.cutoff)

        # plots geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=self.zmin, cmmax=self.zmax, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
        cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button

        self.wid.setCursor(initcursor)                                  # resets the init cursor
        
