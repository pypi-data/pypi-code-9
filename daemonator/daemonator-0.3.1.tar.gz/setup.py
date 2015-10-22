#!/usr/bin/env python
# encoding: utf-8
import sys
from os import path
from distutils.core import setup
from distutils.util import get_platform

"""Verify Python platform is Linux."""
platform = get_platform()
if platform.startswith('linux') == False:
    sys.stderr.write("Daemon-Python is not compatible with %s\n" % platform)
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

"""Determine appropriate Python version for installation."""
if sys.version_info >= (3,):
    package_dir = {'': 'src/3.x.x'}
else:
    package_dir = {'': 'src/2.x.x'}

setup(
    name='daemonator',
    version='0.3.1',
    description='Lightweight and no-nonsense POSIX daemon library for Python (2.x.x/3.x.x)',
    long_description=long_description,
    author='Fredrick Galoso - Stackd, LLC',
    license='MIT/X11',
    platforms='Linux',
    url='https://github.com/flaviocpontes/daemonator',
    download_url='https://github.com/flaviocpontes/daemonator/tarball/0.3.1',
    package_dir=package_dir,
    py_modules=[
        'daemon',
        ],
)