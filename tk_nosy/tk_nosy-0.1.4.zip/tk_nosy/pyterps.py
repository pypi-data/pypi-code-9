#!/usr/bin/env python
# -*- coding: ascii -*-

"""
PyInterpreters finds all python executable interpreters on this file system.

-------------------

Maintains a list of python interpreters on this file system.

Will execute each interpreter (via subprocess.Popen) in order to get its version number

Also executes nosetests, if present, to get its version number.


PyInterpreters
Copyright (C) 2015  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
from __future__ import print_function

# pylint: disable=R0914, R0902, R0912, R0915
# pylint: disable=C0326, C0103
# pylint: disable=W0703

# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2015 Charlie Taylor'
__license__ = 'GPL-3'
__version__ = '0.1.4'  # METADATA_RESET:__version__ = '<<version>>'
__email__ = "cet@appliedpython.com"
__status__ = "Development" # "Prototype", "Development", or "Production"

#
# import statements here. (built-in first, then 3rd party, then yours)
import sys
import os
import glob
import platform
import subprocess


GET_NOSE_VERSION_CODE = """import sys;import nose;sys.stdout.write( nose.__version__ )"""

def get_nose_version_info( python_full_exe_path ):
    """import nose in order to get the nose version number"""
    
    cmdL = [python_full_exe_path, '-c', GET_NOSE_VERSION_CODE]
    #print( 'cmd =',cmd )
    proc = subprocess.Popen(cmdL, shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    nose_version, stderr_value = proc.communicate()
    
    if nose_version:
        return  nose_version, None
    else:
        return None, stderr_value

class PyInterp(object):
    r"""PyInterp is a python executable interpreter on this file system.

    Attributes::
    
        major: major version of python interpreter
        minor: minor version of python interpreter
        micro: micro version of python interpreter
        version_str: string representation of version (ex. 2.7.9)
        is_pypy: boolean flag. True=pypy, False=CPython
        nose_version: string representation of nose version (ex. 1.3.7)
        (ex. C:\Python34\Scripts\nosetests.exe or nosetests3)

        full_path: absolute path to the interpreter
        (ex. C:\Python27\python.exe  or  /usr/bin/python3.4)
        exe_path: the path portion of full_path (ex. C:\Python27  or /usr/bin)
        exe_name: the file name portion of full_path (ex. python.exe  or python3.4)
    """

    def __init__(self, major, minor, micro, full_path):
        """Inits PyInterp."""
        self.major = major
        self.minor = minor
        self.micro = micro
        self.full_path = full_path

        self.version_str = major + '.' + minor + '.' + micro
        self.version_tuple = (int(major),  int(minor), int(micro))

        self.exe_path, self.exe_name = os.path.split( full_path )
        if self.exe_name.startswith('pypy'):
            self.is_pypy = True
        else:
            self.is_pypy = False

        self.nose_version, err_msg = get_nose_version_info( self.full_path )

    def name(self):
        """Name of interpreter is its version number
          (if PYPY then name is "PYPY " + version number)
        """
        if self.is_pypy:
            return 'PYPY ' + self.version_str
        else:
            return self.version_str

    def __str__(self):

        sL = ['Python ' + self.name()]
        sL.append( '   located at: '+ self.full_path)
        sL.append( '   nose version:' + str(self.nose_version))

        return '\n'.join(sL)


GET_PY_VERSION_CODE = """import sys;"""+\
       """major, minor, micro = sys.version_info[:3];"""+\
       """sys.stdout.write( '%s,%s,%s,%s'%(major,minor,micro,sys.executable) )"""

def get_py_version_info( python_full_exe_path ):
    """import nose in order to get the nose version number"""
    
    cmdL = [python_full_exe_path, '-c', GET_PY_VERSION_CODE]
    #print( 'cmd =',cmd )
    proc = subprocess.Popen(cmdL, shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    py_info, stderr_value = proc.communicate()
    
    
    if py_info:
        try:
            py_info = py_info.decode()
            #print('py_info=',py_info)
            #print('type(py_info) =',type(py_info))
            py_major, py_minor, py_micro, py_exe_fullpath = py_info.split(',')
            return  py_major, py_minor, py_micro, py_exe_fullpath
        except Exception:
            return None, None, None, None
    else:
        print( '='*55 )
        print( 'ERROR getting python version information' )
        print( stderr_value.strip() )
        print( '='*55 )
        return None, None, None, None


class PyInterpsOnSys(object):
    """PyInterpreters finds all python executable interpreters on this file system.

    Attributes::
    
        interpL: list of PyInterp objects
        interp2L: list of python 2 PyInterp objects
        interp3L: list of python 3 PyInterp objects
    """

    def __init__(self, extra_search_dirL=None):
        """Inits PyInterpsOnSys

           :param extra_search_dirL: extra search directories for python interpreters
           :type  extra_search_dirL: list of strings

           If extra_search_dirL is provided, the directories in the list will be searched
           for additional python interpreters.
        """
        self.interpL = []
        self.interp2L = []
        self.interp3L = []

        # Start by adding python interpreter running this py file.
        self.add_interp( sys.executable )

        # look for python in standard places
        if platform.system() == "Windows":
            dir_a_L = glob.glob(r"C:\Anaconda\python.exe")
            dirL = glob.glob(r"C:\Python??\python.exe")
            dirL.extend( dir_a_L )
        else:
            dirL = glob.glob('/usr/bin/python*')
        for pydir in dirL:
            if not pydir.endswith("m"):
                self.add_interp( pydir )

        # looke for pypy in standard places
        if platform.system()=="Windows":
            dirL = glob.glob(r"C:\pypy*\pypy.exe")
        else:
            dirL = glob.glob('/usr/bin/pypy*')
        for pydir in dirL:
            if not pydir.endswith("m"):
                if not os.path.split(pydir)[-1].startswith('pypyc'):
                    self.add_interp( pydir )


        # There might be other search directories
        if extra_search_dirL:
            for srch_dir in extra_search_dirL:
                if platform.system()=="Windows":
                    dirbase = os.path.join(srch_dir, "Python")
                    dirname = dirbase + r'??\python.exe'
                    print( 'search dirname =', dirname)

                    dirbase_pypy = os.path.join(srch_dir, "pypy")
                    dirname_pypy = dirbase_pypy + r'*\pypy.exe'
                    print( 'search dirname_pypy =', dirname_pypy)

                else:
                    dirbase = os.path.join(srch_dir, "python")
                    dirname = dirbase + '*'

                    dirbase_pypy = os.path.join(srch_dir, "pypy")
                    dirname_pypy = dirbase_pypy + '*'

                dirL = glob.glob( dirname )
                # add the extra python interpreters
                for pydir in dirL:
                    self.add_interp( pydir )

                # look for pypy also
                dirL = glob.glob( dirname_pypy )
                # add the extra python interpreters
                for pydir in dirL:
                    self.add_interp( pydir )

    def num_terps(self):
        """Return the total number of python interpreters found on system."""
        return len(self.interpL)

    def get_PI_obj_by_py_path(self, py_path):
        r"""Get a PI object using only it's full_exe_path.
          (ex. C:\Python27\python.exe  or  /usr/bin/python3.4)
        """
        for PI in self.interpL:
            if PI.full_path == py_path:
                return PI
        return None

    def get_PI_obj_by_name(self, name):
        """Get a PI object using only it's name. (ex. 3.4.5 or PYPY2.6.6)"""
        for PI in self.interpL:
            if PI.name() == name:
                return PI
        return None

    def get_PI_list(self, removeNameL=None):
        """Return a list of interpreters, but w/o any members of removeNameL."""
        if removeNameL:
            return [PI for PI in self.interpL if PI.name() not in removeNameL]
        else:
            return self.interpL[:]

    def add_interp(self, py_exe_cmd):
        """Adds a python interpreter to the collection"""

        py_major, py_minor, py_micro, py_exe_fullpath = get_py_version_info( py_exe_cmd )
        if py_major:
            for PI in self.interpL:
                if platform.system()=="Windows": # case doesn't matter on Windows
                    if PI.full_path.lower() == py_exe_fullpath.lower():
                        return PI # avoid duplication in interpreter list
                else:
                    version_str = py_major + '.' + py_minor + '.' + py_micro
                    if PI.full_path == py_exe_fullpath or version_str == PI.version_str:
                        return PI # avoid duplication in interpreter list

            PI = PyInterp(py_major, py_minor, py_micro, py_exe_fullpath)
            self.interpL.append( PI )

            if py_major=='2':
                self.interp2L.append( self.interpL[-1] )
            elif py_major=='3':
                self.interp3L.append( self.interpL[-1] )

            # sort lists by version number
            self.interpL = sorted(self.interpL, key=lambda pi: pi.version_tuple)
            self.interp2L = sorted(self.interp2L, key=lambda pi: pi.version_tuple)
            self.interp3L = sorted(self.interp3L, key=lambda pi: pi.version_tuple)

            return PI
        return None

    def __str__(self):
        sL = ['Python Interpreters on This Machine:']
        if len(self.interp2L)>0:
            sL.append('Python 2')
            for PI in self.interp2L:
                sL.append('   %-6s(nose %s) at %s'%(PI.version_str,
                                                    PI.nose_version,
                                                    PI.full_path))
        if len(self.interp3L)>0:
            sL.append('Python 3')
            for PI in self.interp3L:
                sL.append('   %-6s(nose %s) at %s'%(PI.version_str,
                                                    PI.nose_version,
                                                    PI.full_path))
        return '\n'.join(sL)


if __name__ == '__main__':
    C = PyInterpsOnSys()# extra_search_dirL=[r'D:\TOX'] )
    #for PI in C.interpL:
    #    print( PI )
    #C.add_interp( r'D:\TOX\pypy-2.6.0-win32\pypy.exe' )

    print( '='*55 )
    print( C )
