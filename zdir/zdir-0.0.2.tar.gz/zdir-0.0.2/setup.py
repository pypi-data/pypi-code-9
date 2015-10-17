# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


try:
    from pypandoc import convert
    description = convert("README.md", 'rst')
except ImportError:
    description = lambda f: open(f, 'r').read()


# with open('README.rst') as f:
#     readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='zdir',
    version="0.0.2",
    description='Library for handling many small files. Packs files into directory, nameing by hash of content. ',
    long_description=description,
    author='oskarnyqvist',
    author_email='oskarnyqvist@gmail.com',
    url='https://github.com/oskarnyqvist/zdir',
    license=license,
    packages=find_packages(exclude=('tests')),
)
