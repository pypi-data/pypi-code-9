# -*- coding: utf-8 -*-
'''
    wumappy.misc.asciiset
    ---------------------

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import unicode_literals
import numpy as np
import glob                         # for managing severals files thanks to "*." extension
from PySide import QtGui
import csv, os, platform
from os.path import expanduser

res_dir = "/resources"        # resources directory

english_array = [   \
    # string_id,   string_value
    ['FILES_ID',"Files"],  
    ['SETTINGS_ID', "Settings"],
    ['FONT_ID', "Font"],
    ['MISCSETTINGS_ID', "Miscellaneous settings"],
    ['HELP_ID', "Help"],
    ['WUMAPPYHELP_ID', "WuMapPy"],
    ['GEOPHPYHELP_ID', "GeophPy"],
    ['ABOUT_ID', "About"],    
    ['PDFUSERMANUAL_ID', "Pdf user manual"],  
    ['HTMLUSERMANUAL_ID', "Html user manual"],  
    ['DATASET_ID', "Data set"],
    ['OPEN_ID', "Open"],
    ['IMPORT_ID', "Import"], 
    ['FROMASCIIFILES_ID', "From ASCII files"], 
    ['GEOPOSSET_ID', "Geographics positions set"],
    ['FROMSHAPEFILES_ID', "From shape files"],
    ['EXIT_ID', "Exit"],  
    ['LANGUAGE_ID', "Language"], 
    ['FILEFORMAT_ID', "File format"],    
    ['DELIMITER_ID', "Delimiter"],   
    ['DELIMITERSASUNIQUEFLAG_ID', "Several consecutives as unique"],   
    ['SKIPROWS_ID', "Skip raws number"], 
    ['FIELDSROW_ID', "Fields row index"],   
    ['AUTOGRIDDINGFLAG_ID', "Automatical gridding"],  
    ['DISPGRIDDINGFLAG_ID', "Gridding points display"], 
    ['STEPXGRIDDING_ID', "Gridding X step"], 
    ['STEPYGRIDDING_ID', "Gridding Y step"], 
    ['INTERPOLATION_ID', "Interpolation"],   
    ['XCOLNUM_ID', "X column"],  
    ['YCOLNUM_ID', "Y column"],  
    ['ZCOLNUM_ID', "Z column"],  
    ['CANCEL_ID', "Cancel"],
    ['UNDO_ID', "Undo"],
    ['VALID_ID', "Valid"],
    ['RESET_ID', "Reset"],
    ['SAVE_ID', "Save"],
    ['SELECTALL_ID', "Select all"],
    ['UNSELECTALL_ID', "Unselect all"],
    ['DISPLAYSETTINGS_ID', "Display settings"],  
    ['CLOSE_ID', "Close"],   
    ['PRINT_ID', "Print"],   
    ['EXPORT_ID', "Export"],   
    ['EXPORTIMAGE_ID', "As an image file"],   
    ['EXPORTKML_ID', "As an kml file"],   
    ['EXPORTRASTER_ID', "As a raster file(picture + worldfile)"],   
    ['PROCESSING_ID', "Processing"], 
    ['MAGPROCESSING_ID', "Magnetic processing"], 
    ['PLOTTYPE_ID', "Plot type"],   
    ['COLORMAP_ID', "Color map"],    
    ['REVERSEFLAG_ID', "Color map reverse"], 
    ['COLORBARDISPLAYFLAG_ID', "Color bar display"], 
    ['COLORBARLOGSCALEFLAG_ID', "Color bar log scale"],  
    ['AXISDISPLAYFLAG_ID', "Axis display"],  
    ['MINIMALVALUE_ID', "Minimal value"],    
    ['MAXIMALVALUE_ID', "Maximal value"],   
    ['CLOSE_ID', "Close"],  
    ['GEOREFERENCING_ID', "Geo-referencing"],   
    ['FONTNAME_ID', "Font name"],   
    ['FONTSIZE_ID', "Font size"],
    ['RTUPDATE_ID', "Real time update"],
    ['DISPUPDATE_ID', "Update"],
    ['INFORMATIONS_ID', "Informations"],
    ['BADFILEFORMAT_MSG', "Bad file format !"],
    ['PEAKFILT_ID', "Peak filtering"],
    ['VALFILT_ID', "Uses initial data values"],
    ['NANREPLACEDFLAG_ID', "Overlimits values replaced by 'nan'"],
    ['MEDIANREPLACEDFLAG_ID', "Overlimits values replaced by median value"],
    ['MEDIANFILT_ID', "Median filtering"],
    ['FILTERNXSIZE_ID', "Filter size in X coordinates (pixels)"],
    ['FILTERNYSIZE_ID', "Filter size in Y coordinates (pixels)"],
    ['MEDIANFILTERPERCENT_ID', "Median value filtering (%)"],
    ['MEDIANFILTERGAP_ID', "Constant gap filtering"],
    ['FESTOONFILT_ID', "Festoon filtering"],
    ['FESTOONFILTMETHOD_ID', "Correlation method"],
    ['FESTOONFILTSHIFT_ID', "Shift(pixels)"],
    ['POLEREDUCTION_ID', "Pôle reduction"],
    ['APODISATIONFACTOR_ID', "Apodisation(%)"],
    ['APODISATIONFACTOR_MSG', "(0, for no apodisation)"],
    ['INCLINEANGLE_ID', "Inclination(deg)"],
    ['ALPHAANGLE_ID', "Alpha(deg)"],
    ['CORRELATIONMAP_ID', "Correlation map"],
    ['CORRELATIONSUM_ID', "Correlation sum"],
    ['LOGTRANSFORM_ID', "Log. transformation"],
    ['LOGTRANSFORM_MSG', "This factor depends on the data precision.\nIt is approximatively the inverse of this precision"],
    ['LOGTRANSFORM_REF', "Enhancement of magnetic data by logarithmic transformation.\nBill Morris, Matt Pozza, Joe Boyce and George Leblanc\nThe Leading EDGE August 2001, Vol 20, N°8"],
    ['MULTFACTOR_ID', "Multiply factor"],
    ['SIZEGRIDDING_ID', "Gridding size"],
    ['CONTINUATION_ID', "Continuation"],
    ['PROSPTECH_ID', "Technical of prospection"],
    ['DOWNSENSORALT_ID', "Down sensor altitude(m)"],
    ['UPSENSORALT_ID', "Up sensor altitude(m)"],
    ['ALTITUDE_MSG', "(Altitudes are relatives to the soil surface)"],
    ['CONTINUATIONFLAG_ID', "Continuation"],
    ['CONTINUATIONVALUE_ID', "Value(m)"],
    ['SOILSURFACEABOVEFLAG_ID', "Above the soil surface"],
    ['SOILSURFACEBELOWFLAG_ID', "Below the soil surface"],
    ['PROFILESNB_ID', "Profiles number"],
    ['DESTRIPINGMETHOD_ID', "Destriping method"],
    ['CONSTDESTRIP_ID', "Constant destriping"],
    ['DESTRIPINGDEGREESNB_ID', "Polynomial degree"],
    ['CUBICDESTRIP_ID', "Cubic destriping"],
    ['REGTRENDFILT_ID', "Regional trend filtering"],
    ['REGTRENDMETHOD_ID', "Method"],
    ['REGTRENDCOMPONENT_ID', "Component"],
    ['WALLISSETMEAN_ID', "Setmean"],
    ['WALLISSETSTDEV_ID', "Setstdev"],
    ['WALLISSETGAIN_ID', "Setgain"],
    ['WALLISLIMIT_ID', "Limit"],
    ['WALLISEDGEFACTOR_ID', "Edge factor"],
    ['WALLISFILT_ID', "Wallis filtering"],
    ['PLOUGHANGLE_ID', "Angle"],
    ['PLOUGHCUTOFF_ID', "Cut off"],
    ['PLOUGHFILT_ID', "Anti-ploughing filtering"],
    ['STRUCTINDEX_ID', "Structural index"],
    ['EULERDECONV_ID', "Euler deconvolution"],
    ['EULERDECONV_MSG', "For having an estimation of the depth of an anomaly, click the mouse at two points allowing this anomaly"],
    ['ANALYTICSIGNAL_ID', "Analytic signal"],
    ['SUSCEPTIBILITY_ID', "Equivalent stratum in magnetic susceptibility"],
    ['GRADMAGFIELDCONV_ID', "Gradient <-> Magnetic field"],
    ['CALCDEPTH_ID', "Calculation depth(m)"],
    ['EQSTRATTHICKNESS_ID', "Thickness of equivalent stratum(m)"],
    ['PROSPTECHUSED_ID', "Technical prospection used"],
    ['PROSPTECHSIM_ID', "Technical prospection simulated"],
    ['POINTSLIST_ID', "List of points"],
    ['POINTNUM_ID', "num"],
    ['POINTLONGITUDE_ID', "Longitude"],
    ['POINTLATITUDE_ID', "Latitude"],
    ['POINTEASTING_ID', "Easting"],
    ['POINTNORTHING_ID', "Northing"],
    ['POINTX_ID', "X"],
    ['POINTY_ID', "Y"],
    ['POINTSELECTED_ID', "Selected"],
    ['POINTXYCONVERTED_ID', "(X,Y) coordinates"],
    ['REFSYSTEM_ID', "Ref System"],
    ['UTMLETTER_ID', "UTM Letter"],
    ['UTMNUMBER_ID', "UTM Number"],
    ['GEOREFERROR1_MSG', "Not enough points to georeference data set !"],
    ['GEOREFERROR2_MSG', "data set zone greater than selected points list zone !"],
    ['CONFIG_ID', "Configuration"]]


class Language:
    ''' Caracteristics of a language : name, fontname, fontsize, and dictionnary of strings
    '''
    name = ""
    dict = None


class AsciiSet(object):    
    def __init__(self, fontname = None, fontsize = 10):
        # builds the languages list
        self.lnglist = []  # creates empty list
        self.fontsize = fontsize
        self.addLanguage("english", english_array)
        self.lngindex = 0
        self.fontname = fontname
        self.fontsize = fontsize
        self.font = QtGui.QFont(fontname, fontsize)         # updates the font

        if (platform.system() == 'Windows'):
            self.main_dir = expanduser("~") + "/wumappy"
        else:           # Linux, Mac OS, ...
            self.main_dir = expanduser("~") + "/.wumappy"

                        # create the ressource directory if not exists
        os.makedirs(self.main_dir + res_dir, exist_ok=True)

                        # searches the langages files
        filenames = glob.glob(self.main_dir + res_dir + "/*.lng")        # extension if the filenames field is like "*.txt"
        for filename in filenames:
            error, name, array2D = self.readLanguage(filename)
            if ((error == 0) and (name!="english")):
                self.addLanguage(name, array2D)
        
                        # writes the english language file            
        self.saveLanguage(self.main_dir + res_dir + "/english.lng", "english", english_array)
        self.setLanguage("english")
        

    def setLanguage(self, name):
        ''' Sets the display language
        '''
        newname = self.lnglist[self.lngindex].name
        for i in range(len(self.lnglist)):
            if (name == self.lnglist[i].name):
                self.lngindex = i
                newname = name
                break

        return self.lngindex, newname


    def getLanguageList(self):
        ''' Gets the list of the names of languages
        '''
        list=[]
        for lang in self.lnglist:
            list.append(lang.name)
        return list
    

    def language(self):
        ''' Gets the current display language
        '''
        return self.lngindex, self.lnglist[self.lngindex].name


    def addLanguage(self, name, array2D):
        '''
        '''
        lang = Language()               # inits a language
        lang.name = name                
        lang.dict = self.arrayToDict(array2D)
        self.lnglist.append(lang)


    def arrayToDict(self, array2D):
        ''' Converts a 2D array in disctionnary
        '''
        dict =  {}
        for line in array2D:
            dict[line[0]] = line[1]
        return dict


    def getStringValue(self, string_id):
        ''' Gets the string corresponding to the string identifiant
        '''
        string_value = ''
        if (string_id != ''):
            try:            # if string_id exits in the current language, all is fine
                string_value = self.lnglist[self.lngindex].dict[string_id]
            except:         
                try:        # if not, try to use string_id in english array
                    string_value = self.lnglist[0].dict[string_id]
                except:     # if string_id doesn't exist in english array
                    string_value = "?????"
                    
        return string_value


    def saveLanguage(self, filename, name, array2D, delimiter = '\t'):
        ''' Writes the language in a file
        '''
        error = 0       # no error by default
        try:
            csvfile = open(filename, 'w')
        except:
            error = -1

        if (error == 0):    # if no error
            writer = csv.writer(csvfile, delimiter=delimiter)
            writer.writerow([name])                 # writes the name of the language at the first line
            for line in array2D:
                if (len(line) == 2):
                    writer.writerow([line[0], line[1]])
        return error


    def readLanguage(self, filename, delimiter = '\t'):
        ''' Readss the language in a file
        '''
        error = 0       # no error by default
        try:
            csvfile = open(filename, 'r')
        except:
            error = -1

        array2D = []
        name = ""

        if (error == 0):    # if no error
            reader = csv.reader(csvfile, delimiter=delimiter)
            row = next(reader)
            if (len(row) == 1):
                name = row[0]                           # reads the name of the language at the first line
                row = next(reader)                
            for row in reader:                          # reads the string array tu display
                if (len(row) == 2):
                    array2D.append([row[0], row[1]])

        return error, name, array2D


    def setFontSize(self, fontsize):
        ''' Sets the font size
        '''
        self.fontsize = fontsize
        return self.fontsize
    