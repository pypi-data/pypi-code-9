#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup
from web import __version__

long_description = """
Think about the ideal way to write a web app. Write the code to make it happen.

Improved and updated version for usage in the INGI department at Université Catholique de Louvain.
We try to keep this updated with the master branch of web.py.
"""

setup(name='web.py-INGI',
      version=__version__,
      description='Improved and updated version of web.py for usage in the INGI department at Université Catholique de Louvain',
      author='Aaron Swartz, Anand Chitipothu, INGI, Guillaume Derval',
      author_email='me@aaronsw.com, anandology@gmail.com, info@uclouvain.be, guillaume@guillaumederval.be',
      maintainer='Guillaume Derval',
      maintainer_email='guillaume@guillaumederval.be',
      url=' http://webpy.org/',
      packages=['web', 'web.wsgiserver', 'web.contrib'],
      long_description=long_description,
      license="Public domain",
      platforms=["any"],
     )
