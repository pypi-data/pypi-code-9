#!/usr/bin/env python3
from setuptools import setup, find_packages
setup(
    name = 'rn',
    version = '1.0.1',
    description = 'Easy multiple renaming command',
    long_description = 'A UNIX style renaming program for the console.',
    url = 'https://testpypi.python.org/pypi/rn',
    author = 'Jose M. Casarejos',
    author_email = 'rn-program@mundo-r.com',
    license = 'GPLv3',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration',
        ],
    keywords = 'multiple batch file rename renaming utilities console shell',
    scripts = ['rn/rn']
    )
