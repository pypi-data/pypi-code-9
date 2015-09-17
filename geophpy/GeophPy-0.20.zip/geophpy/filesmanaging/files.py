# -*- coding: utf-8 -*-
'''
    geophpy.filesmanaging.files
    ---------------------------

    Input and output File management.

    :copyright: Copyright 2014 Lionel Darras, Philippe Marty and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
### USER DEFINED PARAMETERS ##########################################

# list of file formats treated in this file
fileformat_list = ['ascii', 'netcdf']

######################################################################



from operator import itemgetter
import csv              # for csv files treatment
import glob             # for managing severals files thanks to "*." extension
import netCDF4 as nc4
import numpy as np
import os, time, platform
import geophpy
from geophpy.misc.utils import *
from geophpy.operation.general import *



def fileformat_getlist():
    '''Get the the list of file formats treated
    Returns :
        - fileformat_list : list of file formats.
    '''
    return fileformat_list



def getlinesfrom_ascii(filename, delimiter='\t', skipinitialspace=True, skiprowsnb=0, rowsnb=1):
    ''' Reads lines in an ascii file
    Parameters :

    :filename: file name with extension to read, "test.dat" for example.

    :delimiter: delimiter between fields, tabulation by default.

    :skipinitialspace: if True, considers severals delimiters as only one : "\t\t" as '\t'.

    :skiprowsnb: number of rows to skip to get lines.

    :rowsnb: number of the rows to read, 1 by default.

    Returns :
        - colsnb : number of the columns in all rows, 0 if rows have not the sames columns nb
        - rows : rows.
    '''

    rows = []                                               # empty list
    colsnb = 0
    first=True

    if (os.path.isfile(filename) == True) :                 # if file exist
        csv_reader = csv.reader(open(filename,"r"), delimiter=delimiter, skipinitialspace=skipinitialspace)
        for i in range(skiprowsnb):
            next(csv_reader)                    # skip the row
        for i in range(rowsnb):
            row = next(csv_reader)
            rows.append(row)                    # reads the row
            if (first == True):                 # if first passage
                colsnb = len(row)
                first = False
            else:                               # if not first passage
                if (len(row) != colsnb):        # if size of row different than size of previous rows
                    colsnb = 0                  # initialises number of columns

    return colsnb, rows



# ...TBD... following function seems not to be used !!!
def getxylimitsfrom_ascii(filenameslist, delimiter='\t', skipinitialspace=True, x_colnum=1, y_colnum=2, skiprowsnb=1):
    '''Gets list of XY limits from a list of ascii files
    Parameters :

    :filenameslist: list of files to treat,

    ['file1.xyz', 'file2.xyz', ...] or,

    ['file*.xyz'] to open all files with a filename beginning by "file", and ending by ".xyz".

    :delimiter: delimiter between fields in a line, '\t', ',', ';', ...

    :x_colnum: column number of the X coordinate of the profile, 1 by default.

    :y_colnum: column number of the Y coordinate inside the profile, 2 by default.

    :skiprowsnb: number of rows to skip to get values, 1 by default (to skip fields_row).

    Returns :
        - files nb treated.
        - list of XY limits :
          [[file1_xmin, file1_xmax, file1_ymin, file1_ymax], ..., [fileX_xmin, fileX_xmax, fileX_ymin, fileX_ymax]]
    '''

    filenames_fulllist = []                             # initialisation of the full list if files
    filesnb = 0
    for filenames in filenameslist:                     # for each filenames in the list
        filenamesextended = glob.glob(filenames)        # extension if the filenames field is like "*.txt"
        for filename in filenamesextended:              # for each filename in the extended filenames list
            filenames_fulllist.append(filename)         # adds the filename in the full list of files
            filesnb = filesnb + 1                       # increments files number

                                                            # initialisation
    values_array = []                                   # empty list
    xylimitsarray = []

    for filename in filenames_fulllist:                 # for each filename in the list
        if (os.path.isfile(filename) == True) :         # if file exist
            csvRawFile = csv.reader(open(filename,"r"), delimiter=delimiter, skipinitialspace=skipinitialspace)
            for i in range(skiprowsnb):
                next(csvRawFile)                        # splits header from values array
            data = []
            for line in csvRawFile:
                data.append(line)

            dataT = np.array(data).T
            xylimitsarray.append([dataT[x_colnum-1].min, dataT[x_colnum-1].max, dataT[y_colnum-1].min, dataT[y_colnum-1].max])

    return filesnb, xylimitsarray



def from_ascii(dataset, filenameslist, delimiter='\t', skipinitialspace=True, x_colnum=1, y_colnum=2, z_colnum=3, skip_rows=1, fields_row=0):
   '''
   cf. dataset.py

   returned error codes:

   :0: no error

   :-1: invalid column number

   :-2: file does not exist

   :-3: no file found

   '''
   # if bad number of column #########################################
   if ((x_colnum < 1) or (y_colnum < 1) or (z_colnum < 1)):
      return -1

   # initialisation of the full list of files ########################
   filenames_fulllist = []
   for filenames in filenameslist:
      # extension if filenames is like "*.txt" #######################
      filenamesextended = glob.glob(filenames)
      for filename in filenamesextended:
         # if file exist
         if (os.path.isfile(filename)):
            # adds the filename in the full list of files
            filenames_fulllist.append(filename)
         else:
            return -2
   if (len(filenames_fulllist) == 0):
      return -3

   # if index of fields_row > nb of rows of the header ###############
   if (fields_row >= skip_rows):
      # fields X, Y, Z by default
      fields_row = -1

   # data initialisation #############################################
   values_array = []

   # read the field names only in the first file #####################
   firstfile = True

   # read the data in each file ######################################
   for filename in filenames_fulllist:
      csvRawFile = csv.reader(open(filename,"r"), delimiter=delimiter, skipinitialspace=skipinitialspace)
      # read the beginning of the file as header #####################
      csvHeader = []
      for row in range(skip_rows):
         csvHeader.append(next(csvRawFile))
      # read the rest of the file as data ############################
      csvValuesFileArray = []
      for csvRawLine in csvRawFile:
         csvValuesFileArray.append(csvRawLine)
      # treat header only for first file #############################
      if (firstfile):
         # constructs the array of field names #######################
         if (fields_row > -1):
            try:
               dataset.data.fields = [(csvHeader[fields_row])[x_colnum-1], (csvHeader[fields_row])[y_colnum-1], (csvHeader[fields_row])[z_colnum-1]]
            except:
               dataset.data.fields = ["X", "Y", "Z"]
         else:
            dataset.data.fields = ["X", "Y", "Z"]
         # first file has now been treated ###########################
         firstfile = False
      # treat data for each file #####################################
      for csvValuesLine in csvValuesFileArray:
         try:
            # add values from selected columns
            values_array.append([float(csvValuesLine[x_colnum-1]), float(csvValuesLine[y_colnum-1]), float(csvValuesLine[z_colnum-1])])
         except:
            try:
                # add a 'nan' value
                values_array.append([float(csvValuesLine[x_colnum-1]), float(csvValuesLine[y_colnum-1]), np.nan])
            except:
                # skip line
                continue

   # converts in a numpy array, sorted by column 0 then by column 1.
   dataset.data.values = np.array(sorted(values_array, key=itemgetter(0,1)))

   # Note : values_array is an array of N points of measures [x, y, z], but not in a regular grid, and perhaps with data gaps.

   return 0



def to_ascii(dataset, filename, delimiter='\t'):
   '''
   cf. dataset.py

   returned error codes:

   :0: no error

   '''
   ResultFile = csv.writer(open(filename,"w", newline=''), delimiter=delimiter)
   # writes the first line of the file with fields names
   ResultFile.writerow(dataset.data.fields)
   # initialisation of the lines to write in the file
   csvLines=[]
   # writes lines in the file.
   ResultFile.writerows(csvLines)
   return 0



def from_netcdf(dataset, filenameslist, x_colnum=1, y_colnum=2, z_colnum=3):
   '''
   cf. dataset.py

   returned error codes:

   :0: no error

   :-1: invalid column number

   :-2: file does not exist

   :-3: no file found

   '''
   # if bad number of column #########################################
   if ((x_colnum < 1) or (y_colnum < 1) or (z_colnum < 1)):
      return -1

   # initialisation of the full list of files ########################
   filenames_fulllist = []
   for filenames in filenameslist:
      # extension if filenames is like "*.txt" #######################
      filenamesextended = glob.glob(filenames)
      for filename in filenamesextended:
         # if file exist
         if (os.path.isfile(filename)):
            # adds the filename in the full list of files
            filenames_fulllist.append(filename)
         else:
            return -2
   if (len(filenames_fulllist) == 0):
      return -3

   # in case of MFDataset (Multi Files) ##############################
   if (len(filenames_fulllist) > 1):
      pass # ...TBD...

   # in case of single file ##########################################
   else:
      # Open netcdf file #############################################
      filename = filenames_fulllist[0]
      fileroot = nc4.Dataset(filename, "r", format="NETCDF4")

      # Read dataset attributes ######################################
      # for attr in fileroot.ncattrs():
      dataset_description      = fileroot.description
      dataset_originalfilename = fileroot.filename # ...TBD... à comparer avec la veleur courante de filename ?
      dataset_history          = fileroot.history
      dataset_os               = fileroot.os
      dataset_author           = fileroot.author
      dataset_source           = fileroot.source
      dataset_version          = fileroot.version
      # ...TBD... pour l'instant on ne fait rien des variables dataset_* ... les inclure dans la structure Dataset définie dans dataset.Py ?

      # Read dataset values ##########################################
      dat_grp = fileroot.groups["Data"]
      dataset_data_units = []
      dataset_data_values = []
      zimg = False
      eimg = False
      nimg = False
      fields  = list(dat_grp.variables.keys())
      if ('z_image' in fields):
         fields.remove('z_image')
         zimg = True
      if ('easting_image' in fields):
         fields.remove('easting_image')
         eimg = True
      if ('northing_image' in fields):
         fields.remove('northing_image')
         nimg = True
      for field in fields:
         val_var = dat_grp.variables[field]
         dataset_data_units.append(val_var.units)         # ...TBD...
         dataset_data_values.append(val_var)
      dataset.data.fields                 = list(fields)
      dataset.data.values                 = np.array(dataset_data_values)
      if (zimg):
         img_var = dat_grp.variables['z_image']
         dataset.data.z_image                = np.array(img_var)
         dataset_info_z_units                = img_var.units # ...TBD...
         dataset_info_z_nanval               = img_var.missing_value
         dataset.info.x_min                  = img_var.x_min
         dataset.info.x_max                  = img_var.x_max
         dataset.info.y_min                  = img_var.y_min
         dataset.info.y_max                  = img_var.y_max
         dataset.info.z_min                  = img_var.z_min
         dataset.info.z_max                  = img_var.z_max
         dataset.info.x_gridding_delta       = img_var.grid_xdelta
         dataset.info.y_gridding_delta       = img_var.grid_ydelta
         dataset.info.gridding_interpolation = img_var.grid_interp
         dataset.info.plottype               = img_var.plottype
         dataset.info.cmapname               = img_var.cmapname
      if (eimg):
         eas_var = dat_grp.variables['easting_image']
         dataset.data.easting_image          = np.array(eas_var)
         dataset_info_easting_units          = eas_var.units # ...TBD...
         dataset_info_easting_nanval         = eas_var.missing_value
      if (nimg):
         nor_var = dat_grp.variables['northing_image']
         dataset.data.northing_image         = np.array(nor_var)
         dataset_info_northing_units         = nor_var.units # ...TBD...
         dataset_info_northing_nanval        = nor_var.missing_value

      # Read dataset georef data #####################################
      geo_grp = fileroot.groups["GeoRefSystem"]
      dataset.georef.active            = (geo_grp.active == 1)
      if (dataset.georef.active):
         dataset.georef.refsystem      = geo_grp.refsystem
         dataset.georef.utm_zoneletter = geo_grp.utm_zoneletter
         dataset.georef.utm_zonenumber = geo_grp.utm_zonenumber
         ptu_var = geo_grp.variables["pts_number"]
         pte_var = geo_grp.variables["pts_easting"]
         ptn_var = geo_grp.variables["pts_northing"]
         pta_var = geo_grp.variables["pts_abs"]
         pto_var = geo_grp.variables["pts_ord"]
         for p in range(len(geo_grp.dimensions["point"])):
#           dataset.georef.points_list.append(GeoRefPoint(easting=pue_var[p], northing=pun_var[p]))
            dataset.georef.points_list.append([ptu_var[p], pte_var[p], ptn_var[p], pta_var[p], pto_var[p]])

      # Close netcdf file ############################################
      fileroot.close()

   return 0



def to_netcdf(dataset, filename, description=None):
   '''
   cf. dataset.py

   returned error codes:

   :0: no error

   '''
   # netCDF does not support "None" values ###########################
   if (description == None):
      description = 'nil'
   if (dataset.data.z_image == None):
      dataset.interpolate()

   # Open file for writing ###########################################
   # 'w' means write (and clobber !), or create if necessary
   # 'a' means append (does not create !)
   fileroot = nc4.Dataset(filename, "w", format="NETCDF4")

   # Create root attributes ##########################################
   fileroot.description = description
   fileroot.filename    = filename
   fileroot.history     = "Created " + time.ctime(time.time())
   fileroot.os          = platform.uname()
   fileroot.author      = os.getlogin()
   fileroot.source      = geophpy.__software__ + ' ' + geophpy.__version__ + ' of ' + geophpy.__date__
   fileroot.version     = "netCDF " + nc4.getlibversion()

   # Create data group ###############################################
   dat_grp = fileroot.createGroup("Data")
   val_len = len(dataset.data.values)
   val_dim = dat_grp.createDimension("value", val_len)
   val_typ = dataset.data.values.dtype
   f = 0
   for field in [f.replace('/','\\') for f in dataset.data.fields]:
      val_var = dat_grp.createVariable(field, val_typ, ("value",))
      val_var.units     = 'nil' # ...TBD...
      val_var[:]        = dataset.data.values[:,f]
      f += 1
   if (dataset.data.z_image != None):
      nx, ny  = dataset.data.z_image.shape
      abs_dim = dat_grp.createDimension("x", nx)
      ord_dim = dat_grp.createDimension("y", ny)
      img_typ = dataset.data.z_image.dtype
      img_var = dat_grp.createVariable("z_image", img_typ, ("x","y",))
      img_var.units        = 'nil' # ...TBD...
      img_var.missing_value= np.nan
      img_var.x_min        = dataset.info.x_min
      img_var.x_max        = dataset.info.x_max
      img_var.y_min        = dataset.info.y_min
      img_var.y_max        = dataset.info.y_max
      img_var.z_min        = dataset.info.z_min
      img_var.z_max        = dataset.info.z_max
      img_var.grid_xdelta  = dataset.info.x_gridding_delta
      img_var.grid_ydelta  = dataset.info.y_gridding_delta
      img_var.grid_interp  = dataset.info.gridding_interpolation
      img_var.plottype     = dataset.info.plottype
      img_var.cmapname     = dataset.info.cmapname
      img_var[...]         = dataset.data.z_image[...]
   if (dataset.data.easting_image != None):
      eas_typ = dataset.data.easting_image.dtype
      eas_var = dat_grp.createVariable("easting_image", eas_typ, ("x","y",))
      eas_var.units        = 'nil' # ...TBD...
      eas_var.missing_value= np.nan
      eas_var[...]         = dataset.data.easting_image[...]
   if (dataset.data.northing_image != None):
      nor_typ = dataset.data.northing_image.dtype
      nor_var = dat_grp.createVariable("northing_image", nor_typ, ("x","y",))
      nor_var.units        = 'nil' # ...TBD...
      nor_var.missing_value= np.nan
      nor_var[...]         = dataset.data.northing_image[...]

   # Create georefsys group ##########################################
   geo_grp = fileroot.createGroup("GeoRefSystem")
   if (dataset.georef.active):
      geo_grp.active         = 1
      geo_grp.refsystem      = dataset.georef.refsystem
      geo_grp.utm_zoneletter = dataset.georef.utm_zoneletter
      geo_grp.utm_zonenumber = dataset.georef.utm_zonenumber
      pts_len = len(dataset.georef.points_list)
      pts_dim = geo_grp.createDimension("point", pts_len)
      ptu_var = geo_grp.createVariable("pts_number",   "i", ("point",))
      pte_var = geo_grp.createVariable("pts_easting",  "d", ("point",))
      ptn_var = geo_grp.createVariable("pts_northing", "d", ("point",))
      pta_var = geo_grp.createVariable("pts_abs",      "d", ("point",))
      pto_var = geo_grp.createVariable("pts_ord",      "d", ("point",))
      p = 0
      for [pts_number, pts_easting, pts_northing, pts_abs, pts_ord] in dataset.georef.points_list:
         ptu_var[p] = pts_number
         pte_var[p] = pts_easting
         ptn_var[p] = pts_northing
         pta_var[p] = pts_abs
         pto_var[p] = pts_ord
         p += 1
   else:
      geo_grp.active      = 0

   # Close file ######################################################
   fileroot.close()

   # Return error code ###############################################
   return 0
