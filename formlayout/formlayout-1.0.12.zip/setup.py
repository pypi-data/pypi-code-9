# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
formlayout
==========

Module creating PyQt4 form dialogs/layouts to edit various type of parameters

Copyright © 2009-2012 Pierre Raybaut
This software is licensed under the terms of the GNU General Public
License version 2 as published by the Free Software Foundation.
"""

import formlayout as module
name = 'formlayout'
version = module.__version__
py_modules = ['formlayout']
package_data = {}
description = 'Module creating PyQt4 form dialogs/widgets to edit various type of parameters'
keywords = 'PyQt4 GUI'
classifiers = ['Development Status :: 5 - Production/Stable',
               ]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
      name = name,
      version = version,
      description = description,
      download_url = 'http://%s.googlecode.com/files/%s-%s.tar.gz' % (name, name, version),
      author = "Pierre Raybaut",
      author_email = 'pierre.raybaut@gmail.com',
      url = 'http://code.google.com/p/%s/' % name,
      license = 'MIT',
      keywords = keywords,
      platforms = ['any'],
      py_modules = py_modules,
      package_data = package_data,
      classifiers = classifiers + [
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        ],
    )
