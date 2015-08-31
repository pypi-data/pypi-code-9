#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""setup.py for the pyneric project"""

import os

from setuptools import find_packages, setup


THIS_DIRECTORY = os.path.dirname(__file__)

def read_file(path):
    return open(os.path.join(THIS_DIRECTORY, path)).read()

# Set __version_info__ and __version__ from the _version.py module code.
exec(read_file(os.path.join('src', 'pyneric', '_version.py')))

setup(
    name='pyneric',
    version=__version__,
    author="Craig Hurd-Rindy",
    author_email="gnuworldman@gmail.com",
    maintainer="Craig Hurd-Rindy",
    maintainer_email="gnuworldman@gmail.com",
    url='https://github.com/gnuworldman/pyneric',
    description="generic Python library",
    long_description=read_file('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['future>=0.15'],
    extras_require={'fsnotify': ['pyinotify>=0.9'],
                    'requests': ['requests'],
                    'django-pguuid': ['Django>=1.6', 'django-extensions>=1.3.0', 'psycopg2'],
                    },
    )
