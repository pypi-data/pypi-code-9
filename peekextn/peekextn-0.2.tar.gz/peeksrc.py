"""
peeksrc

Peek into the sources and list the file types contained in the sources.
Also, enable display the sources in tree format.

Purpose
=======

    This tool can be used as the first step for source code reading and
    understand the basic design.
        * What are the different file types in the sources.
            * To understand file interface design.
        * Walk over specific extenstion on all directories.
        * Show directories and files with max depth level.
        * Generate header file path for doxygen

Interface
=========

    commandline
    -----------
    peeksrc
        -e [list] : Extension Lists
        -g group  : Extension group
        -l level  : File/Directory Level depth
        -u        : All unknown files
        -p        : List File extension Paths
        -d        : Destination Dir
        -t        : Directory Tree Structure
        -o        : Output File
        
    API
    ---

    source = peeksrc()
    source.showextn()


Logging and Reporting
=====================

    Console Logs and formatting
    Generate HTML report
    Generate Doxy tool input
    Generate files to pipe

DataStructures
==============

    Data Associations
        File Extens -> Files 
        File Extens -> Paths
        Directory -> File Extens -> Files

    Data Structure
        
        dirtree = ['dir1', "dir1", ..., ]

        ExtnNodes = { 
            "group1" : {
                'extn1' : {
                            'desc' : "Description",
                            'files' : 
                                    { 'dir1' : [file1, file2, file3, ...]
                                      'dir2' : [file1, file2, file3, ...]
                                    }
                            }
                'extn2' : {
                            'descr' : "Description",
                            'files' : 
                                    { 'dir1' : [file1, file2, file3, ...]
                                      'dir2' : [file1, file2, file3, ...]
                                    }
                }
            }
"""

# Release info
__author__ = 'Vadivel'
__versioninfo__ = (0, 1)
__version__ = '.'.join(map(str,__versioninfo__))
COPYRIGHT = """\
Copyright (C) 2014-2015 Vad
"""

import os
import sys
import re
import string
import collections

