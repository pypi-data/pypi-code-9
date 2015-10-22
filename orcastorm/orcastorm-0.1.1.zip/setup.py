#!/usr/bin/env python
from distutils.core import setup
from orcastorm import __version__

setup(name='orcastorm',
      version=__version__,
      description='Asnychronous two factor authentication client for Saaspass with Tornado',
      long_description="""Provides a simple module that can be used from a Tornado server to authenticate users """ +
                       """ with various authentication methods provided by www.saaspass.com""",
      author='László Zsolt Nagy',
      author_email='nagylzs@gmail.com',
      license="GNU LGPLv3",
      py_modules=['orcastorm'],
      requires=['tornado (>=4.3)'],
      url="https://bitbucket.org/nagylzs/orcastorm",
      classifiers=[
            'Topic :: Security', 'Topic :: Internet :: WWW/HTTP',
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: Implementation :: CPython",
            ],
      )
