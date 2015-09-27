# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import sys

with open('README.rst') as f:
    description = f.read()

setup(
    name='seamless',
    url='http://github.com/emulbreh/seamless/',
    version='0.1.0',
    packages=find_packages(),
    license=u'BSD',
    author=u'Johannes Dollinger',
    author_email=u'emulbreh@googlemail.com',
    long_description=description,
    include_package_data=True,
    install_requires=[
        'click',
        'itsdangerous',
        'requests',
    ],
    entry_points={
        'console_scripts': ['seamless = seamless.cli:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]
)
