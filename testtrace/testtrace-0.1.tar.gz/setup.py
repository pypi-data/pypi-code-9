#!/usr/bin/env python3
# Copyright (C) 2015 Canonical
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Testtrace setup module."""

from setuptools import setup

setup(
    name="testtrace",
    version='0.1',
    url="https://launchpad.net/testtrace/",
    py_modules=['testtrace'],
    author="Zygmunt Krynicki",
    author_email="zygmunt.krynicki@canonical.com",
    license="GPLv3",
    platforms=["POSIX"],
    description="Python TestResult subclass that does code tracing",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
    include_package_data=False,
    zip_safe=True
)
