#!/usr/bin/env python3
from distutils.core import setup

setup(name='lcw',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Estimate the number of lines in a file.',
      url='http://dada.pink/lcw/',
      packages=['lcw'],
      version='0.0.2',
      license='LGPL',
      entry_points = {'console_scripts': ['lcw = lcw.cli:main']},
)
