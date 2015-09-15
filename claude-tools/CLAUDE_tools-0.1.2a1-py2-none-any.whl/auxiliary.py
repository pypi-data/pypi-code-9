'''
Created on Sep 4, 2015

@author: andrei
'''

from __future__ import print_function

import ConfigParser
import logging
import re
import tarfile
import sys
import os
import subprocess
import contextlib
from shutil import make_archive
from zipfile import ZipFile

extentions_list = ['zip']

@contextlib.contextmanager
def cd_change(tmp_location):
    cd = os.getcwd()
    os.chdir(tmp_location)
    try:
        yield
    finally:
        os.chdir(cd)

def execute(cmd, shellOutput=True):
    logger = getLogger()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    while True:
        out = p.stdout.readline()
        if out == '' and p.poll() != None:
            break
        if out != '':
            if shellOutput:
                sys.stdout.write(out)
                sys.stdout.flush()
            else:
                logger.info(out)

def seekZipForElement(zip_file, element):
        files = []
        
        with ZipFile(zip_file, 'r') as myzip:
            content_list = myzip.namelist()
            
            for content in content_list:
                if element in content:
                    files.append(content)
                    
        return files

    
def createZip(arch, root_path):
    norm_path = os.path.normpath(root_path)
    (base_dir, root_dir) = os.path.split(norm_path)
    
    make_archive(arch, 'zip', base_dir, root_dir)

def extractZip(arch, extract_dir):
    with ZipFile(arch, 'r') as myzip:
        myzip.extractall(extract_dir)

'''def extractArch(arch, directory):
    tar = tarfile.open(arch)
    tar.extractall(directory)
    tar.close()
    
def createArch(arch, directory):
    tar = tarfile.open(arch, 'w:gz')
    tar.add(directory)
    tar.close()'''

#splits the given path to a list of path elements
def splitPath(path, maxdepth=20):
    ( head, tail ) = os.path.split(path)
    return splitPath(head, maxdepth - 1) + [ tail ] \
         if maxdepth and head and head != path \
         else [ head or tail ]
         
def getRootDir(path):
    path_split = splitPath(path)
    if len(path_split) > 1:
        return path_split[0]
    else:
        return ''

#reads a file and returns a config object for the file 
def readConfig(config_file_path):
    #reading the global config file
    path = config_file_path
    config = ConfigParser.RawConfigParser()
    config.read(path)
    
    return config

#returns value of the specified option
def read_option(config, section, option):
    if not config.has_section(section):
        raise ConfigParser.ParsingError("Section %s not found" % section)
    if not config.has_option(section, option):
        raise ConfigParser.ParsingError("Section %s has no option %s" % (section, option))
    
    return config.get(section, option)

#converts string to boolean
def str2bool(v):
    return v.lower() in ("yes", "true", "True", "t", "1")

#initialize a logger object with the specified logging level
def initLogger(log_file, logging_level):
    log_pair = os.path.split(log_file)
    make_dirs(log_pair[0])
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr = logging.FileHandler(log_file)
    hdlr.setFormatter(formatter)
    
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr) 
    logger.setLevel(logging_level)
    
    return logger

def getLogger():
    return logging.getLogger(__name__)

#creates necessary non-existing directories for the specified path 
def make_dirs(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
        
#checks whether the specified file extension is in the specified extensions list
def fileNameCheck(file_name, extentions_list):
    file_name_split = file_name.split('.', 1)
    if file_name_split[1] in extentions_list and not re.search('\W+', file_name_split[0]):
        return True
    return False


import warnings as _warnings
import os as _os
import sys as _sys

from tempfile import mkdtemp

class TemporaryDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    def __init__(self, suffix="", prefix="tmp", dir=None):
        self._closed = False
        self.name = None # Handle mkdtemp raising an exception
        self.name = mkdtemp(suffix, prefix, dir)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def cleanup(self, _warn=False):
        if self.name and not self._closed:
            try:
                self._rmtree(self.name)
            except (TypeError, AttributeError) as ex:
                # Issue #10188: Emit a warning on stderr
                # if the directory could not be cleaned
                # up due to missing globals
                if "None" not in str(ex):
                    raise
                print("ERROR: {!r} while cleaning up {!r}".format(ex, self,),
                      file=_sys.stderr)
                return
            self._closed = True
#            if _warn:
#                self._warn("Implicitly cleaning up {!r}".format(self),
#                           ResourceWarning)

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def __del__(self):
        # Issue a ResourceWarning if implicit cleanup needed
        self.cleanup(_warn=True)

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(_os.listdir)
    _path_join = staticmethod(_os.path.join)
    _isdir = staticmethod(_os.path.isdir)
    _islink = staticmethod(_os.path.islink)
    _remove = staticmethod(_os.remove)
    _rmdir = staticmethod(_os.rmdir)
    _warn = _warnings.warn

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            try:
                isdir = self._isdir(fullname) and not self._islink(fullname)
            except OSError:
                isdir = False
            if isdir:
                self._rmtree(fullname)
            else:
                try:
                    self._remove(fullname)
                except OSError:
                    pass
        try:
            self._rmdir(path)
        except OSError:
            pass