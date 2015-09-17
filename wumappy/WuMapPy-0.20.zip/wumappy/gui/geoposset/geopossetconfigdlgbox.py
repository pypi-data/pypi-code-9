# -*- coding: utf-8 -*-
'''
    wumappy.gui.geopossetconfigdlgbox
    ---------------------------------

    Configuring geographics positions set dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from geophpy.geoposset import *
from copy import deepcopy
from PySide import QtCore, QtGui
import os
import numpy as np
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Configuring Geoposset Dialog Box Object                                       #
#---------------------------------------------------------------------------#
class ConfigGeopossetDlgBox(object):
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent=None):
        '''
        '''
        
        window = cls()
        window.title = title
        window.cartofig = None
        window.parent = parent
        window.asciiset = parent.asciiset
        window.icon = parent.icon
        window.fig = None
        window.pointindex = 0
        window.geoposset = deepcopy(parent.geoposset)
                
        window.items_list = [['Label', 'POINTNUM_ID', 0, 0, False, None, None],  
                           ['ComboBox', '', 1, 0, True, window.PointNumInit, window.PointNumUpdate], 
                           ['CheckBox', 'POINTXYCONVERTED_ID', 2, 0, True, window.PointXYActivationInit, window.PointXYActivationUpdate], 
                           ['Label', 'POINTX_ID', 3, 0, False, window.PointXLabelInit, None],   
                           ['DoubleSpinBox', '', 4, 0, True, window.PointXInit, window.PointXUpdate], 
                           ['Label', 'POINTY_ID', 5, 0, False, window.PointYLabelInit, None],   
                           ['DoubleSpinBox', '', 6, 0, True, window.PointYInit, window.PointYUpdate], 
                           ['ValidButton', 'VALID_ID', 7, 0, True, window.ValidButtonInit, None],   
                           ['CancelButton', 'CANCEL_ID', 8, 0, True, window.CancelButtonInit, None],
                           ['TextEdit', '', 0, 1, True, window.PointsListInit, None]]
        
        dlgbox = CartoDlgBox(window.title, window, window.items_list) # self.wid est construit dans CartoDlgBox
        dlgbox.exec()

        return dlgbox.result(), window


    def PointNumInit(self, id=None):
        for point in self.geoposset.points_list:
            id.addItem(str(point[0]))
        id.setCurrentIndex(self.pointindex)
        self.PointNumId = id
        return id


    def PointNumUpdate(self):
        self.pointindex = self.PointNumId.currentIndex()
        if ((self.geoposset.points_list[self.pointindex][3] != None) and (self.geoposset.points_list[self.pointindex][4] != None)):
            self.PointXId.setValue(self.geoposset.points_list[self.pointindex][3])
            self.PointYId.setValue(self.geoposset.points_list[self.pointindex][4])
            self.PointXYActivationId.setChecked(True)
        else:
            self.PointXYActivationId.setChecked(False)
        
    
    def PointXYActivationInit(self, id=None):
        self.PointXYActivationId = id
        return id


    def PointXYActivationUpdate(self):
        activ = self.PointXYActivationId.isChecked()
        self.PointXId.setEnabled(activ)
        self.PointXLabelId.setEnabled(activ)
        self.PointYId.setEnabled(activ)
        self.PointYLabelId.setEnabled(activ)
        self.PointsListUpdate()
        if (activ == False):
            x = y = None
        else :
            x = self.PointXId.value()
            y = self.PointYId.value()
        self.geoposset.points_list[self.pointindex][3] = x
        self.geoposset.points_list[self.pointindex][4] = y
        self.PointsListUpdate()
        

    def PointXLabelInit(self, id=None):
        self.PointXLabelId = id
        return id


    def PointXInit(self, id=None):
        id.setRange(-10000, 10000)
        self.PointXId = id
        return id


    def PointXUpdate(self):
        x = self.PointXId.value()
        self.geoposset.points_list[self.pointindex][3] = x
        self.PointsListUpdate()
        

    def PointYLabelInit(self, id=None):
        self.PointYLabelId = id
        return id


    def PointYInit(self, id=None):
        id.setRange(-10000, 10000)
        self.PointYId = id
        return id


    def PointYUpdate(self):
        y = self.PointYId.value()
        self.geoposset.points_list[self.pointindex][4] = y
        self.PointsListUpdate()
        

    def PointsListInit(self, id=None):
        self.PointsListId = id
        id.setReadOnly(True)
        self.PointsListUpdate()
        self.PointNumUpdate()
        self.PointXYActivationUpdate()
        return id


    def PointsListUpdate(self):
        szPointNum = self.asciiset.getStringValue('POINTNUM_ID')
        szPointLon = self.asciiset.getStringValue('POINTLONGITUDE_ID')
        szPointLat = self.asciiset.getStringValue('POINTLATITUDE_ID')
        szPointX = self.asciiset.getStringValue('POINTX_ID')
        szPointY = self.asciiset.getStringValue('POINTY_ID')
        self.PointsListId.setText("%s\t%s\t%s\t%s\t%s"%(szPointNum, szPointLon, szPointLat, szPointX, szPointY))
        maxwidth = 0
        for point in self.geoposset.points_list:
            line = "%s\t%s\t%s\t%s\t%s"%(point[0], point[1], point[2], point[3], point[4])
            self.PointsListId.append(line)
            width = self.PointsListId.fontMetrics().boundingRect(line).width()
            if (width > maxwidth):
                maxwidth = width
        self.PointsListId.setMinimumWidth(1.5*maxwidth)


    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


