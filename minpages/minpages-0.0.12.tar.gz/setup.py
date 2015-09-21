#!/usr/bin/env python
from __future__ import print_function

from glob import glob
from setuptools import setup, find_packages

setup(
        name = 'minpages',
        version = '0.0.12',
        description = 'An abbreviated man-pages', 
        long_description = """
A simple way to make a man page or add a reminder""",
        url = 'http://github.com/brian-bk/minpages/',
        license='GPL',
        author = 'Brian Kleszyk',
        author_email = 'bkleszyk@gmail.com',
        packages = find_packages(),
        package_dir={'minpages':'minpages'},
        package_data={'minpages':['pages/*']},
        entry_points = {
            'console_scripts': [
                'min = minpages.min:main'
            ]
        },
        install_requires=['click']
)


