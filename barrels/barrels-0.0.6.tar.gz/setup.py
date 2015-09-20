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
import barrels

setup(
    name='barrels',
    version=str(barrels.__version__),
    description='Instead of tarballs, barrels of files',
    long_description=description,
    author='oskarnyqvist',
    author_email='oskarnyqvist@gmail.com',
    url='https://github.com/oskarnyqvists/barrels',
    license=license,
    packages=find_packages(exclude=('tests')),
)
