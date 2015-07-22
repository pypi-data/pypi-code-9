#!/usr/bin/python 
# -*- coding: utf-8 -*-
'''
Created on 2015-7-21

@author: wangfang
'''

'''


EpistaSim_Linux



'''
import codecs
import os
import sys
from setuptools import setup, find_packages




# Get the long description from the relevant file
def read(fname):
    
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "EpistaSim_Linux"
PACKAGES = ["ForWard","BackWard"]
DESCRIPTION = " Simulator of Single nucleotide polymorphism (SNP) patetrn in a region from two loci through forward and coalescent process with mutation and recombination under selection model"
LONG_DESCRIPTION = read("DESCRIPTION.rst")
KEYWORDS = "epistasis simulation"
AUTHOR = "Shaojun Zhang"
AUTHOR_EMAIL = "zhangsahojun@ems.hrbmu.edu.cn"
URL = "http://blog.useasp.net/"
VERSION = "1.1.0"
LICENSE = "MIT"
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Python Software Foundation License',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Unix',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    py_modules = PACKAGES
)
 