# -*- coding: utf-8 -*-
'''
    wumappy.gui.dataset.eulerdeconvolutiondlgbox
    --------------------------------------------

    Euler deconvolution dialog box management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty, and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
from geophpy.dataset import *
from PySide import QtCore, QtGui
import os, csv
from wumappy.gui.common.cartodlgbox import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#---------------------------------------------------------------------------#
# Euler deconvolution Dialog Box Object                                     #
#---------------------------------------------------------------------------#
class EulerDeconvolutionDlgBox:
    
    def __init__(self):
        pass

    @classmethod
    def new(cls, title, parent, apod=0, nflag=False, nvalue=0):
        '''
        '''
        
        window = cls()
        window.parent = parent
        window.dataset = parent.dataset
        window.originaldataset = parent.dataset
        window.asciiset = parent.asciiset
        window.configset = parent.configset
        window.icon = parent.icon
        window.realtimeupdateflag = window.configset.getboolean('MISC', 'realtimeupdateflag')
        window.apod = apod
        window.nflag = nflag
        window.nvalue = nvalue
        window.disprects = []
        window.disppoints = []
        window.xfirstpoint = None
        window.yfirstpoint = None
        window.items_list = [['Label', 'APODISATIONFACTOR_ID', 0, 0, False, None, None],  
                           ['SpinBox', '', 1, 0, True, window.ApodisationFactorInit, window.ApodisationFactorUpdate],    
                           ['Label', 'APODISATIONFACTOR_MSG', 2, 0, False, None, None],
                           ['SpinBox', '', 4, 0, True, window.StructIndexValueInit, window.StructIndexValueUpdate],
                           ['CheckBox', 'STRUCTINDEX_ID', 3, 0, True, window.StructIndexFlagInit, window.StructIndexFlagUpdate],  
                           ['Label', 'EULERDECONV_MSG', 1, 1, False, None, None],  
                           ['TextEdit', '', 6, 0, True, window.EulerDeconvResultInit, None],    
                           ['MiscButton', 'RESET_ID', 7, 0, True, window.ResetButtonInit, window.ResetButtonUpdate],   
                           ['MiscButton', 'UNDO_ID', 8, 0, True, window.UndoButtonInit, window.UndoButtonUpdate],   
                           ['MiscButton', 'DISPUPDATE_ID', 9, 0, True, window.DispUpdateButtonInit, window.DispUpdateButtonUpdate],   
                           ['MiscButton', 'SAVE_ID', 10, 0, True, window.SaveButtonInit, window.SaveButtonUpdate],   
                           ['CancelButton', 'CANCEL_ID', 11, 0, True, window.CancelButtonInit, None],   
                           ['Image', '', 0, 1, False, window.CartoImageInit, window.CartoImageMouseLeftClick]]

        dlgbox = CartoDlgBox(title, window, window.items_list)
        dlgbox.exec()

        return dlgbox.result(), window


    def ApodisationFactorInit(self, id=None):
        if (id != None):
            id.setRange(0, 25)
            id.setSingleStep(5)
            id.setValue(self.apod)
        self.ApodisationFactorId = id
        return id


    def ApodisationFactorUpdate(self):
        self.apod = self.ApodisationFactorId.value()


    def StructIndexValueInit(self, id=None):
        if (id != None):
            id.setRange(0, 3)
            id.setSingleStep(1)
            id.setValue(self.nvalue)
        self.StructIndexValueId = id
        return id


    def StructIndexValueUpdate(self):
        self.nvalue = self.StructIndexValueId.value()
      

    def StructIndexFlagInit(self, id=None):
        if (id != None):
            id.setChecked(self.nflag)
        self.StructIndexFlagId = id
        self.StructIndexValueId.setEnabled(self.nflag)
        return id


    def StructIndexFlagUpdate(self):
        self.nflag = self.StructIndexFlagId.isChecked()
        self.StructIndexValueId.setEnabled(self.nflag)
      

    def EulerDeconvResultInit(self, id=None):
        if (id != None):
            id.setReadOnly(True)
            self.eulerdeconvresults = [['xmin','xmax','ymin','ymax','n','x','y','depth']]
            id.setText("xmin,xmax,ymin,ymax,n,x,y,depth")

        self.EulerDeconvResultId = id
        return id


    def ResetButtonInit(self, id=None):
        self.ResetButtonId = id
        return id


    def ResetButtonUpdate(self):
        self.disprects=[]
        self.disppoints=[]
        self.eulerdeconvresults = [['xmin','xmax','ymin','ymax','n','x','y','depth']]
        self.EulerDeconvResultId.setText("xmin,xmax,ymin,ymax,n,x,y,depth")
        self.CartoImageUpdate()                                 # updates carto image
        

    def UndoButtonInit(self, id=None):
        self.UndoButtonId = id
        return id


    def UndoButtonUpdate(self):
        self.EulerDeconvResultId.undo()
        if (len(self.disppoints) > 0):
            self.disppoints.pop()
        if (len(self.disprects) > 0):
            self.disprects.pop()
        if (len(self.eulerdeconvresults) > 1):
            self.eulerdeconvresults.pop()
        self.CartoImageUpdate()
        

    def DispUpdateButtonInit(self, id=None):
        self.DispUpdateButtonId = id
        id.setHidden(self.realtimeupdateflag)                   # Hides button if real time updating activated
        id.setEnabled(False)                                    # disables the button , by default
        return id


    def DispUpdateButtonUpdate(self):
        self.CartoImageUpdate()                                 # updates carto image
        

    def SaveButtonInit(self, id=None):
        self.SaveButtonId = id
        return id


    def SaveButtonUpdate(self):
        dir = self.configset.get('DIRECTORIES', 'eulerfiledir')

        initcursor = self.wid.cursor()                                          # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                                # sets the wait cursor

        qfiledlg = QtGui.QFileDialog(self.wid, directory = dir)
        qfiledlg.setFont(self.asciiset.font)
        qfiledlg.setGeometry(self.wid.geometry().left(), self.wid.geometry().top(), qfiledlg.geometry().width(), qfiledlg.geometry().height())
        qfiledlg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        qfiledlg.show()
        qfiledlg.exec()
        if (qfiledlg.result() == QtGui.QDialog.Accepted):
            fullfilename = qfiledlg.selectedFiles()
            self.configset.set('DIRECTORIES', 'eulerfiledir', os.path.dirname(fullfilename[0]))
            with open(fullfilename[0], 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                writer.writerows(self.eulerdeconvresults)
            
        self.wid.setCursor(initcursor)                                          # resets the init cursor
        self.SaveButtonId.setEnabled(False)                                     # disables the save button
        

    def CancelButtonInit(self, id=None):
        self.CancelButtonId = id
        return id


    def CartoImageInit(self, id=None):
        self.cartofig = None
        self.CartoImageId = id
        self.CartoImageUpdate()
        return id


    def CartoImageMouseLeftClick(self, x=None, y=None):
        if ((x!=None) and (y!=None)):
            if (self.xfirstpoint==None or self.yfirstpoint==None):
                # first point of rectangle to save
                self.xfirstpoint = x
                self.yfirstpoint = y
            else:
                # second point of rectangle to construct the rectangle
                if (x < self.xfirstpoint):
                    xmin = x
                    xmax = self.xfirstpoint
                else:
                    xmin = self.xfirstpoint
                    xmax = x
                if (y < self.yfirstpoint):
                    ymin = y
                    ymax = self.yfirstpoint
                else:
                    ymin = self.yfirstpoint
                    ymax = y
                self.disprects.append([xmin, ymin, xmax - xmin, ymax - ymin])
                self.nvalue, x, y, depth, xnearestmin, ynearestmin, xnearestmax, ynearestmax = self.dataset.eulerdeconvolution(xmin, xmax, ymin, ymax, self.apod, self.nflag, self.nvalue)                
                self.disppoints.append([x, y])
                self.eulerdeconvresults.append([xnearestmin,xnearestmax,ynearestmin,ynearestmax,self.nvalue,x,y,depth])
                self.EulerDeconvResultId.append("%.02f, %.02f, %.02f, %.02f, %.02f, %.02f, %.02f, %.02f"%(xnearestmin,xnearestmax,ynearestmin,ynearestmax,self.nvalue,x,y,depth))
                self.CartoImageUpdate()
                self.xfirstpoint = None
                self.yfirstpoint = None
            

    def CartoImageUpdate(self):
        initcursor = self.wid.cursor()                                  # saves the init cursor type
        self.wid.setCursor(QtCore.Qt.WaitCursor)                        # sets the wait cursor

        # processes data set
        self.dataset = self.originaldataset.copy()

        # plots geophysical image
        tempfilename=self.configset.temp_dir + "/temp.PNG"
        self.cartofig, cartocmap = self.dataset.plot(self.parent.plottype, self.parent.colormap, creversed=self.parent.reverseflag, fig=self.cartofig, filename=tempfilename, interpolation=self.parent.interpolation, cmmin=self.parent.zmin, cmmax=self.parent.zmax, cmapdisplay = False, axisdisplay = False, logscale=self.parent.colorbarlogscaleflag, rects = self.disprects, points = self.disppoints)
        cartopixmap = QtGui.QPixmap(tempfilename)
#        cartopixmap = QtGui.QPixmap.grabWidget(self.cartofig.canvas)    # builds the pixmap from the canvas
        self.CartoImageId.setSize(cartopixmap.width(), cartopixmap.height())      # sets the size in pixels of the pixmap displayed
        self.CartoImageId.setPixmap(cartopixmap) 
        self.CartoImageId.setEnabled(True)                              # enables the carto image
        if (len(self.eulerdeconvresults) > 1):
            self.ResetButtonId.setEnabled(True)                         # enables the reset button
            self.UndoButtonId.setEnabled(True)                          # enables the undo button
            self.SaveButtonId.setEnabled(True)                          # enables the save button
        else:
            self.ResetButtonId.setEnabled(False)                         # disables the reset button
            self.UndoButtonId.setEnabled(False)                          # disables the undo button
            self.SaveButtonId.setEnabled(False)                          # disables the save button
            
        self.DispUpdateButtonId.setEnabled(False)                       # disables the display update button
        
        self.wid.setCursor(initcursor)                                  # resets the init cursor
