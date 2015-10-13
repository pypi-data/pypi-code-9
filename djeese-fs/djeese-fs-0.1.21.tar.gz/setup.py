#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fs import __version__
from setuptools import setup, find_packages


setup(
    name='djeese-fs',
    version=__version__,
    description='A twisted based daemon file system.',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    url='https://github.com/aldryncore/djeese-fs',
    packages=find_packages(),
    license='BSD',
    platforms=['OS Independent'],
    include_package_data=True,
    install_requires=[
        'argparse>=1.2.1',
        'certifi>=0.0.8',
        'chardet>=1.0.1',
    ],
    extras_require={
        'server':  [
            'Twisted>=12.0.0',
            'zope.interface>=3.8.0',
        ],
    },
    entry_points="""
    [console_scripts]
    djeesefs = fs.cli:main
    """,
)
