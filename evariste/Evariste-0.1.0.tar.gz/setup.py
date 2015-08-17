#!/usr/bin/env python3

# Copyright 2015 Louis Paternault
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

"""Installer"""

from setuptools import setup, find_packages
import codecs
import glob
import os
import sys

def readme():
    directory = os.path.dirname(os.path.join(
        os.getcwd(),
        __file__,
        ))
    with codecs.open(
        os.path.join(directory, "README.rst"),
        encoding="utf8",
        mode="r",
        errors="replace",
        ) as file:
        return file.read()

def evs_scripts():
    evs_path = os.path.join(os.path.dirname(sys.argv[0]), "evariste", "evs")
    for name in glob.iglob(os.path.join(evs_path, "*")):
        if os.path.isdir(name):
            name = os.path.basename(name)
        elif name.endswith(".py"):
            name = os.path.basename(name)[0:-3]
        else:
            continue
        bin = os.path.join(
            "bin",
            "evs-{}".format(name),
            )
        if os.path.isfile(bin) and os.access(bin, os.X_OK):
            yield os.path.basename(bin), name

setup(
        name='Evariste',
        version="0.1.0",
        packages=find_packages(exclude=["test*"]),
        setup_requires=["hgtools"],
        install_requires=[
            "jinja2",
            "docutils",
            "pygit2==0.22",
            "unidecode",
            ],
        include_package_data=True,
        author='Louis Paternault',
        author_email='spalax@gresille.org',
        description='TODO',
        url='https://git.framasoft.org/spalax/evariste',
        license="AGPLv3 or any later version",
        test_suite="test.suite",
        entry_points={
            'console_scripts':
                [
                    'evariste = evariste.main:main',
                    'evs = evariste.evs:main',
                ]
                +
                [
                    '{} = evariste.evs.{}:main'.format(bin, name)
                    for bin, name
                    in evs_scripts()
                    ]
                },
        classifiers=[ # TODO
            "Development Status :: 1 - Planning",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ],
        long_description=readme(),
        zip_safe = False,
)
