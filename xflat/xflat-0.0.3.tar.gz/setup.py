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
    name='xflat',
    version="0.0.3",
    description='Flattens xml/html documents',
    long_description=description,
    author='oskarnyqvist',
    author_email='oskarnyqvist@gmail.com',
    url='https://github.com/oskarnyqvists/xflat',
    license=license,
    packages=find_packages(exclude=('tests')),
)
