# Copyright (C) 2015 Okami, okami@fuzetsu.info

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os, sys, glob, fnmatch
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Code borrowed from wxPython's setup and config files
# Thanks to Robin Dunn for the suggestion.
# I am not 100% sure what's going on, but it works!
def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


# https://wiki.python.org/moin/Distutils/Tutorial
def find_data_files(srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    def walk_helper(arg, dirname, files):
        if '.svn' in dirname:
            return
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)

                if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                    names.append(filename)
        if names:
            lst.append((dirname, names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list


setup(**{
    'name': 'aoisora',
    'version': '0.0.2',
    'author': 'Okami',
    'author_email': 'okami@fuzetsu.info',
    'description': 'Lightweight Bluetooth manager for Bluez5 with PyQt4 UI',
    'license': 'GPLv3',
    'keywords': 'bluetooth bluez pyqt',
    'url': 'https://pypi.python.org/pypi/aoisora',
    'packages': [
        'aoisora',
        'aoisora.device',
    ],
    'scripts': ['AoiSora'],
    'long_description': '',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    'install_requires': [
    ],
    'data_files': find_data_files('share/aoisora', '*.svg', recursive=False),
    'include_package_data': True,
})
