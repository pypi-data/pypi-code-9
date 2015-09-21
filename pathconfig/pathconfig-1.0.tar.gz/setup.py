#!/usr/bin/env python
from setuptools import setup

README_TEXT = file('README.md').read()

setup(name='pathconfig',
      version='1.0',
      description='On-demand loading and configurable paths',
      long_description =README_TEXT,
      author='Yannick Versley',
      author_email='versley@cl.uni-heidelberg.de',
      packages=['pathconfig'],
      package_dir={'': 'py_src'},
      url='https://github.com/yv/pathconfig',
      install_requires=['setuptools>=17', 'pyyaml']
      )
