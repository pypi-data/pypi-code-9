#!/usr/bin/python
import glob
import sys
import os
import xml.etree.ElementTree as ET
import argparse

def replace_vtm_sources(old_pvsm_file, new_pvsm_file, newfiles, sort=True):
    """
    replace all data files in: old_pvsm_file
    with the data files in: newfiles  (e.g. sorted(glob.glob('./RESULT/*.vtm')))
    and put the result in: new_pvsm_file
    """
    if not isinstance(newfiles, list):
      newfiles = [newfiles] # make the function behave the same way as with a list

    tree=ET.parse(old_pvsm_file)
    root=tree.getroot()

    sources = root.find(".//Proxy[@group='sources'][@type='XMLMultiBlockDataReader']")

    filename = sources.find("./Property[@name='FileName']")
    filenameinfo = sources.find("./Property[@name='FileNameInfo']")


    oldfiles = filename.findall("./Element")

    #remove references to old files
    for elem in oldfiles:
        filename.remove(elem)

    #add new elements
    if sort:
      enum = enumerate(sorted(newfiles))
    else:
      enum = enumerate(newfiles)

    for i, name in enum:
        newfile = ET.SubElement(filename, 'Element')
        newfile.set('index',str(i))
        newfile.set('value',name)

    # Set the current view to the last file of the list
    filenameinfo.find('./Element').set('value', newfiles[-1])

    filename.set('number_of_elements',str(len(newfiles)))


    tree.write(new_pvsm_file)

def remove_end_time(pvsm_file):
    tree=ET.parse(pvsm_file)
    root=tree.getroot()
    source = root.find(".//Proxy[@group='animation'][@type='AnimationScene']")
    filename = source.find("./Property[@name='EndTime']")
    oldfiles = filename.findall("./Element")
    #remove references to old files
    for elem in oldfiles:
        filename.remove(elem)

    tree.write(pvsm_file)
 

parser = argparse.ArgumentParser(description='Open paraview for project')
parser.add_argument('path', metavar='path', type=str, help='path of the case folder')

args = parser.parse_args()
case_folder = args.path

path_name = os.path.join( case_folder,"*.pvsm")
pvsm_files = glob.glob(path_name)

files = os.path.join(case_folder, 'RESULT')
files = os.path.join(files, '*.vtm')
files = glob.glob(files)

if files == []:
  print "no result files"

elif pvsm_files == []:
  data = os.path.basename(files[0]).split('.')[0]
  if len(files)>1:
    data = data+'...vtm'
  else:
    data = files[0]
  data = os.path.join( os.path.dirname(files[0]), data )
  os.system( "paraview --data="+data)
else:
  for pvsm_file in pvsm_files:
    original = pvsm_file+"_original"
    new      = pvsm_file
    os.rename(new, original)
    replace_vtm_sources(original,new,sorted(files))
    # temporary bugfix for paraview
    remove_end_time(new)
  print new
  os.system( "paraview --state="+new)
