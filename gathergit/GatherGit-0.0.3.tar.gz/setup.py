#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

from distutils.core import setup
import os, sys

setup(name='GatherGit',
      author='Arnold Bechtoldt',
      author_email='mail@arnoldbechtoldt.com',
      description='Gather Git Repositories together to one large file tree',
      install_requires = ['pyyaml', 'sh', 'gitpython'],
      license='Apache 2.0',
      packages=['gathergit'],
      scripts=['bin/gathergit'],
      url='https://github.com/bechtoldt/GatherGit',
      version='0.0.3',
      data_files=[
        ('usr/share/gathergit/config.dist', ['config.dist/settings.yaml', 'config.dist/deployments.yaml']),
      ],
     )
