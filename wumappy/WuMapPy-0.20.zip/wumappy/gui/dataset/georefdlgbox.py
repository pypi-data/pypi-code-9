# -*- coding: utf-8 -*-
'''
    wumappy.gui.georefdlgbox
    ---------------------------------

    Georeferencing data set dialog box management.

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
from copy import deepcopy
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Georeferencing data set Dialog Box Object                                 #
#---------------------------------------------------------------------------#
class GeorefDlgBox(object):
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent=None, geopossetwindowslist=None):
        '''
        '''
        
        window = cls()
        window.title = title
        window.cartofig = None
        window.parent = parent
        window.asciiset = parent.asciiset
        window.dataset = deepcopy(parent.dataset)
        window.icon = parent.icon
        window.fig = None
        window.geopossetindex = 0
        window.pointindex = 0
        window.geopossetwindowslist = geopossetwindowslist
        window.selectedpoints_list = []
        window.geoposset = deepcopy(window.geopossetwindowslist[window.geopossetindex].geoposset)
                
        window.items_list = [['Label', 'GEOPOSSET_ID', 0, 0, False, None, None],  
                           ['ComboBox', '', 1, 0, True, window.GeoPosSetSelectInit, window.GeoPosSetSelectUpdate], 
                           ['Label', 'POINTNUM_ID', 2, 0, False, None, None],  
                           ['ComboBox', '', 3, 0, True, window.PointNumInit, window.PointNumUpdate], 
                           ['CheckBox', 'POINTSELECTED_ID', 4, 0, True, window.PointSelectionFlagInit, window.PointSelectionFlagUpdate], 
                           ['Label', 'POINTX_ID', 5, 0, False, window.PointXLabelInit, None],   
                           ['DoubleSpinBox', '', 6, 0, True, window.PointXInit, window.PointXUpdate], 
                           ['Label', 'POINTY_ID', 7, 0, False, window.PointYLabelInit, None],   
                           ['DoubleSpinBox', '', 8, 0, True, window.PointYInit, window.PointYUpdate], 
                           ['ValidButton', 'VALID_ID', 9, 0, True, window.ValidButtonInit, None],   
                           ['CancelButton', 'CANCEL_ID', 10, 0, True, window.CancelButtonInit, None],
                           ['Label', '', 1, 1, True, window.GeoRefStatusInit, None],
                           ['TextEdit', '', 0, 1, True, window.PointsListInit, None]]
        
        dlgbox = CartoDlgBox(window.title, window, window.items_list) # self.wid est construit dans CartoDlgBox
        dlgbox.exec()

        return dlgbox.result(), window


    def GeoPosSetSelectInit(self, id=None):
        
        for geopossetwindow in self.geopossetwindowslist:
            id.addItem(geopossetwindow.title)
        id.setCurrentIndex(self.geopossetindex)
        self.GeoPosSetSelectId = id
        return id


    def GeoPosSetSelectUpdate(self):
        self.geopossetindex = self.GeoPosSetSelectId.currentIndex()
        self.geoposset = self.geopossetwindowslist[self.geopossetindex].geoposset
        self.PointNumReset()
        self.PointsListUpdate()
        
    
    def PointNumInit(self, id=None):
        self.PointNumId = id
        self.PointNumReset()
        return id


    def PointNumReset(self):
        self.PointNumId.clear()
        for point in self.geoposset.points_list:
            self.PointNumId.addItem(str(point[0]))
        self.PointNumId.setCurrentIndex(self.pointindex)


    def PointNumUpdate(self):
        self.pointindex = self.PointNumId.currentIndex()
        if ((self.geoposset.points_list[self.pointindex][3] != None) and (self.geoposset.points_list[self.pointindex][4] != None)):
            self.PointXId.setValue(self.geoposset.points_list[self.pointindex][3])
            self.PointYId.setValue(self.geoposset.points_list[self.pointindex][4])
            self.PointSelectionFlagId.setChecked(True)
        else:
            self.PointSelectionFlagId.setChecked(False)
        
    
    def PointSelectionFlagInit(self, id=None):
        self.PointSelectionFlagId = id
        return id


    def PointSelectionFlagUpdate(self):
        activ = self.PointSelectionFlagId.isChecked()
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
        self.PointSelectionFlagUpdate()
        return id


    def PointsListUpdate(self):
        szPointNum = self.asciiset.getStringValue('POINTNUM_ID')
        szPointLon = self.asciiset.getStringValue('POINTLONGITUDE_ID')
        szPointLat = self.asciiset.getStringValue('POINTLATITUDE_ID')
        szPointX = self.asciiset.getStringValue('POINTX_ID')
        szPointY = self.asciiset.getStringValue('POINTY_ID')
        self.PointsListId.setText("%s\t%s\t%s\t%s\t%s"%(szPointNum, szPointLon, szPointLat, szPointX, szPointY))
        maxwidth = 0
        self.selectedpoints_list = []
        for point in self.geoposset.points_list:
            line = "%s\t%s\t%s\t%s\t%s"%(point[0], point[1], point[2], point[3], point[4])
            self.PointsListId.append(line)
            width = self.PointsListId.fontMetrics().boundingRect(line).width()
            if (width > maxwidth):
                maxwidth = width
            if ((point[3] != None) and (point[4] != None)):
                self.selectedpoints_list.append(point)
        self.PointsListId.setMinimumWidth(1.5*maxwidth)
        self.selectedpoints_list = np.array(self.selectedpoints_list)
        if (len(self.selectedpoints_list) < 4):
            errormsg = self.asciiset.getStringValue('GEOREFERROR1_MSG')
        else :
            errormsg = ''            
        self.GeoRefStatusId.setText(errormsg)
        self.ValidButtonId.setEnabled(self.dataset.setgeoref(self.geoposset.refsystem, self.selectedpoints_list, self.geoposset.utm_letter, self.geoposset.utm_number) == 0)
     

    def GeoRefStatusInit(self, id=None):
        self.GeoRefStatusId = id
        return id
        

    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


