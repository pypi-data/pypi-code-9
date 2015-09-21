#!/usr/bin/env python

# Copyright (c) 2011 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from setuptools import setup, find_packages
import os
import re
import sys

# pull in some definitions from the package's __init__.py file
sys.path.insert(0, os.path.join('src', ))
import Assign_GUP

requires = Assign_GUP.__requires__
packages = find_packages()
verbose=1
long_description = open('README.rst', 'r').read()


setup (name             = Assign_GUP.__package_name__,        # Assign_GUP
       version          = Assign_GUP.__version__,
       license          = Assign_GUP.__license__,
       description      = Assign_GUP.__description__,
       long_description = long_description,
       author           = Assign_GUP.__author_name__,
       author_email     = Assign_GUP.__author_email__,
       url              = Assign_GUP.__url__,
       download_url     = Assign_GUP.__download_url__,
       keywords         = Assign_GUP.__keywords__,
       install_requires = requires,
       platforms        = 'any',
       package_dir      = {'Assign_GUP': 'src/Assign_GUP'},
       #packages         = find_packages(),
       packages         = [str(Assign_GUP.__package_name__), 
                           # do not really need to package this mock
                           'Assign_GUP.mock_PyQt4',
                           ],
       package_data     = dict(Assign_GUP=['resources/*', ]),
       classifiers      = Assign_GUP.__classifiers__,
       entry_points={
            # create & install console_scripts in <python>/bin
            # 'console_scripts': [
            #   'Assign_GUP=Assign_GUP.main:main', 
            # ],
            'gui_scripts': ['Assign_GUP=Assign_GUP.main_window:main'],
      },
  )
