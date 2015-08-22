# Copyright (C) 2015 Real Time Enterprises, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.txt')).read()
version = open(os.path.join(here, 'version.txt')).read().strip()


setup(
    name='check_filemaker',
    version=file('version.txt').read().strip(),
    description='Nagios plugin for monitoring FileMaker',
    long_description=README + '\n\n' + CHANGELOG,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ],
    keywords='Nagios plugin monitoring FileMaker',
    author='Bob Tanner',
    author_email='tanner@real-time.com',
    url='https://github.com/basictheprogram/check_filemaker',
    download_url='http://pypi.python.org/pypi/check_filemaker',
    license='GPL',
    py_modules=['check_filemaker'],
    zip_safe=False,
    test_suite='check_filemaker.tests',
    install_requires=[
        'PyFileMaker',
        'requests',
    ],
)
