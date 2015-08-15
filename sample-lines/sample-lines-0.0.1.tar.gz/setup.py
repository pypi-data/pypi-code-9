#!/usr/bin/env python3
from distutils.core import setup

setup(name='sample-lines',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Sample lines from a file.',
      url='http://dada.pink/sample-lines/',
      py_modules=['sample_lines'],
      version='0.0.1',
      license='LGPL',
      entry_points = {'console_scripts': ['sample-lines = sample_lines:main']},
)
