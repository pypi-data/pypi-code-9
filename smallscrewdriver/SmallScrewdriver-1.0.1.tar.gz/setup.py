#!/usr/bin/env python
# encoding: utf8
from setuptools import setup, find_packages

setup(
    name="SmallScrewdriver",
    version="1.0.1",
    packages=['SmallScrewdriver', 'ScreamingMercury'],
    scripts=['ScreamingMercury.py', 'SundaysIron.py'],
    install_requires=['PySide>=1.2.1',
                      'SillyCrossbow>=1.0.8'],
    package_data={
        '': ['*.txt', '*.rst', 'ScreamingMercury/*.png']
    },
    author="Shnaider Pavel",
    author_email="shnaiderpasha@gmail.com",
    description="""
    SmallScrewdriver is python texture packer library, with frontend's on PySide GUI, Flask/React.js, and console
    """,
    license="LGPL",
    keywords="texture",
    url="https://github.com/Ingener74/Small-Screwdriver"
)
