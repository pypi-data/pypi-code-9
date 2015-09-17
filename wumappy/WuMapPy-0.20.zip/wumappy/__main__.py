# -*- coding: utf-8 -*-
'''
    wumappy
    -------

    The public API and command-line interface to WuMapPy package.

    :copyright: Copyright 2014 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
import os, sys
import argparse

from PySide import QtCore, QtGui
from wumappy import SOFTWARE, VERSION, AUTHORS, DATE, DESCRIPTION
from wumappy.gui.common.menubar import *
from wumappy.gui.common.warningdlgbox import *
from wumappy.gui.dataset.datasetwindow import *
from wumappy.gui.geoposset.geopossetwindow import *
from wumappy.gui.opendatasetdlgbox import *
from wumappy.gui.opengeopossetdlgbox import *
from wumappy.gui.guisettingsdlgbox import *
from wumappy.gui.languagedlgbox import *
from wumappy.misc.asciiset import *
from wumappy.misc.configset import *
import geophpy
from geophpy.dataset import *
from geophpy.geoposset import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

ITEM_SEPARATOR = 0
ITEM_FILES = 1
ITEM_SETTINGS = 2
ITEM_HELP = 3
ITEM_DATASET = 10
ITEM_DATASET_OPEN = 11
ITEM_DATASET_IMPORT = 12
ITEM_DATASET_OPENASCIIFILES = 13
ITEM_GEOPOSSET = 14
ITEM_GEOPOSSET_OPEN = 15
ITEM_GEOPOSSET_IMPORT = 16
ITEM_GEOPOSSET_OPENSHAPEFILES = 17
ITEM_EXIT = 18
ITEM_LANGUAGE = 20
ITEM_FONT = 21
ITEM_MISCSETTINGS = 22
ITEM_ABOUT = 30
ITEM_WUMAPPYHELP = 31
ITEM_WUMAPPYPDFUSERMANUAL = 311
ITEM_WUMAPPYHTMLUSERMANUAL = 312
ITEM_GEOPHPYHELP = 32
ITEM_GEOPHPYPDFUSERMANUAL = 321
ITEM_GEOPHPYHTMLUSERMANUAL = 322

class WuMapPyGui(QtGui.QWidget):

    def __init__(self):
        # definitions
        self.currentdatasetwindowsindex = 1
        self.currentgeopossetwindowsindex = 1
        self.datasetwindowslist = []        # list of data set windows
        self.geopossetwindowslist = []      # list of geographic position set windows

        super(WuMapPyGui, self).__init__()

        self.wid = self
        self.configset = ConfigSet()
        self.asciiset = AsciiSet(self.configset.get('ASCII', 'fontname'), self.configset.getint('ASCII', 'fontsize'))              # creates an ascii string set
        self.asciiset.setLanguage(self.configset.get('ASCII', 'language'))
        self.wid.setFont(self.asciiset.font)    # sets the font before creating menu bar

                
        # ITEM_Id, ITEM_NameId, ITEM_Action, ITEM_Comment, Parent_Id, IsEnabled Function
        self.ItemList = [[ITEM_FILES, 'FILES_ID', "Menu", "", None, True], \
                        [ITEM_DATASET, 'DATASET_ID', None, "", ITEM_FILES, True], \
                        [ITEM_DATASET_OPEN, 'OPEN_ID', self.opendataset, "Builds data set from netcdf files", ITEM_FILES, True], \
                        [ITEM_DATASET_IMPORT, 'IMPORT_ID', "Menu", "", ITEM_FILES, True], \
                        [ITEM_DATASET_OPENASCIIFILES, 'FROMASCIIFILES_ID', self.opendatasetfromasciifiles, "Builds data set from ASCII files", ITEM_DATASET_IMPORT, True], \
                        [ITEM_SEPARATOR, '', "Separator", "", ITEM_FILES, True], \
                        [ITEM_GEOPOSSET, 'GEOPOSSET_ID', None, "", ITEM_FILES, True], \
                        [ITEM_GEOPOSSET_OPEN, 'OPEN_ID', self.opengeoposset, "Builds geographics positions set from netcdf files", ITEM_FILES, True], \
                        [ITEM_GEOPOSSET_IMPORT, 'IMPORT_ID', "Menu", "", ITEM_FILES, True], \
                        [ITEM_GEOPOSSET_OPENSHAPEFILES, 'FROMSHAPEFILES_ID', self.opengeopossetfromshapefile, "Builds geographics positions set from shape files", ITEM_GEOPOSSET_IMPORT, True], \
                        [ITEM_SEPARATOR, '', "Separator", "", ITEM_FILES, True], \
                        [ITEM_EXIT, 'EXIT_ID', self.exit, "Exits WuMapPy Application", ITEM_FILES, True], \
                        [ITEM_SETTINGS, 'SETTINGS_ID', "Menu", "", None, True], \
                        [ITEM_LANGUAGE, 'LANGUAGE_ID', self.language, "", ITEM_SETTINGS, True], \
                        [ITEM_FONT, 'FONT_ID', self.font, "", ITEM_SETTINGS, True], \
                        [ITEM_MISCSETTINGS, 'MISCSETTINGS_ID', self.settings, "", ITEM_SETTINGS, True], \
                        [ITEM_HELP, 'HELP_ID', "Menu", "", None, True], \
                        [ITEM_ABOUT, 'ABOUT_ID', self.about, "", ITEM_HELP, True],
                        [ITEM_WUMAPPYHELP, 'WUMAPPYHELP_ID', "Menu", "", ITEM_HELP, True], \
                        [ITEM_WUMAPPYHTMLUSERMANUAL, 'HTMLUSERMANUAL_ID', self.wumappyhtmlhelp, "", ITEM_WUMAPPYHELP, True],
                        [ITEM_WUMAPPYPDFUSERMANUAL, 'PDFUSERMANUAL_ID', self.wumappypdfhelp, "", ITEM_WUMAPPYHELP, True],
                        [ITEM_GEOPHPYHELP, 'GEOPHPYHELP_ID', "Menu", "", ITEM_HELP, True], \
                        [ITEM_GEOPHPYHTMLUSERMANUAL, 'HTMLUSERMANUAL_ID', self.geophpyhtmlhelp, "", ITEM_GEOPHPYHELP, True],
                        [ITEM_GEOPHPYPDFUSERMANUAL, 'PDFUSERMANUAL_ID', self.geophpypdfhelp, "", ITEM_GEOPHPYHELP, True]]
        
        self.LanguageItemList = []        # list of languages action items (item_num, item_id)

        self.menubar = MenuBar.from_list(self.ItemList, self)

                                            # gets the icon from a PNG file 
        self.resources_path = os.path.join(os.path.dirname(__file__), 'resources')
        logo_path = os.path.abspath(os.path.join(self.resources_path, 'wumappy.png'))
        self.icon = QtGui.QIcon(logo_path)

        self.wid.setWindowIcon(self.icon)
        self.wid.setWindowTitle(SOFTWARE)
        self.fillingwindow()



    def fillingwindow(self):
        '''
        
        '''
        logo_path = os.path.abspath(os.path.join(self.resources_path, 'wumappy.png'))
        layout = QtGui.QVBoxLayout()                # builds the main layout
        self.layout = layout
        layout1 = QtGui.QGridLayout()
        layout1.setRowMinimumHeight(0, self.menubar.height)
        layout2 = QtGui.QHBoxLayout()
        layout3 = QtGui.QVBoxLayout()

        layout.addLayout(layout1)                                           # First layout to avoid overwriting with menubar
        layout.addLayout(layout2)                                           
        qlogo = QtGui.QLabel()                                              # Adds the WuMapPy logo
        qlogo.setPixmap(QtGui.QPixmap(logo_path))
        layout2.addWidget(qlogo)
        layout2.addLayout(layout3)
        qfont = QtGui.QFont(family="times")
        qfont.setPointSize(54)                                              # defines the font size for the software title
        message1 = QtGui.QLabel('%s' % SOFTWARE, self.wid)                  # defines the software title
        message1.setFont(qfont)
        message1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout3.addWidget(message1)        
        message2 = QtGui.QLabel('V%s - %s' % (VERSION, DATE), self.wid)     # defines the software version and date
        qfont.setPointSize(16)                                              # defines the font size for the software version and date
        message2.setFont(qfont)
        message2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout3.addWidget(message2)
        message3 = QtGui.QLabel('%s' % DESCRIPTION, self.wid)               # defines the software description
        qfont.setPointSize(16)                                              # defines the font size for the software description
        message3.setFont(qfont)
        message3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout3.addWidget(message3)

        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)                # to not authorize size modification
        self.wid.setLayout(layout)

        self.wid.show()
            


    def closeEvent(self, event):
        '''
        Configures the close event of the main window
        '''
        self.exit()
        

    def opendataset(self):
        '''
        Builds data set from one or several files
        '''
        success = False
        directory = self.configset.get('DIRECTORIES', 'openfiledir')
        qfiledlg = QtGui.QFileDialog(self.wid, directory = directory, filter='*.nc')
        qfiledlg.setFont(self.asciiset.font)
        qfiledlg.setGeometry(self.geometry().left(), self.geometry().top(), qfiledlg.geometry().width(), qfiledlg.geometry().height())
        qfiledlg.show()
        qfiledlg.exec()
        if (qfiledlg.result() == QtGui.QDialog.Accepted):            
            filenames = qfiledlg.selectedFiles()
            success, dataset = DataSet.from_file(filenames, fileformat='netcdf')

            if (success == True):
                colormap = self.configset.get('DISPSETTINGS', 'colormap')
                reverseflag = self.configset.getboolean('DISPSETTINGS', 'reverseflag')
                plottype = self.configset.get('DISPSETTINGS', 'plottype')
                interpolation = self.configset.get('DISPSETTINGS', 'interpolation')
                colorbardisplayflag = self.configset.getboolean('DISPSETTINGS', 'colorbardisplayflag')
                axisdisplayflag = self.configset.getboolean('DISPSETTINGS', 'axisdisplayflag')
                dpi = self.configset.getint('DISPSETTINGS', 'dpi')
                colorbarlogscaleflag = self.configset.getboolean('DISPSETTINGS', 'colorbarlogscaleflag')

                title = "DataSet" + str(self.currentdatasetwindowsindex)
                self.currentdatasetwindowsindex += 1            
                window = DatasetWindow.new(self, title, dataset, self.geopossetwindowslist, plottype, colormap, interpolation, reverseflag = reverseflag, colorbarlogscaleflag = colorbarlogscaleflag, dpi = dpi, colorbardisplayflag = colorbardisplayflag, axisdisplayflag = axisdisplayflag)
                self.datasetwindowslist.append(window)
                window.view()
        
        return(success)


    def opendatasetfromasciifiles(self):
        '''
        Builds data set from one or several text files
        '''
        success = False

        directory = self.configset.get('DIRECTORIES', 'openasciifiledir')
        qfiledlg = QtGui.QFileDialog(self.wid, directory = directory)
        qfiledlg.setFont(self.asciiset.font)
        qfiledlg.setGeometry(self.geometry().left(), self.geometry().top(), qfiledlg.geometry().width(), qfiledlg.geometry().height())
        qfiledlg.show()
        qfiledlg.exec()
        if (qfiledlg.result() == QtGui.QDialog.Accepted):            
            filenames = qfiledlg.selectedFiles()
        
            if (len(filenames)>0):
                delimiter = self.configset.get('FILES', 'delimiter')
                if (delimiter == 'space'):
                    delimiter = ' '
                elif (delimiter == 'tab'):
                    delimiter = '\t'

                self.configset.set('DIRECTORIES', 'openasciifiledir', qfiledlg.directory().path())    

                fileformat = self.configset.get('FILES', 'fileformat')            
                delimitersasuniqueflag = self.configset.getboolean('FILES', 'delimitersasuniqueflag')
                skiprows = self.configset.getint('FILES', 'skiprows')
                fieldsrow = self.configset.getint('FILES', 'fieldsrow')
                xcolnum = self.configset.getint('GENSETTINGS', 'xcolnum')
                ycolnum = self.configset.getint('GENSETTINGS', 'ycolnum')
                zcolnum = self.configset.getint('GENSETTINGS', 'zcolnum')
                stepxgridding = self.configset.getfloat('GENSETTINGS', 'stepxgridding')
                stepygridding = self.configset.getfloat('GENSETTINGS', 'stepygridding')
                interpgridding = self.configset.get('GENSETTINGS', 'interpgridding')
                autogriddingflag = self.configset.getboolean('GENSETTINGS', 'autogriddingflag')
                dispgriddingflag = self.configset.getboolean('GENSETTINGS', 'dispgriddingflag')
                festoonfiltflag = self.configset.getboolean('PROCESSING', 'festoonfiltflag')
                festoonfiltmethod = self.configset.get('PROCESSING', 'festoonfiltmethod')
                festoonfiltshift = self.configset.getint('PROCESSING', 'festoonfiltshift')
            

                colormap = self.configset.get('DISPSETTINGS', 'colormap')
                reverseflag = self.configset.getboolean('DISPSETTINGS', 'reverseflag')

                r, openfiles = OpenDatasetDlgBox.new("Open Data Set", filenames, self, xcolnum, ycolnum, zcolnum, delimiter, fileformat, delimitersasuniqueflag, skiprows, fieldsrow, interpgridding, stepxgridding, stepygridding, autogriddingflag, dispgriddingflag, festoonfiltflag = festoonfiltflag, festoonfiltmethod = festoonfiltmethod, festoonfiltshift = festoonfiltshift, colormap = colormap, reverseflag = reverseflag)
                if (r == QtGui.QDialog.Accepted):
                    success = True
                    dataset = openfiles.dataset
                    zmin = openfiles.zmin
                    zmax = openfiles.zmax
                    colorbarlogscaleflag = openfiles.colorbarlogscaleflag
                    reverseflag = openfiles.reverseflag
                    
                if (success == True):
                    self.configset.set('DISPSETTINGS', 'colormap', str(colormap))
                    self.configset.set('DISPSETTINGS', 'reverseflag', str(reverseflag))
                    self.configset.set('DISPSETTINGS', 'colorbarlogscaleflag', str(colorbarlogscaleflag))
                    
                    plottype = self.configset.get('DISPSETTINGS', 'plottype')
                    interpolation = self.configset.get('DISPSETTINGS', 'interpolation')
                    colorbardisplayflag = self.configset.getboolean('DISPSETTINGS', 'colorbardisplayflag')
                    axisdisplayflag = self.configset.getboolean('DISPSETTINGS', 'axisdisplayflag')
                    dpi = self.configset.getint('DISPSETTINGS', 'dpi')

                    title = "DataSet" + str(self.currentdatasetwindowsindex)
                    self.currentdatasetwindowsindex += 1            
                    window = DatasetWindow.new(self, title, dataset, self.geopossetwindowslist, plottype, colormap, interpolation, reverseflag = reverseflag, colorbarlogscaleflag = colorbarlogscaleflag, zmin = zmin, zmax = zmax, dpi = dpi, colorbardisplayflag = colorbardisplayflag, axisdisplayflag = axisdisplayflag)
                    self.datasetwindowslist.append(window)
                    window.view()
                                                                    # updates configuration file
                    self.configset.set('FILES', 'fileformat', openfiles.fileformat)
                    if (openfiles.delimiter == ' '):
                        delimiter = 'space'
                    elif (openfiles.delimiter == '\t'):
                        delimiter = 'tab'
                    else:
                        delimiter = openfiles.delimiter
                    self.configset.set('FILES', 'delimiter', delimiter)
                    self.configset.set('FILES', 'delimitersasuniqueflag', str(openfiles.delimitersasuniqueflag))
                    self.configset.set('FILES', 'skiprows', str(openfiles.skiprows))
                    self.configset.set('FILES', 'fieldsrow', str(openfiles.fieldsrow))
                    self.configset.set('GENSETTINGS', 'autogriddingflag', str(openfiles.autogriddingflag))
                    self.configset.set('GENSETTINGS', 'dispgriddingflag', str(openfiles.dispgriddingflag))
                    self.configset.set('GENSETTINGS', 'stepxgridding', str(openfiles.stepxgridding))
                    self.configset.set('GENSETTINGS', 'stepygridding', str(openfiles.stepygridding))
                    self.configset.set('GENSETTINGS', 'interpgridding', openfiles.interpgridding)
                    self.configset.set('GENSETTINGS', 'xcolnum', str(openfiles.x_colnum))
                    self.configset.set('GENSETTINGS', 'ycolnum', str(openfiles.y_colnum))
                    self.configset.set('GENSETTINGS', 'zcolnum', str(openfiles.z_colnum))
                    self.configset.set('PROCESSING', 'festoonfiltmethod', openfiles.festoonfiltmethod)
                    self.configset.set('PROCESSING', 'festoonfiltshift', str(openfiles.festoonfiltshift))
                    self.configset.set('PROCESSING', 'festoonfiltflag', str(openfiles.festoonfiltflag))
                else:
                    QtGui.QErrorMessage()                

        return(success)


    def opengeoposset(self):
        '''
        Builds geographics positions set from one or several ascii files
        '''
        success = self._opengeoposset(filter='*.csv', filetype='asciifile')
        return(success)


    def opengeopossetfromshapefile(self):
        '''
        Builds positions set from one or several shape files
        '''
        success = self._opengeoposset(filter='*.shp', filetype='shapefile')
        return(success)



    def _opengeoposset(self, filter='*', filetype='asciifile'):
        '''
        Builds positions set from one or several files
        '''
        success = True
        filenames = QtGui.QFileDialog.getOpenFileNames(filter = filter)
        if (len(filenames[0])>0):
            refsystem = self.configset.get('GEOPOSITIONING', 'refsystem')
            utm_letter = self.configset.get('GEOPOSITIONING', 'utm_letter')
            utm_number = self.configset.getint('GEOPOSITIONING', 'utm_number')
            try :
                r, openfiles = OpenGeopossetDlgBox.new("Open Geographics Positions Set From " + filetype, filetype, filenames[0], refsystem, utm_number, utm_letter, self)
                if (r == QtGui.QDialog.Accepted):
                    geoposset = openfiles.geoposset        
                    title = "GeoPosSet" + str(self.currentgeopossetwindowsindex)
                    self.currentgeopossetwindowsindex += 1
                    window = GeopossetWindow.new(self, title, geoposset, None)
                    self.geopossetwindowslist.append(window)
                    window.view()
                    self.configset.set('GEOPOSITIONING', 'refsystem', str(openfiles.geoposset.refsystem))
                    self.configset.set('GEOPOSITIONING', 'utm_letter', str(openfiles.geoposset.utm_letter))
                    self.configset.set('GEOPOSITIONING', 'utm_number', str(openfiles.geoposset.utm_number))
                                                                    # updates all data set windows
                    for datasetwindow in self.datasetwindowslist:
                        datasetwindow.menubar.update()
            except:
                QtGui.QErrorMessage()                

        return(success)



    def settings(self):
        '''
        Edits GUI Settings
        '''
       
        r, guisettings = GuiSettingsDlgBox.new("User Interface Settings", self)
        if (r == QtGui.QDialog.Accepted):
            self.configset.set('MISC', 'realtimeupdateflag', str(guisettings.realtimeupdateflag))
            


    def language(self):
        '''
        Edits language Settings
        '''
       
        r, language = LanguageDlgBox.new("Language Settings", self)
        if (r == QtGui.QDialog.Accepted):
                                                                # gets new ascii set language and font
            self.asciiset = language.asciiset
                                                                # updates configuration file
            self.configset.set('ASCII', 'language', self.asciiset.lnglist[self.asciiset.lngindex].name)
            
                                                                # updates menu bar with new language or font
            self.menubar.update()
                                                                # updates all data set windows
            for datasetwindow in self.datasetwindowslist:
                datasetwindow.menubar.update()
                                                                # updates all geopos set windows
            for geopossetwindow in self.geopossetwindowslist:
                geopossetwindow.menubar.update()


    def about(self):
        '''
        Displays informations about application
        '''
        text = SOFTWARE + " V" + VERSION  + "\tDate : " + DATE + "\n" + DESCRIPTION + "\n\n" + geophpy.__software__ + " V" + geophpy.__version__ + "\tDate : " + geophpy.__date__ + "\n" + geophpy.__description__ + "\n\nAuthors : " + AUTHORS
        about = QtGui.QMessageBox(self.wid)        
        about.setGeometry(self.geometry().left(), self.geometry().top(), about.geometry().width(), about.geometry().height())
        about.setFont(self.asciiset.font)
        about.setWindowTitle(self.asciiset.getStringValue('ABOUT_ID'))
        about.setText(text)
        about.show()
        about.exec()
            

    def wumappypdfhelp(self):
        '''
        launches pdf wumappy user guide
        '''
        viewer = self.configset.get("MISC", "pdf_viewer")
        os.system(getwumappyhelp(viewer, 'pdf'))


    def wumappyhtmlhelp(self):
        '''
        launches html wumappy user guide
        '''
        viewer = self.configset.get("MISC", "html_viewer")
        os.system(getwumappyhelp(viewer))


    def geophpypdfhelp(self):
        '''
        launches pdf geophpy user guide
        '''
        viewer = self.configset.get("MISC", "pdf_viewer")        
        os.system(getgeophpyhelp(viewer, 'pdf'))


    def geophpyhtmlhelp(self):
        '''
        launches html geophpy user guide
        '''
        viewer = self.configset.get("MISC", "html_viewer")
        os.system(getgeophpyhelp(viewer))


    def font(self):
        '''
        Edits Font Settings
        '''

        qfontdlg = QtGui.QFontDialog(self.asciiset.font, self.wid)
        qfontdlg.setFont(self.asciiset.font)
        qfontdlg.setGeometry(self.geometry().left(), self.geometry().top(), qfontdlg.geometry().width(), qfontdlg.geometry().height())
        qfontdlg.show()
        qfontdlg.exec()
        font = qfontdlg.selectedFont()

        if (qfontdlg.result() == QtGui.QDialog.Accepted):
            self.asciiset.font = font
            self.asciiset.fontname = font.family()
            self.asciiset.fontsize = font.pointSize()
            self.wid.setFont(font)                              # sets the font before updating menu bar

                                                                # updates configuration file
            self.configset.set('ASCII', 'fontname', self.asciiset.fontname)
            self.configset.set('ASCII', 'fontsize', str(self.asciiset.fontsize))
                                                                # updates menu bar with new language or font
            self.menubar.update()
                                                                # updates all data set windows
            self.fillingwindow()

            for datasetwindow in self.datasetwindowslist:
                datasetwindow.menubar.update()
                                                                # updates all geopos set windows
            for geopossetwindow in self.geopossetwindowslist:
                geopossetwindow.menubar.update()


    def exit(self):
        '''
        Exits wumappy application
        '''
        for datasetwindow in self.datasetwindowslist:           # exits all data set windows
            datasetwindow.wid.close()
        for geopossetwindow in self.geopossetwindowslist:       # exits all geo pos set windows
            geopossetwindow.wid.close()
        self.configset.save()                                   # saves configuration file
        self.wid.close()                                        # exits current window



help_path = os.path.join(os.path.dirname(__file__), 'help')
htmlhelp_filename = os.path.abspath(os.path.join(help_path, 'html', 'index.html'))
pdfhelp_filename = os.path.abspath(os.path.join(help_path, 'pdf', 'WuMapPy.pdf'))

def getwumappyhelp(viewer='none', type='html'):
   '''
   To get help documentation of WuMapPy

   Parameters:

   :type: type of help needed, 'html' or 'pdf'.

   Returns:

   :helpcommand: application to start followed by pathname and filename of the 'html' or 'pdf' help document.
   
   '''

   if (type == 'pdf'):
      pathfilename = pdfhelp_filename
   else :
      pathfilename = htmlhelp_filename

   if (viewer == 'none'):           # start automatically the best application 
       helpcommand = pathfilename
   else :
       helpcommand = viewer + " " + pathfilename
   return helpcommand



def main():
    '''Parse command-line arguments and execute WuMapPy command.'''

    parser = argparse.ArgumentParser(prog='%s' % SOFTWARE, 
                                     description='%s' % DESCRIPTION)
    parser.add_argument('--version', action='version',
                        version='%s version %s' % (SOFTWARE, VERSION),
                        help='Print %s’s version number and exit.' % SOFTWARE)

    wumappy = QtGui.QApplication(sys.argv)
    gui = WuMapPyGui()

    sys.exit(wumappy.exec_())



if __name__ == '__main__':
    main()
