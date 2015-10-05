#-----------------------------------------------------------------------------
# Copyright (c) 2005-2015, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


__all__ = ('HOMEPATH', 'PLATFORM', '__version__')

import os
import sys

from . import compat
from .compat import is_darwin, is_win, is_py2
from .utils.git import get_repo_revision


# Note: Keep this variable as plain string so it could be updated automatically
#       when doing a release.
__version__ = '3.0.dev6'


# This ensures for Python 2 that PyInstaller will work on Windows with paths
# containing foreign characters.
HOMEPATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if is_win and is_py2:
    try:
        unicode(HOMEPATH)
    except UnicodeDecodeError:
        # Do conversion to ShortPathName really only in case HOMEPATH is not
        # ascii only - conversion to unicode type cause this unicode error.
        try:
            import win32api
            HOMEPATH = win32api.GetShortPathName(HOMEPATH)
        except ImportError:
            pass

## Default values of paths where to put files created by PyInstaller.
## Mind option-help in build_main when changes these
# Folder where to put created .spec file.
DEFAULT_SPECPATH = compat.getcwd()
# Folder where to put created .spec file.
# Where to put the final app.
DEFAULT_DISTPATH = os.path.join(compat.getcwd(), 'dist')
# Where to put all the temporary work files, .log, .pyz and etc.
DEFAULT_WORKPATH = os.path.join(compat.getcwd(), 'build')


PLATFORM = compat.system() + '-' + compat.architecture()
# Include machine name in path to bootloader for some machines.
# e.g. 'arm'
if compat.machine():
    PLATFORM += '-' + compat.machine()
