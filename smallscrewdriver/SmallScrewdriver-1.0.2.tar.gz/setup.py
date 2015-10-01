#!/usr/bin/env python
# encoding: utf8
from setuptools import setup

setup(
    name="SmallScrewdriver",
    version="1.0.2",
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
    url="https://github.com/Ingener74/Small-Screwdriver",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: Freeware",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Editors",
    ]
)
