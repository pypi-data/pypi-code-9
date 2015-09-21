
# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
add label, slider, value to a QGridLayout

Coordinate the action of a slider with the topic value::

  label   value   slider                 
  bio     0.7     -|---|---|---|[-]|---|-
  phys    0.2     -|--[|]--|---|---|---|-

======  =========  ====================================================
widget  type       description
======  =========  ====================================================
label   QLabel     mnemonic name (no white space)
value   QLineEdit  string with floating point value: 0 <= value <= 1.0
slider  QSlider    graphical adjustment of value
======  =========  ====================================================

These three widgets will be added to the *parent* widget,
assumed to be on the same row of a QGridLayout.

A *topic* (known here as *label*) is some scientific area 
of interest to the PRP.
Such as, for the SAXS review panel, some of the proposals
are for XPCS (X-ray Photon Correlation Spectroscopy).

Each proposal will have a strength value assigned for
each topic, indicating how important that topic is to the
proposed experiment.

Each reviewer will have a strength value assigned for
each topic, indicating the strength of that reviewer 
in the particular topic.

---------
'''


import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import history
import traceback


class AGUP_TopicSlider(QtCore.QObject):
    '''add topic, slider, value_entry to a QGridLayout'''
    
    def __init__(self, parent, row, label, value):
        QtCore.QObject.__init__(self)
        self.slider_factor = 100    # slider = int(slider_factor * value_widget + 0.5)

        self.slider = QtGui.QSlider(
                                value=int(self.slider_factor*value),
                                maximum=self.slider_factor,
                                pageStep=10,
                                tracking=False,
                                orientation=QtCore.Qt.Horizontal,
                                tickPosition=QtGui.QSlider.TicksAbove,  # looks like a user preference
                                #tickPosition=QtGui.QSlider.TicksBothSides,
                                #tickPosition=QtGui.QSlider.TicksBelow,
                                #tickPosition=QtGui.QSlider.NoTicks,
                                tickInterval=20
                               )

        self.value_widget = QtGui.QLineEdit(str(value))
        self.value_widget.setMaximumWidth(self.slider_factor)
        
        self.label = label
        self.parent = parent
        self.value = value

        parent.addWidget(QtGui.QLabel(label), row, 0)
        parent.addWidget(self.value_widget, row, 1)
        parent.addWidget(self.slider, row, 2)
        
        # connect slider changes with value_widget and vice versa
        self.slider.valueChanged.connect(self.onSliderChange)
        self.slider.sliderMoved.connect(self.onSliderChange)
        self.value_widget.textEdited.connect(self.onValueChange)
    
    def onSliderChange(self, value):
        self.setValue(str(value / float(self.slider_factor)))
    
    def onValueChange(self, value):
        if value == '.':
            value = 0
        try:
            float_value = float(value)
            if 0 <= float_value <= 1.0:
                self.setSliderValue(int(float_value*self.slider_factor + .5))
        except ValueError, exc:
            history.addLog('problem with Topic: ' + str(self.label))
            history.addLog(traceback.format_exc())

    def getValue(self):
        # if can't convert, get value from slider
        try:
            value = float(self.value_widget.text())
        except ValueError, exc:
            value = self.getSliderValue() / float(self.slider_factor)
        return value
    
    def setValue(self, value):
        '''
        set strength of this topic (0:low, 1.0: high)
        
        :param int value: 0 <= value <= 100
        
        This routine sets the slider value.
        '''
        self.value_widget.setText(str(value))
    
    def getSliderValue(self):
        value = self.slider.value()
        return value
    
    def setSliderValue(self, value):
        '''
        set value of the slider indicating strength of this topic (0:low, 100: high)
        
        :param int value: 0 <= value <= 100
        
        This routine sets the text value.
        '''
        self.slider.setValue(value)
