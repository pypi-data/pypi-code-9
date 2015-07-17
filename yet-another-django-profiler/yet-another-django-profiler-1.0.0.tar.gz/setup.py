# encoding: utf-8
# Created by Jeremy Bowman on Thu Feb 20 16:54:00 EST 2014
# Copyright (c) 2014, 2015 Safari Books Online. All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-clause BSD license.  See the LICENSE file for details.
"""
yet-another-django-profiler setup script
"""

import codecs
import os
import sys
from setuptools import find_packages, setup

from yet_another_django_profiler import __version__

version = '.'.join(str(n) for n in __version__)

install_requires = [
    'Django',
]

if '{0.major}.{0.minor}'.format(sys.version_info) < '3.3':
    install_requires.append('mock')

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from pip.download import PipSession
    from pip.index import PackageFinder
    from pip.req import parse_requirements
    session = PipSession()
    root_dir = os.path.abspath(os.path.dirname(__file__))
    requirements_path = os.path.join(root_dir, 'requirements', 'documentation.txt')
    finder = PackageFinder([], [], session=session)
    requirements = parse_requirements(requirements_path, finder, session=session)
    install_requires.extend([str(r.req) for r in requirements])

with codecs.open('README.rst', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    name='yet-another-django-profiler',
    version=version,
    author='Jeremy Bowman',
    author_email='jbowman@safaribooksonline.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development',
    ],
    description='Django middleware for performance profiling directly from the browser',
    long_description=long_description,
    url='http://github.com/safarijv/yet-another-django-profiler',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    include_package_data=True,
    scripts=['gprof2dot.py'],
    zip_safe=True,
    install_requires=install_requires,
)
