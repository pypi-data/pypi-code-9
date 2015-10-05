#!/usr/bin/env python

# Copyright (c) 2014 Johnny Wezel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(
    name='jw.grbackup',
    version='0.7.1',
    platforms='POSIX',
    url='https://pypi.python.org/pypi/jw.grbackup',
    license='GPL',
    author='Johnny Wezel',
    author_email='dev-jay@wezel.name',
    description='Gentoo rsync backup -- a simple differential backup script for Gentoo Linux',
    long_description=open('README.rst').read(),
    keywords='backup, utility',
    install_requires=[
        'setuptools>=3',
        'PyYAML',
        'sortedcontainers',
        'paramiko',
        'future'
    ],
    packages=find_packages(),
    namespace_packages=['jw'],
    entry_points={
        'console_scripts': [
            'grbackup = jw.grbackup.main:Main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Archiving :: Mirroring',
        'Topic :: Utilities'
    ]
)

