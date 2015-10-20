#!/usr/bin/env python
# coding=utf-8
b'This library requires pypy or Python 2.6, 2.7, 3.3, pypy or newer'
import io
import os
import re
from setuptools import setup, find_packages


def get_path(*args):
    return os.path.join(os.path.dirname(__file__), *args)


def read_from(filepath):
    with io.open(filepath, 'rt', encoding='utf8') as f:
        return f.read()


data = read_from(get_path('siht.py'))
version = re.search(u"__version__\s*=\s*u?'([^']+)'", data).group(1).strip()
readme = read_from(get_path('README.rst'))


setup(
    name='siht',
    version=version,
    author='Juan-Pablo Scaletti',
    author_email='juanpablo@lucumalabs.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    url='http://jpscaletti.com',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
