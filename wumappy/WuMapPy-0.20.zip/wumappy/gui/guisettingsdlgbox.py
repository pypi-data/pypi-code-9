# -*- coding: utf-8 -*-
'''
    wumappy.gui.guisettingsdlgbox
    -----------------------------

    Graphical User Interface settings dialog box management.

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
# GUI Settings Dialog Box Object                                            #
#---------------------------------------------------------------------------#
class GuiSettingsDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent):
        '''
        '''
        
        window = cls()
        window.title = title
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.items_list = [['CheckBox', 'RTUPDATE_ID', 0, 0, True, window.RealTimeUpdateInit, window.RealTimeUpdateUpdate],
                           ['ValidButton', 'VALID_ID', 1, 1, True, window.ValidButtonInit, None],   
                           ['CancelButton', 'CANCEL_ID', 1, 0, True, window.CancelButtonInit, None]]
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')

        dlgbox = GridDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def RealTimeUpdateInit(self, id=None):
        if (id != None):
            id.setChecked(self.realtimeupdateflag)
        self.RealTimeUpdateId = id
        return id


    def RealTimeUpdateUpdate(self):
        self.realtimeupdateflag = self.RealTimeUpdateId.isChecked()


    def ValidButtonInit(self, id=None):
        self.ValidButtonId = id
        return id


    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


