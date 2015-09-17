# -*- coding: utf-8 -*-
'''
    wumappy.gui.opendatasetdlgbox
    -----------------------------

    Opening dataset dialog box management.

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
# Opening Dataset Dialog Box Object                                         #
#---------------------------------------------------------------------------#
class OpenDatasetDlgBox(object):
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, filenames, parent=None, xcolnum=1, ycolnum=2, zcolnum=3, delimiter='\t', fileformat='ascii', delimitersasuniqueflag=True, skiprows=1, fieldsrow=0, interpgridding = 'nearest', stepxgridding = None, stepygridding = None, autogriddingflag = True, dispgriddingflag = True, festoonfiltflag = False, festoonfiltmethod = 'Pearson', festoonfiltshift = 0, colormap = "Greys", reverseflag = False, peakfiltflag = False, nanreplacedflag=False, medianreplacedflag=False, medianfiltflag = False, nxsize=3, nysize=3, percent=0, gap=0):
        '''
        '''
        
        window = cls()
        window.title = title
        window.delimiter = delimiter
        window.fileformat = fileformat
        window.delimitersasuniqueflag = delimitersasuniqueflag
        window.x_colnum = xcolnum
        window.y_colnum = ycolnum
        window.z_colnum = zcolnum
        window.skiprows = skiprows
        window.fieldsrow = fieldsrow
        window.filenames = filenames
        window.cartofig = None
        window.stepxgridding = stepxgridding
        window.stepygridding = stepygridding
        window.interpgridding = interpgridding
        window.stepxgridding_firstime = True
        window.stepygridding_firstime = True
        window.parent = parent
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')                                                                
        window.autogriddingflag = autogriddingflag
        window.dispgriddingflag = dispgriddingflag
        window.festoonfiltflag = festoonfiltflag
        window.festoonfiltmethod = festoonfiltmethod
        window.festoonfiltshift = festoonfiltshift
        window.valfiltflag = False
        window.dataset = None
        window.colormap = colormap
        window.reverseflag = reverseflag
        window.colorbarlogscaleflag = False
        window.automaticrangeflag = True
        window.peakfiltflag = peakfiltflag
        window.nanreplacedflag = nanreplacedflag
        window.medianreplacedflag = medianreplacedflag
        window.medianfiltflag = medianfiltflag
        window.nxsize = nxsize
        window.nysize = nysize
        window.percent = percent
        window.gap = gap
        window.histofig = None
                
        window.items_list = [['Label', '', 0, 0, False, window.FileNamesInit, None], \
                           ['Label', '', 1, 0, False, None, None],  \
                           ['Label', 'FILEFORMAT_ID', 2, 0, False, None, None], \
                           ['ComboBox', '', 3, 0, True, window.FileFormatInit, window.FileFormatUpdate],   \
                           ['Label', 'DELIMITER_ID', 4, 0, False, None, None],  \
                           ['ComboBox', '', 5, 0, True, window.DelimiterInit, window.DelimiterUpdate], \
                           ['CheckBox', 'DELIMITERSASUNIQUEFLAG_ID', 6, 0, False, window.SeveralsDelimitersAsUniqueInit, window.SeveralsDelimitersAsUniqueUpdate],  \
                           ['Label', '', 7, 0, False, None, None],  \
                           ['Label', 'SKIPROWS_ID', 8, 0, False, None, None],   \
                           ['SpinBox', '', 9, 0, True, window.SkipRowsNumberInit, window.SkipRowsNumberUpdate], \
                           ['Label', 'FIELDSROW_ID', 10, 0, False, None, None],   \
                           ['SpinBox', '', 11, 0, True, window.FieldsRowIndexInit, window.FieldsRowIndexUpdate], \
                           ['Label', '', 12, 0, False, None, None],  \
                           ['Label', 'XCOLNUM_ID', 13, 0, False, None, None],   \
                           ['SpinBox', '', 14, 0, True, window.XColumnInit, window.XColumnUpdate],    \
                           ['Label', 'YCOLNUM_ID', 15, 0, False, None, None],   \
                           ['SpinBox', '', 16, 0, True, window.YColumnInit, window.YColumnUpdate],    \
                           ['Label', 'ZCOLNUM_ID', 17, 0, False, None, None],   \
                           ['SpinBox', '', 18, 0, True, window.ZColumnInit, window.ZColumnUpdate],    \
                           ['Label', 'STEPXGRIDDING_ID', 0, 1, False, window.GriddingXStepLabelInit, None],    \
                           ['DoubleSpinBox', '', 1, 1, True, window.GriddingXStepInit, window.GriddingXStepUpdate],  \
                           ['Label', 'STEPYGRIDDING_ID', 2, 1, False, window.GriddingYStepLabelInit, None], \
                           ['DoubleSpinBox', '', 3, 1, True, window.GriddingYStepInit, window.GriddingYStepUpdate],  \
                           ['Label', '', 4, 1, False, window.GriddingSizeInit, None],  \
                           ['CheckBox', 'AUTOGRIDDINGFLAG_ID', 5, 1, True, window.GriddingAutoInit, window.GriddingAutoUpdate], \
                           ['Label', 'INTERPOLATION_ID', 6, 1, False, None, None],  \
                           ['ComboBox', '', 7, 1, True, window.GriddingInterpolationInit, window.GriddingInterpolationUpdate], \
                           ['Label', 'COLORMAP_ID', 8, 1, False, None, None],   
                           ['ComboBox', '', 9, 1, True, window.ColorMapInit, window.ColorMapUpdate], 
                           ['CheckBox', 'REVERSEFLAG_ID', 10, 1, True, window.ColorMapReverseInit, window.ColorMapReverseUpdate],  
                           ['CheckBox', 'COLORBARLOGSCALEFLAG_ID', 11, 1, True, window.ColorBarLogScaleInit, window.ColorBarLogScaleUpdate],   
                           ['CheckBox', 'DISPGRIDDINGFLAG_ID', 12, 1, True, window.GriddingPointsDisplayInit, window.GriddingPointsDisplayUpdate], \
                           ['Label', 'MINIMALVALUE_ID', 13, 1, False, None, None],  
                           ['SpinBox', '', 14, 1, True, window.MinimalValuebySpinBoxInit, window.MinimalValuebySpinBoxUpdate],    
                           ['Slider', '', 15, 1, True, window.MinimalValuebySliderInit, window.MinimalValuebySliderUpdate],  
                           ['Label', 'MAXIMALVALUE_ID', 16, 1, False, None, None],  
                           ['SpinBox', '', 17, 1, True, window.MaximalValuebySpinBoxInit, window.MaximalValuebySpinBoxUpdate],    
                           ['Slider', '', 18, 1, True, window.MaximalValuebySliderInit, window.MaximalValuebySliderUpdate],
                           ['CheckBox', 'PEAKFILT_ID', 0, 2, True, window.PeakFiltInit, window.PeakFiltUpdate],  \
                           ['CheckBox', 'NANREPLACEDFLAG_ID', 1, 2, True, window.NanReplacedValuesInit, window.NanReplacedValuesUpdate],  
                           ['CheckBox', 'MEDIANREPLACEDFLAG_ID', 2, 2, True, window.MedianReplacedValuesInit, window.MedianReplacedValuesUpdate],  
                           ['Label', '', 3, 2, False, None, None],  \
                           ['CheckBox', 'MEDIANFILT_ID', 4, 2, True, window.MedianFiltInit, window.MedianFiltUpdate],  \
                           ['Label', 'FILTERNXSIZE_ID', 5, 2, False, window.NxSizeLabelInit, None],  
                           ['SpinBox', '', 6, 2, True, window.NxSizeInit, window.NxSizeUpdate],    
                           ['Label', 'FILTERNYSIZE_ID', 7, 2, False, window.NySizeLabelInit, None],  
                           ['SpinBox', '', 8, 2, True, window.NySizeInit, window.NySizeUpdate],    
                           ['Label', 'MEDIANFILTERPERCENT_ID', 9, 2, False, window.PercentLabelInit, None],  
                           ['SpinBox', '', 10, 2, True, window.PercentInit, window.PercentUpdate],    
                           ['Label', 'MEDIANFILTERGAP_ID', 11, 2, False, window.GapLabelInit, None],  
                           ['SpinBox', '', 12, 2, True, window.GapInit, window.GapUpdate],
                           ['Label', '', 13, 2, False, None, None],  \
                           ['CheckBox', 'FESTOONFILT_ID', 14, 2, True, window.FestoonFiltInit, window.FestoonFiltUpdate],  \
                           ['Label', 'FESTOONFILTMETHOD_ID', 15, 2, False, window.FestoonMethodLabelInit, None],  \
                           ['ComboBox', '', 16, 2, True, window.FestoonMethodInit, window.FestoonMethodUpdate],    \
                           ['Label', 'FESTOONFILTSHIFT_ID', 17, 2, False, window.FestoonShiftLabelInit, None],  \
                           ['SpinBox', '', 18, 2, True, window.FestoonShiftInit, window.FestoonShiftUpdate],    \
                           ['MiscButton', 'DISPUPDATE_ID', 20, 2, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate],   \
                           ['ValidButton', 'VALID_ID', 20, 1, True, window.ValidButtonInit, None],   \
                           ['CancelButton', 'CANCEL_ID', 20, 0, True, window.CancelButtonInit, None],   \
                           ['Image', '', 19, 1, False, window.HistoImageInit, None],   
                           ['Image', '', 1, 3, False, window.CartoImageInit, None]]
        
        dlgbox = CartoDlgBox("Open dataset", window, window.items_list) # self.wid est construit dans CartoDlgBox
        dlgbox.exec()

        return dlgbox.result(), window


    def FileNamesInit(self, id=None):
        filenames=""
        n = len(self.filenames)
        for i in range(n):
            filenames = filenames + self.filenames[i]
            if (i<(n-1)):
                filenames = filenames + '\n'
        id.setText(filenames)
        return id


    def FileFormatInit(self, id=None):
        formatlist = fileformat_getlist()
        id.addItems(formatlist)
        index = id.findText(self.fileformat)
        id.setCurrentIndex(index)
        self.FileFormatId = id
        return id


    def FileFormatUpdate(self):
        self.fileformat = self.FileFormatId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True
        
    
    def DelimiterInit(self, id=None):
        id.addItems(['.', ',', ';', 'space', 'tab', '-'])
        if (self.delimiter == ' '):
            delimiter = 'space'
        elif (self.delimiter == '\t'):
            delimiter = 'tab'
        else:
            delimiter = self.delimiter
        index = id.findText(delimiter)
        id.setCurrentIndex(index)
        self.DelimiterId = id
        return id


    def DelimiterUpdate(self):
        self.delimiter = self.DelimiterId.currentText()
        if (self.delimiter == 'space'):
            self.delimiter = ' '
        elif (self.delimiter == 'tab'):
            self.delimiter = '\t'
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True


    def SeveralsDelimitersAsUniqueInit(self, id=None):
        id.setChecked(self.delimitersasuniqueflag)
        self.SeveralsDelimiterAsUniqueId = id
        return id


    def SeveralsDelimitersAsUniqueUpdate(self):
        self.delimitersasuniqueflag = self.SeveralsDelimiterAsUniqueId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def SkipRowsNumberInit(self, id=None):
        id.setValue(self.skiprows)
        self.SkipRowsNumberId = id
        return id


    def SkipRowsNumberUpdate(self):
        self.skiprows = self.SkipRowsNumberId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True
        
    
    def FieldsRowIndexInit(self, id=None):
        id.setValue(self.fieldsrow)
        self.FieldsRowIndexId = id
        return id


    def FieldsRowIndexUpdate(self):
        self.fieldsrow = self.FieldsRowIndexId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True
        
    
    def GriddingAutoInit(self, id=None):
        if (id != None):
            id.setChecked(self.autogriddingflag)
            if (self.autogriddingflag == True):
               self.stepxgridding = None
               self.stepygridding = None
               Enabled = False
            else:
               Enabled = True
        self.GriddingAutoId = id
        return id


    def GriddingAutoUpdate(self):
        self.stepxgridding = None
        self.stepygridding = None
        self.autogriddingflag = self.GriddingAutoId.isChecked()
        if (self.autogriddingflag == True):
           self.stepxgridding = None
           self.stepygridding = None
           Enabled = False
        else:
           Enabled = True
        self.GriddingXStepLabelId.setEnabled(Enabled)
        self.GriddingXStepId.setEnabled(Enabled)
        self.GriddingYStepLabelId.setEnabled(Enabled)
        self.GriddingYStepId.setEnabled(Enabled)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def GriddingPointsDisplayInit(self, id=None):
        self.GriddingPointsDisplayId = id
        if (id != None):
            id.setChecked(self.dispgriddingflag)
        return id


    def GriddingPointsDisplayUpdate(self):
        self.dispgriddingflag = self.GriddingPointsDisplayId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def GriddingXStepLabelInit(self, id=None):
        id.setEnabled(not self.autogriddingflag)
        self.GriddingXStepLabelId = id
        return id

    
    def GriddingXStepInit(self, id=None):
        id.setSingleStep(0.25)
        id.setEnabled(not self.autogriddingflag)
        self.GriddingXStepId = id
        return id


    def GriddingXStepUpdate(self):
        self.stepxgridding = self.GriddingXStepId.value()
        if (self.stepxgridding_firstime == False):
            if (self.realtimeupdateflag):                       
                self.CartoImageUpdate()                             # updates carto only if real time updating activated
            else:
                self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
                self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
                self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        else:
            self.stepxgridding_firstime = False
        
    
    def GriddingYStepLabelInit(self, id=None):
        id.setEnabled(not self.autogriddingflag)
        self.GriddingYStepLabelId = id
        return id

    
    def GriddingYStepInit(self, id=None):
        id.setSingleStep(0.25)
        id.setEnabled(not self.autogriddingflag)
        self.GriddingYStepId = id
        return id

    
    def GriddingYStepUpdate(self):
        self.stepygridding = self.GriddingYStepId.value()
        if (self.stepygridding_firstime == False):
            if (self.realtimeupdateflag):                       
                self.CartoImageUpdate()                             # updates carto only if real time updating activated
            else:
                self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
                self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
                self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        else:
            self.stepygridding_firstime = False


    def GriddingSizeInit(self, id=None):
        self.GriddingSizeId = id
        return id


    def GriddingSizeUpdate(self):
        text = "%s (%s * %s)"%(self.asciiset.getStringValue('SIZEGRIDDING_ID'), self.rowsnb, self.colsnb)
        self.GriddingSizeId.setText(text)
        
    
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
        self.GriddingInterpolationId = id
        return id


    def GriddingInterpolationUpdate(self):        
        self.interpgridding = self.GriddingInterpolationId.currentText()
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        
    
    def XColumnInit(self, id=None):
        id.setValue(self.x_colnum)
        self.XColumnId = id
        return id

    
    def XColumnUpdate(self):
        self.x_colnum = self.XColumnId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True

    
    def YColumnInit(self, id=None):
        id.setValue(self.y_colnum)
        self.YColumnId = id
        return id

    
    def YColumnUpdate(self):
        self.y_colnum = self.YColumnId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        self.automaticrangeflag = True

    
    def ZColumnInit(self, id=None):
        id.setValue(self.z_colnum)
        self.ZColumnId = id
        return id


    def ZColumnUpdate(self):
        self.z_colnum = self.ZColumnId.value()
        self.automaticrangeflag = True
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button

    
    def FestoonFiltInit(self, id=None):
        if (id != None):
            id.setChecked(self.festoonfiltflag)
        self.FestoonFiltId = id
        return id


    def FestoonFiltUpdate(self):
        self.festoonfiltflag = self.FestoonFiltId.isChecked()
        self.FestoonMethodLabelId.setEnabled(self.festoonfiltflag)
        self.FestoonMethodId.setEnabled(self.festoonfiltflag)
        self.FestoonShiftLabelId.setEnabled(self.festoonfiltflag)
        self.FestoonShiftId.setEnabled(self.festoonfiltflag)
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def FestoonMethodLabelInit(self, id=None):
        id.setEnabled(self.festoonfiltflag)
        self.FestoonMethodLabelId = id
        return id


    def FestoonMethodInit(self, id=None):
                                                    # building of the "plot type" field to select in a list
        method_list = ['Pearson','Spearman', 'Kendall']  # festoonfiltmethod_getlist()
        try:
            method_index = method_list.index(self.festoonfiltmethod)
        except:
            method_index = 0
            
        if (id != None):
            id.addItems(method_list)
            id.setCurrentIndex(method_index)
            id.setEnabled(self.festoonfiltflag)
        self.FestoonMethodId = id
        return id


    def FestoonMethodUpdate(self):
        self.festoonfiltmethod = self.FestoonMethodId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def FestoonShiftLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.festoonfiltflag)
        self.FestoonShiftLabelId = id
        return id


    def FestoonShiftInit(self, id=None):
        if (id != None):                                                    
            range = 400 # TEMP
            id.setRange(-range, +range)
            id.setValue(self.festoonfiltshift)
            id.setEnabled(self.festoonfiltflag)
        self.FestoonShiftId = id
        return id


    def FestoonShiftUpdate(self):
        self.festoonfiltshift = self.FestoonShiftId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def PeakFiltInit(self, id=None):
        if (id != None):
            id.setChecked(self.peakfiltflag)
        self.PeakFiltId = id
        return id


    def PeakFiltUpdate(self):
        self.peakfiltflag = self.PeakFiltId.isChecked()
        self.NanReplacedValuesId.setEnabled(self.peakfiltflag)
        self.MedianReplacedValuesId.setEnabled(self.peakfiltflag)
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def NanReplacedValuesInit(self, id=None):
        if (id != None):
            id.setEnabled(self.peakfiltflag)
            id.setChecked(self.nanreplacedflag)
        self.NanReplacedValuesId = id
        return id


    def NanReplacedValuesUpdate(self):
        self.nanreplacedflag = self.NanReplacedValuesId.isChecked()

        self.MedianReplacedValuesId.setEnabled(not self.nanreplacedflag)

        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def MedianReplacedValuesInit(self, id=None):
        if (id != None):
            id.setEnabled(self.peakfiltflag)
            id.setChecked(self.medianreplacedflag)
        self.MedianReplacedValuesId = id
        return id


    def MedianReplacedValuesUpdate(self):
        self.medianreplacedflag = self.MedianReplacedValuesId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def MedianFiltInit(self, id=None):
        if (id != None):
            id.setChecked(self.medianfiltflag)
        self.MedianFiltId = id
        return id


    def MedianFiltUpdate(self):
        self.medianfiltflag = self.MedianFiltId.isChecked()
        self.NxSizeLabelId.setEnabled(self.medianfiltflag)
        self.NxSizeId.setEnabled(self.medianfiltflag)
        self.NySizeLabelId.setEnabled(self.medianfiltflag)
        self.NySizeId.setEnabled(self.medianfiltflag)
        self.PercentId.setEnabled(self.medianfiltflag)
        self.GapId.setEnabled(self.medianfiltflag)
        
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def NxSizeLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.NxSizeLabelId = id
        return id


    def NxSizeInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
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


    def NySizeLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.NySizeLabelId = id
        return id


    def NySizeInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
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


    def PercentLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.PercentLabelId = id
        return id


    def PercentInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
            id.setRange(0, 100)
            id.setValue(self.percent)
        self.PercentId = id
        return id


    def PercentUpdate(self):
        self.percent = self.PercentId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def GapLabelInit(self, id=None):
        if (id != None):                                                    
            id.setEnabled(self.medianfiltflag)
        self.GapLabelId = id
        return id


    def GapInit(self, id=None):
        if (id != None):
            id.setEnabled(self.medianfiltflag)
            id.setRange(0, 100)
            id.setValue(self.gap)
        self.GapId = id
        return id


    def GapUpdate(self):
        self.gap = self.GapId.value()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ColorMapInit(self, id=None):
                                                    # building of the "color map" field to select in a list
        cmap_list = colormap_getlist()
        try:
            cmap_index = cmap_list.index(self.colormap)
        except:
            cmap_index = 0
            
        if (id != None):
            id.addItems(cmap_list)
            id.setCurrentIndex(cmap_index)
        self.ColorMapId = id
        return id


    def ColorMapUpdate(self):
        self.colormap = self.ColorMapId.currentText()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def ColorMapReverseInit(self, id=None):
        if (id != None):
            id.setChecked(self.reverseflag)
        self.ColorMapReverseId = id
        return id


    def ColorMapReverseUpdate(self):
        self.reverseflag = self.ColorMapReverseId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button
        

    def ColorBarLogScaleInit(self, id=None):
        self.ColorBarLogScaleId = id
        return id


    def ColorBarLogScaleReset(self):
                                                        # gets the limits of the histogram of the data set
        zmin, zmax = self.dataset.histo_getlimits()
        if (zmin <= 0):                                 # if data values are below or equal to zero
            self.colorbarlogscaleflag = False               
            self.ColorBarLogScaleId.setEnabled(False)   # the data can not be log scaled
        else:
            self.ColorBarLogScaleId.setEnabled(True)            
        self.ColorBarLogScaleId.setChecked(self.colorbarlogscaleflag)


    def ColorBarLogScaleUpdate(self):
        self.colorbarlogscaleflag = self.ColorBarLogScaleId.isChecked()
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySpinBoxInit(self, id=None):
        self.MinValuebySpinBoxId = id
        return id


    def MinimalValuebySpinBoxReset(self):
        self.MinValuebySpinBoxId.setRange(self.zmin, self.zmax)
        self.MinValuebySpinBoxId.setValue(self.zmin)


    def MinimalValuebySpinBoxUpdate(self):
        zminsaved = self.zmin
        self.zmin = self.MinValuebySpinBoxId.value()
        if (self.zmin >= self.zmax):
            self.zmin = zminsaved
        self.MinValuebySpinBoxId.setValue(self.zmin)    

        self.MinValuebySliderId.setValue(self.zmin)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MinimalValuebySliderInit(self, id=None):
        id.setOrientation(QtCore.Qt.Horizontal)
        self.MinValuebySliderId = id
        return id


    def MinimalValuebySliderReset(self):
        self.MinValuebySliderId.setRange(self.zmin, self.zmax)
        self.MinValuebySliderId.setValue(self.zmin)


    def MinimalValuebySliderUpdate(self):
        zminsaved = self.zmin
        self.zmin = self.MinValuebySliderId.value()
        if (self.zmin >= self.zmax):
            self.zmin = zminsaved
            self.MinValuebySliderId.setValue(self.zmin)    

        self.MinValuebySpinBoxId.setValue(self.zmin)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MaximalValuebySpinBoxInit(self, id=None):
        self.MaxValuebySpinBoxId = id
        return id


    def MaximalValuebySpinBoxReset(self):
        self.MaxValuebySpinBoxId.setRange(self.zmin, self.zmax)
        self.MaxValuebySpinBoxId.setValue(self.zmax)


    def MaximalValuebySpinBoxUpdate(self):
        zmaxsaved = self.zmax
        self.zmax = self.MaxValuebySpinBoxId.value()
        if (self.zmax <= self.zmin):
            self.zmax = zmaxsaved
            self.MaxValuebySpinBoxId.setValue(self.zmax)    
            
        self.MaxValuebySliderId.setValue(self.zmax)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def MaximalValuebySliderInit(self, id=None):
        id.setOrientation(QtCore.Qt.Horizontal)
        self.MaxValuebySliderId = id
        return id


    def MaximalValuebySliderReset(self):
        self.MaxValuebySliderId.setRange(self.zmin, self.zmax)
        self.MaxValuebySliderId.setValue(self.zmax)
        return id


    def MaximalValuebySliderUpdate(self):
        zmaxsaved = self.zmax
        self.zmax = self.MaxValuebySliderId.value()
        if (self.zmax <= self.zmin):
            self.zmax = zmaxsaved
            self.MaxValuebySliderId.setValue(self.zmax)    
            
        self.MaxValuebySpinBoxId.setValue(self.zmax)
        if (self.realtimeupdateflag):                       
            self.CartoImageUpdate()                             # updates carto only if real time updating activated
            self.HistoImageUpdate()
        else:
            self.CartoImageId.setEnabled(False)                 # disables the carto image to indicate that carto not still updated
            self.ValidButtonId.setEnabled(False)                # disables the valid button until the carto will be updated
            self.DispUpdateButtonId.setEnabled(True)            # enables the display update button


    def HistoImageInit(self, id=None):
        self.HistoImageId = id
        return id


    def HistoImageUpdate(self):
        self.histofig = self.dataset.histo_plot(fig=self.histofig, zmin=self.zmin, zmax=self.zmax)
        histopixmap = QtGui.QPixmap.grabWidget(self.histofig.canvas)   # builds the pixmap from the canvas
        histopixmap = histopixmap.scaledToWidth(200)
        self.HistoImageId.setPixmap(histopixmap)
        

    def DispUpdateButtonInit(self, id=None):
        id.setEnabled(False)                        # disables the button , by default
        if (self.realtimeupdateflag == True):
            id.setHidden(self.realtimeupdateflag)   # Hides button if real time updating activated
        self.DispUpdateButtonId = id
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
        first = True

        initcursor = self.wid.cursor()              # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)    # sets the wait cursor
        
                                                    # gets the fields values
        for n in range(len(self.filenames)):
            # treats data values
            colsnb = getlinesfrom_file(self.filenames[n], self.fileformat, self.delimiter, self.delimitersasuniqueflag, self.skiprows, 10)[0]
            if (first == True):
                datacolsnb = colsnb
            else:
                if (colsnb != datacolsnb):
                    datacolsnb = 0

        if (datacolsnb >= 3) :
            self.XColumnId.setRange(1, datacolsnb)
            self.YColumnId.setRange(1, datacolsnb)
            self.ZColumnId.setRange(1, datacolsnb)

        try:
            # opens temporary files
            success, self.dataset = DataSet.from_file(self.filenames, fileformat=self.fileformat, delimiter=self.delimiter, x_colnum=self.x_colnum, y_colnum=self.y_colnum, z_colnum=self.z_colnum, skipinitialspace=self.delimitersasuniqueflag, skip_rows=self.skiprows, fields_row=self.fieldsrow)            
                
            # makes the z image
            self.dataset.interpolate(interpolation=self.interpgridding, x_delta=self.stepxgridding, y_delta=self.stepygridding, x_decimal_maxnb=2, y_decimal_maxnb=2, x_frame_factor=0., y_frame_factor=0.)
            self.colsnb = len(self.dataset.data.z_image)
            self.rowsnb = len(self.dataset.data.z_image[0])
            self.GriddingSizeUpdate()

            # processes peak filtering if flag enabled
            if (self.peakfiltflag):
                self.dataset.peakfilt(self.zmin, self.zmax, self.medianreplacedflag, self.nanreplacedflag, self.valfiltflag)

            # processes festoon filtering if flag enabled
            if (self.festoonfiltflag):
                self.dataset.festoonfilt(self.festoonfiltmethod, self.festoonfiltshift, self.valfiltflag)

            # processes median filtering if flag enabled
            if (self.medianfiltflag):
                self.dataset.medianfilt(self.nxsize, self.nysize, self.percent, self.gap, self.valfiltflag)

            # resets limits of input parameters
            if (self.automaticrangeflag):
                self.automaticrangeflag = False
                self.zmin, self.zmax = self.dataset.histo_getlimits()
                self.ColorBarLogScaleReset()
                self.MaximalValuebySpinBoxReset()
                self.MaximalValuebySliderReset()
                self.MinimalValuebySpinBoxReset()
                self.MinimalValuebySliderReset()
                
            # plots geophysical image
            if (self.peakfiltflag):     # displays all values to verify peak filtering effects
                cmmin = None            
                cmmax = None
            else:                       # display filtering only
                cmmin = self.zmin
                cmmax = self.zmax
            
            self.cartofig, cartocmap = self.dataset.plot(self.dataset.info.plottype, self.colormap, cmmin=cmmin, cmmax=cmmax, fig=self.cartofig, interpolation='none', creversed=self.reverseflag, logscale=self.colorbarlogscaleflag, pointsdisplay=self.dispgriddingflag)
            self.GriddingXStepId.setValue(self.dataset.info.x_gridding_delta)
            self.dataset.info.x_gridding_delta = self.GriddingXStepId.value()    # to be sure than the value in the dialog box is not the real value arounded
            self.GriddingYStepId.setValue(self.dataset.info.y_gridding_delta)
            self.dataset.info.y_gridding_delta = self.GriddingYStepId.value()    # to be sure than the value in the dialog box is not the real value arounded
            self.interpgridding = self.dataset.info.gridding_interpolation
            self.stepxgridding = self.dataset.info.x_gridding_delta
            self.stepygridding = self.dataset.info.y_gridding_delta
            cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
            self.CartoImageId.setPixmap(cartopixmap)
            self.CartoImageId.setEnabled(True)                              # enables the carto image
            self.ValidButtonId.setEnabled(True)
        except:
            self.cartofig, cartocmap = None, None
            self.CartoImageId.setEnabled(False)                             # disables the carto image
            self.ValidButtonId.setEnabled(False)

        self.DispUpdateButtonId.setEnabled(False)                           # disables the display update button

        self.wid.setCursor(initcursor)                                          # resets the init cursor
