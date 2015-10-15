# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

version = ''
with open('mission/__init__.py', 'r') as f:
    version = re.search(r'__version__\s*=\s*\'([\d.]+)\'', f.read()).group(1)

if not version:
    raise RuntimeError('Couldn\'t find version string')

with open('README.rst') as f:
    readme = f.read()

setup(
    name='polyrents-challenge',
    version=version,
    author='Nick Frost',
    author_email='nickfrostatx@gmail.com',
    description='Application security challenge',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'redis',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Security',
    ],
)
