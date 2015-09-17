# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.datasetinformationsdlgbox
    ---------------------------------------------

    Data set informations dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
import numpy as np
from wumappy.gui.common.griddlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Data set information Dialog Box Object                                    #
#---------------------------------------------------------------------------#
class DatasetInformationsDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent):
        '''
        '''
        
        window = cls()
        window.title = title
        window.interpgridding = parent.dataset.info.gridding_interpolation
        window.stepxgridding = parent.dataset.info.x_gridding_delta
        window.stepygridding = parent.dataset.info.y_gridding_delta
        window.icon = parent.icon
        window.items_list = [['Label', 'STEPXGRIDDING_ID', 0, 0, False, None, None],
                           ['DoubleSpinBox', '', 0, 1, True, window.GriddingXStepInit, None],  
                           ['Label', 'STEPYGRIDDING_ID', 1, 0, False, None, None], 
                           ['DoubleSpinBox', '', 1, 1, True, window.GriddingYStepInit, None],  
                           ['Label', 'INTERPOLATION_ID', 2, 0, False, None, None],  
                           ['ComboBox', '', 2, 1, True, window.GriddingInterpolationInit, None]]

        dlgbox = GridDlgBox(title, parent, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def GriddingXStepInit(self, id=None):
        if (id != None):
            id.setValue(self.stepxgridding)
            id.setEnabled(False)
        self.GriddingXStepId = id
        return id


    def GriddingYStepInit(self, id=None):
        if (id != None):
            id.setValue(self.stepygridding)
            id.setEnabled(False)
        self.GriddingYStepId = id
        return id

    
    def GriddingInterpolationInit(self, id=None):
                                                    # building of the "interpolation" field to select in a list
        interpolation_list = griddinginterpolation_getlist()

        try:
            interpolation_index = interpolation_list.index(self.interpgridding)
        except:
            interpolation_index = 0
            
        if (id != None):
            id.addItems(interpolation_list)
            id.setCurrentIndex(interpolation_index)
            id.setEnabled(False)
        self.GriddingInterpolationId = id
        return id




