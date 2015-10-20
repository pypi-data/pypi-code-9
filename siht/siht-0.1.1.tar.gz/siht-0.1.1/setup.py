#!/usr/bin/env python
# coding=utf-8
b'This library requires pypy or Python 2.6, 2.7, 3.3, pypy or newer'
import io
import os
from setuptools import setup


def get_path(*args):
    return os.path.join(os.path.dirname(__file__), *args)


def read_from(filepath):
    with io.open(filepath, 'rt', encoding='utf8') as f:
        return f.read()


readme = read_from(get_path('README.rst'))


setup(
    name='siht',
    version='0.1.1',
    author='Juan-Pablo Scaletti',
    author_email='juanpablo@lucumalabs.com',
    include_package_data=True,
    zip_safe=True,
    url='https://github.com/jpscaletti/siht',
    license='MIT license',
    description='An anti-explicit manifesto',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
