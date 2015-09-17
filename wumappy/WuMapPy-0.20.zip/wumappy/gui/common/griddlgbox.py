# -*- coding: utf-8 -*-
'''
    wumappy.gui.common.griddlgbox
    -----------------------------

    Gridded dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Item():
    id = None       # item identifiant
    type = None     # item type, 'CheckBox', 'ComboBox', 'SpinBox', 'DoubleSpinBox', 'Label', 'ValidButton', 'CancelButton', 'MiscButton', ...
    init = None     # item init() function
    update = None   # item update() function
    


#---------------------------------------------------------------------------#
# Display Gridded Dialog Box Object                                          #
#---------------------------------------------------------------------------#
class GridDlgBox(QtGui.QDialog):
    
    def __init__(self, title, parent, it_list):
        '''
        Parameters :
        :title: title of dialog box
        :parent: parent windows object
        :it_list: list of items to add in the dialog box.
            [type, label, col_index, isavailable, init, update],... , with :
            :type: item type, 'CheckBox', 'ComboBox', 'SpinBox', 'Label', 'DoubleSpinBox', 'Slider', 'Carto', 'ValidButton', 'CancelButton', 'MiscButton', ...
            :label: item label.
            :row_index: index of the row to display item, 0,1, ...
            :col_index: index of the column to display item, 0,1, ...
            :isavailable: True if item is available, False if not.
            :init: initialisation function for item init(), 'None' if no function.
            :update: update function for item update(), 'None' if no function.
        '''
        super(GridDlgBox, self).__init__()

        self.asciiset = parent.asciiset
        self.icon = parent.icon
        self.items_list = []

        self.setWindowTitle(title)                  # sets the windows title
        self.setWindowIcon(self.icon)               # sets the window icon
        self.setFont(self.asciiset.font)

        self.layout = QtGui.QGridLayout()           # builds the main layout

        for it in it_list:
            item = Item()
            item.type = it[0]
            label = self.asciiset.getStringValue(it[1])
            row_index = it[2]
            col_index = it[3]
            isavailable = it[4]
            item.init = it[5]
            item.update = it[6]

            isValid = True
            if (item.type == 'CheckBox'):
                item.id = QtGui.QCheckBox(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'ComboBox'):
                item.id = QtGui.QComboBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'SpinBox'):
                item.id = QtGui.QSpinBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'DoubleSpinBox'):
                item.id = QtGui.QDoubleSpinBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Slider'):
                item.id = QtGui.QSlider()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Label'):
                item.id = QtGui.QLabel(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Image'):
                item.id = QtGui.QLabel(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'ValidButton'):
                item.id = QtGui.QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'CancelButton'):
                item.id = QtGui.QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'MiscButton'):
                item.id = QtGui.QPushButton("")
                item.id.setFont(self.asciiset.font)
            else:
                isValid = False

            if (isValid == True):
                self.items_list.append(item)

                if (item.init != None):                    
                    item.id = item.init(item.id)

                if (item.type == 'CheckBox'):
                    if (item.update != None):
                        item.id.stateChanged.connect(item.update)
                elif (item.type == 'ComboBox'):
                    if (item.update != None):
                        item.id.currentIndexChanged.connect(item.update)
                elif (item.type == 'SpinBox'):
                    if (item.update != None):
                        item.id.valueChanged.connect(item.update)
                elif (item.type == 'DoubleSpinBox'):
                    if (item.update != None):
                        item.id.valueChanged.connect(item.update)
                elif (item.type == 'Slider'):
                    if (item.update != None):
                        item.id.sliderReleased.connect(item.update)
                elif (item.type == 'ValidButton'):
                    item.id.clicked.connect(self.valid)
                elif (item.type == 'CancelButton'):
                    item.id.clicked.connect(self.cancel)
                elif (item.type == 'MiscButton'):
                    if (item.update != None):
                        item.id.clicked.connect(item.update)                    

                self.layout.addWidget(item.id, row_index, col_index)

        self.layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)    # to not authorize size modification
        self.setLayout(self.layout)



    def setValidButtonEnabled(self, enabled):
        '''
        Parameters:
        :enabled: True to enable valid button, False if not.
        '''
        self.okbuttonid.setEnabled(enabled)


    def valid(self):
        '''
        Closes the dialog box
        '''
        self.accept()
        self.close()        


    def cancel(self):
        '''
        Closes the dialog box
        '''
        self.close()
