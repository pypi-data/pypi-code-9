#!/usr/bin/env python3
from distutils.core import setup

setup(name='qudth',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Estimate the distributions of line lengths of files.',
      url='http://dada.pink/qudth/',
      packages=['qudth'],
      install_requires = ['sparkprob>=0.1'],
      version='0.0.2',
      license='LGPL',
      entry_points = {'console_scripts': ['qudth = qudth.cli:cli']},
)
