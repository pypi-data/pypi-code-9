#!/usr/bin/env python
# vim: fileencoding=UTF-8 filetype=python ff=unix expandtab sw=4 sts=4 tw=120
# author: Christer Sjöholm -- goobook AT furuvik DOT net

from setuptools import setup, find_packages
import os
import versioneer

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

setup(name='hcs_utils',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description="My personal library collecting some useful snippets.",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Christer Sjöholm',
      author_email='hcs at furuvik dot net',
      url='http://pypi.python.org/pypi/hcs_utils',
      download_url='http://pypi.python.org/pypi/hcs_utils',
      packages=find_packages(),
      zip_safe=True,
      install_requires=[
          # For more details, see: http://packages.python.org/distribute/setuptools.html#declaring-dependencies
      ],
      entry_points={
          # -*- Entry points: -*-
      }
      )
