#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

setup(
    name='ssend',
    version="0.1.3",
    description="Send messages to a room/user in slack from the command line",
    url="https://github.com/sarlalian/ssend",
    install_requires=[ 'slacker >= 0.7.0' ],
    license="MIT",
    author='Will L. Fife',
    author_email='sarlalian+pip@gmail.com',
    packages=['slacksender'],
    entry_points={
        'console_scripts': [
            'ssend=slacksender:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
