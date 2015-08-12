# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='uiside',
    version='0.1.1',
    description='Additional UI components for PySide-based applications',
    long_description=long_description,
    url='https://github.com/confluenity/uiside',
    author='Confluenity',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='pyside ui components',
    packages=find_packages(),
    install_requires=[]
)
