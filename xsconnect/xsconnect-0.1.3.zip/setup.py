#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

import xsconnect

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # No extra packages are needed.
]

test_requirements = [  # TODO: put package test requirements here
]

setup(
    name='xsconnect',
    version=xsconnect.__version__,
    description=
    "Generate pin assignment constraints for a given combination of XESS peripheral + motherboard + daughterboard.",
    long_description=readme + '\n\n' + history,
    author=xsconnect.__author__,
    author_email=xsconnect.__email__,
    url='https://github.com/xesscorp/xsconnect',
#    packages=['xsconnect', ],
    packages=setuptools.find_packages(),
    package_dir={'xsconnect': 'xsconnect'},
    entry_points={
        'console_scripts':[
            'xsconn = xsconnect.xsconn:xsconn',
            'xsconnect = xsconnect.xsconn:xsconn',
        ],
        'gui_scripts':[
            'gxsconn = xsconnect.gxsconn:gxsconn',
            'gxsconnect = xsconnect.gxsconn:gxsconn',
        ],
    },
# Don't set include_package_data to True! Then it only includes data files under version control.
#    include_package_data=True,
    package_data={'xsconnect': ['*.gif', '*.png']},
#    scripts=['scripts/xsconn.py', 'scripts/gxsconn.py', 'scripts/xsconn.cmd', 'scripts/gxsconn.cmd'],
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='xsconnect',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 "Programming Language :: Python :: 2",
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7', ],
    test_suite='tests',
    tests_require=test_requirements)
