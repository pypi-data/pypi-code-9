# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.festoonfiltdlgbox
    -------------------------------------

    Festoon filtering dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
import numpy as np
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Festoon Filtering Dialog Box Object                                       #
#---------------------------------------------------------------------------#
class FestoonFiltDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, method='Pearson', shift=0):
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
        window.method = method
        window.shift = shift
        window.items_list = [['Label', '', 0, 0, False, None, None],
                           ['Label', 'FESTOONFILTMETHOD_ID', 1, 0, False, None, None],  
                           ['ComboBox', '', 2, 0, True, window.MethodInit, window.MethodUpdate],    
                           ['Label', 'FESTOONFILTSHIFT_ID', 3, 0, False, None, None],  
                           ['SpinBox', '', 4, 0, True, window.ShiftInit, window.ShiftUpdate],    
                           ['Label', 'CORRELATIONMAP_ID', 6, 0, False, None, None],  
                           ['Image', '', 7, 0, False, window.CorrMapImageInit, None],   
                           ['Label', 'CORRELATIONSUM_ID', 8, 0, False, None, None],  
                           ['Image', '', 9, 0, False, window.CorrSumImageInit, None],   
                           ['MiscButton', 'DISPUPDATE_ID', 10, 0, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate],   
                           ['ValidButton', 'VALID_ID', 11, 0, True, window.ValidButtonInit, None],   
                           ['CancelButton', 'CANCEL_ID', 12, 0, True, window.CancelButtonInit, None],   
                           ['Image', '', 0, 1, False, window.CartoImageInit, None]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def MethodInit(self, id=None):                                                  
        method_list = festooncorrelation_getlist()
        try:
            method_index = method_list.index(self.method)
        except:
            method_index = 0
            
        if (id != None):
            id.addItems(method_list)
            id.setCurrentIndex(method_index)
        self.MethodId = id
        return id


    def MethodUpdate(self):
        self.method = self.MethodId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ShiftInit(self, id=None):
        if (id != None):
                                                    
            range = (self.dataset.info.y_max - self.dataset.info.y_min)/2
            id.setRange(-range, +range)
            id.setValue(self.shift)
        self.ShiftId = id
        return id


    def ShiftUpdate(self):
        self.shift = self.ShiftId.value()
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


    def CorrMapImageInit(self, id=None):
        self.CorrMapImageId = id
        self.corrmapfig = None
        return id


    def CorrMapImageUpdate(self):
        self.corrmapfig = self.dataset.correlation_plotmap(fig=self.corrmapfig)
        pixmap = QtGui.QPixmap.grabWidget(self.corrmapfig.canvas)   # builds the pixmap from the canvas
        pixmap = pixmap.scaledToWidth(400)
        self.CorrMapImageId.setPixmap(pixmap)
        

    def CorrSumImageInit(self, id=None):
        self.CorrSumImageId = id
        self.corrsumfig = None
        return id


    def CorrSumImageUpdate(self):
        self.corrsumfig = self.dataset.correlation_plotsum(fig=self.corrsumfig)
        pixmap = QtGui.QPixmap.grabWidget(self.corrsumfig.canvas)   # builds the pixmap from the canvas
        pixmap = pixmap.scaledToWidth(400)
        self.CorrSumImageId.setPixmap(pixmap)
        

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
        self.shift = self.dataset.festoonfilt(self.method, self.shift)

        # plots geophysical image
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, interpolation=self.parent.interpolation, cmmin=None, cmmax=None, cmapdisplay = True, axisdisplay = True, logscale=self.parent.colorbarlogscaleflag)        
        cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        self.CartoImageId.setPixmap(cartopixmap)
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        self.ValidButtonId.setEnabled(True)                             # enables the valid button
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button

        self.CorrSumImageUpdate()
        self.CorrMapImageUpdate()
        self.ShiftId.setValue(self.shift)

        self.wid.setCursor(initcursor)                                  # resets the init cursor
        
