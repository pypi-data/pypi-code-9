# -*- coding: utf-8 -*-
#
# Copyright © 2009-2013 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
formlayout
==========

Module for creating Qt form dialogs/layouts to edit various type of parameters,
compatible with both PyQt4 and PySide

Copyright © 2009-2013 Pierre Raybaut
This software is licensed under the terms of the GNU General Public
License version 2 as published by the Free Software Foundation.
"""

import formlayout as module
name = 'formlayout'
version = module.__version__
py_modules = ['formlayout']
package_data = {}
description = 'Module for creating Qt form dialogs/widgets to edit various type of parameters, compatible with both PyQt4 and PySide'
keywords = 'PyQt4 PySide GUI'
classifiers = ['Development Status :: 5 - Production/Stable']

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
      name = name,
      version = version,
      description = description,
      download_url = 'http://%s.googlecode.com/files/%s-%s.zip' % (name, name, version),
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
