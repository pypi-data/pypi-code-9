#! python
#-*- coding: utf-8 -*-
#
# Copyright 2013-2014 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
''''The *pandalon-xlsutils* utilities are based on *xlwings* and interface with excel workbooks.


Install:
========
To install directly from a PIP repository:: 

    pip install pandalon

or assuming you have downloaded and `cd` into the sources::

    python setup.py install .
'''
## Got ideas for project-setup from many places, among others:
#    http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
#    http://python-packaging-user-guide.readthedocs.org/en/latest/current.html

import os, sys, io
import re

from setuptools import setup


## Fail early in ancient python-versions
#
proj_name = 'pandalon-xlsutils'
mydir = os.path.dirname(__file__)



## Version-trick to have version-info in a single place,
## taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
##
def read_project_version(verfile):
    fglobals = {}
    with io.open(os.path.join(mydir, verfile)) as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals['__version__']

def read_text_lines(fname):
    with io.open(os.path.join(mydir, fname)) as fd:
        return fd.readlines()

proj_ver = read_project_version('xlsutils.py')


description = __doc__[1]
long_desc = __doc__
## Trick from: http://peterdowns.com/posts/first-time-with-pypi.html
download_url = 'https://github.com/ankostis/%s/tarball/v%s' %(proj_name, proj_ver)

setup(
    name = proj_name,
    version=proj_ver,
    description=description,
    long_description=long_desc,
    author="Kostis Anagnostopoulos @ European Commission (JRC)",
    author_email="ankostis@gmail.com",
    url = "https://github.com/ankostis/%s" % proj_name,
    download_url=download_url,
    license = "European Union Public Licence 1.1 or later (EUPL 1.1+)",
    keywords = [
         "programming", "interoperation", "excel", "data",
    ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 3 - Alpha",
        'Natural Language :: English',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Pre-processors",
    ],
    packages = ['xlsutils.py'],
    package_data= {'': ['*.vba']},
    include_package_data = True,
    install_requires = [
        'xlwings',
        #'xlwings == 0.2.3',     # For Excel integration
        'easygui',
    ],
    setup_requires = [
    ],
    tests_require = [
        'nose',
    ],
    extras_require = {
    },
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'xlsutils = xlsutils:main',
        ],
    }, 
    zip_safe=True,
    options={
        'build_sphinx' :{
            'build_dir': 'docs/_build',
        },
        'bdist_wheel' :{
            'universal': True,
        },
    }
)



