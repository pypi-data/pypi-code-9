#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.bitbucket@metagriffin.net>
# date: 2015/10/15
# copy: (C) Copyright 2015-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import sys, os, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kw):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kw.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.5.3',
]

dependencies = [
  'mercurial            >= 2.8.2',
]

extras_dependencies = {
  'yaml': 'PyYAML       >= 3.11',
}

entrypoints = {
}

classifiers = [
  'Development Status :: 4 - Beta',
  # 'Development Status :: 5 - Production/Stable',
  # 'Development Status :: 6 - Mature',
  # 'Development Status :: 7 - Inactive',
  'Environment :: Console',
  'Intended Audience :: Developers',
  'Natural Language :: English',
  'Operating System :: OS Independent',
  'Programming Language :: Python',
  'Topic :: Software Development',
  'Topic :: Software Development :: Version Control',
  'Topic :: Utilities',
  'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
]

setup(
  name                  = 'hg_fingerprint',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'Better archive fingerprint file composition.',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'metagriffin',
  author_email          = 'mg.pypi@uberdev.org',
  url                   = 'https://bitbucket.org/metagriffin/hg-fingerprint',
  keywords              = 'mercurial hg version control archive fingerprint text json yaml xml',
  packages              = find_packages(),
  platforms             = ['any'],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  extras_require        = extras_dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'hg_fingerprint',
  entry_points          = entrypoints,
  license               = 'GPLv3+',
)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