class  peeksrc:
    _names = ['peekextn.fileextn']
   
    def __init__(self):
        self._AllExtnNodes = collections.OrderedDict()
        self.dirtree = list()
        self.fcnt = 0
        self.fextnlist = list()
        self.destndir = os.path.abspath(os.curdir)
        self.showall = False
        self.showpath = False
        self.showdoxy = False
        self.showdirtree = False
        self.level = 0
        self.getExtnNodes()
        self.parseCmdLineOptions()

    def __del__(self):
        pass

    def __call__(self, *args, **kwargs):
        #get all extn Nodes
        self.getExtnNodes()
        self.parseCmdLineOptions()
        
    def getExtnNodes(self):
        """
        Import the File extensions and store in a member dict variable.    
        """
        for name in self._names:
            try:
                mod = __import__(name, fromlist=['open'])
            except ImportError:
                raise ImportError("import %s error" % name)
        self._AllExtnNodes = mod.AllXtens

    def addfileXtens(self, extn, srcfile, direntry, fileXtens):
        fnode = fileXtens[extn]
        if 'files' not in fnode.keys():
            fnode['files'] = collections.OrderedDict()
            if 'desc' not in fnode.keys():
                fnode['desc'] = extn
        fdir = fnode['files']
        if direntry not in fdir.keys():
            fdir[direntry] = list()
            if direntry not in self.dirtree:
                self.dirtree.append(direntry)
        if srcfile not in fdir[direntry]:
            fdir[direntry].append(srcfile)

    def appendSrcType(self, direntry, srcfile):
        marked = 0
        unknownExtn = list()
        unknownFiles = list()

        for ftype in self._AllExtnNodes.keys():
            fileXtens = self._AllExtnNodes[ftype]

            if srcfile in fileXtens.keys():
                self.addfileXtens(srcfile, srcfile, direntry, fileXtens)
                marked = 1
            index=[it.start() for it in re.finditer('[.]',srcfile)]
            if not index:
                unknownFiles.append(srcfile)
            for idx in index:
                extn = srcfile[idx+1:]
                if extn in fileXtens.keys():
                    self.addfileXtens(extn, srcfile, direntry, fileXtens)
                    marked = 1
            if (marked == 0):
                if (index) and (extn not in unknownExtn):
                    unknownExtn.append(extn)
            for extn in fileXtens.keys():
                if any(st in string.punctuation for st in extn):
                    index = [it.start() for it in re.finditer(extn,srcfile)]
                    if (len(index) > 0):
                        self.addfileXtens(extn, srcfile, direntry, fileXtens)
                        marked = 1

        if (marked == 0):
            fileXtens = self._AllExtnNodes["unknown"]
            for extn in unknownExtn:
                if extn not in fileXtens.keys():
                    fileXtens[extn] = collections.OrderedDict() 
                self.addfileXtens(extn, srcfile, direntry, fileXtens)
            for ufile in unknownFiles:
                self.addfileXtens("noextn", ufile, direntry, fileXtens)

    def createExtnNodes(self):
        """
        peek into dir and respect subdirectories
        """
        for parent, dirs, files in os.walk(self.destndir):
            for fname in files:
                filename = os.path.join(parent, fname)
                if os.path.isfile(filename):
                    direntry=parent
                    #direntry=parent.replace(self.destndir,'',len(self.destndir))
                    #direntry = os.path.basename(os.path.abspath(parent))
                    self.appendSrcType(direntry, fname)

    def showtreedir(self):
        if self.showdirtree is False:
            return

        for direntry in self.dirtree:
            print("\n",' '*4*(direntry.count(os.sep)), " %s/" %(os.path.basename(direntry)))
            for ftype in self._AllExtnNodes.keys():
                if (ftype == "unknown"):
                    assign = '?'
                else:
                    assign = '+'
                fileXtens = self._AllExtnNodes[ftype]
                for extn in fileXtens.keys():
                    enode = fileXtens[extn]
                    if 'files' not in enode.keys():
                        continue
                    if (len(self.fextnlist) > 0):
                        if (extn not in self.fextnlist):
                            continue
                    fdir  = enode['files']
                    if direntry in fdir.keys():

                        for fname in fdir[direntry]:
                            print(" ",' '*4*(direntry.count(os.sep)), "%s %s" %(assign,fname))
    
    def showfileextn(self):
        for ftype in self._AllExtnNodes.keys():
            if (ftype == "unknown"):
                assign = '?'
            else:
                assign = ':'
            fileXtens = self._AllExtnNodes[ftype]
            for extn in fileXtens.keys():
                enode = fileXtens[extn]
                if 'files' not in enode.keys():
                    continue
                if (len(self.fextnlist) > 0):
                    if (extn not in self.fextnlist):
                        continue
                desc  = enode['desc']
                fdir  = enode['files']
                if (len(fdir) > 0):
                    if self.showdoxy is True:
                        print("%-10s: %s" %(extn," ".join([str("-I"+os.path.abspath(fp)) for fp in fdir.keys()])))
                    else:
                        print( "%20s %s %s" %(extn, assign, desc))
                        if self.showpath is True:
                            for dirnode in fdir.keys():
                                print(' '*24,"+ %s/" %dirnode)

                        elif self.showall is True:
                            for dirnode in fdir.keys():
                                print(' '*24," %s/" %dirnode)
                                for files in fdir[dirnode]:
                                    print(' '*28, files)
    def showextn(self):
        self.showfileextn()
        self.showtreedir()

    def parseCmdLineOptions(self):
        level = 0
        extnlist = ""

        groups = ",".join([key for key in self._AllExtnNodes.keys()])

        from optparse import OptionParser
        usage = "usage : %prog [options]"
        version = "%prog 1.0"
        parser = OptionParser(usage=usage, version=version)

        parser.add_option("-l", "--level", action="store", type="int",
                            dest="level", default=0,
                            help="Level to which to show the files")
        parser.add_option("-a", "--showall", action="store_true",
                            dest="showall", default=False,
                            help="Show all files")
        parser.add_option("-e", "--extn", action="store", type="string",
                            dest="extnlist",
                            help="List of files for extension")
        parser.add_option("-g", "--group", action="store", type="string",
                            dest="extngroup", help="groups: "+groups)
        parser.add_option("-u", "--unknown", action="store_true",
                            dest="unknown", default=False,
                            help="list uknown/unsupported file extension")
        parser.add_option("-p", "--showpath", action="store_true",
                            dest="showpath", default=False,
                            help="list file xtension paths")
        parser.add_option("-d", "--destn", action="store", type="string",
                            dest="destndir",default=os.curdir,
                            help="Destination Directory")
        parser.add_option("-t", "--tree", action="store_true",
                            dest="showdirtree",default=False,
                            help="Show Directory Tree")
        parser.add_option("--doxy", action="store_true",
                            dest="showdoxy",default=False,
                            help="Path string included in doxygen")
        (options, args) = parser.parse_args()

        #print (options)

        extnlist = []
        if options.unknown is True:
            options.extngroup = "unknown"
        if options.extngroup in [key for key in self._AllExtnNodes.keys()]:
            extnlist = self._AllExtnNodes[options.extngroup].keys()

        if ((options.extngroup) and (len(extnlist) == 0)):
            print("Supported extn group are: %s" %groups)
            sys.exit()

        if options.extnlist:
            extnlist = options.extnlist.split(',')
            extnlist = [ext.strip(' ') for ext in extnlist]

        self.fextnlist = extnlist

        if options.showall is True:
            self.showall = True
            options.level = -1

        if (options.level > 0):
            self.fcnt = options.level

        if (options.destndir):
            self.destndir = options.destndir

        if (options.showdirtree is True):
            self.showdirtree = True
        if (options.showdoxy is True):
            self.showdoxy = True
            self.showpath = True
        if (options.showpath is True):
            self.showpath = True

