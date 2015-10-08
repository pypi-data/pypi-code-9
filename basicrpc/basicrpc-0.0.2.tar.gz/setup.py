#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    basicrpc
    ~~~~~
    authors: Jude Nelson and Muneeb Ali
    license: MIT, see LICENSE for more details.
"""

from setuptools import setup, find_packages

setup(
    name='basicrpc',
    version='0.0.2',
    url='https://github.com/muneeb-ali/basicrpc',
    license='MIT',
    author='Jude Nelson and Muneeb Ali',
    author_email='support@onename.com',
    description='A very simple Python RPC client',
    keywords='rpc client server netstring',
    packages=find_packages(),
    download_url='https://github.com/muneeb-ali/basicrpc/archive/master.zip',
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
