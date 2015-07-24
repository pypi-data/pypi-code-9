#!/usr/bin/env python3

"""Setup script for spexcript."""

import setuptools
import os

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()
    
with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setuptools.setup(
    name="spexcript",
    version='0.2',
    description="Spexcript -- easy layout for theater scripts",
    url='https://github.com/k7hoven/spexcript',
    author='Koos Zevenhoven',
    author_email='koos.zevenhoven@aalto.fi',
    packages=setuptools.find_packages(),
    long_description=(README + '\n' + CHANGES),
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],

    install_requires = REQUIREMENTS,
)

