#!/usr/bin/env python2
# coding=utf-8
"""Setup script for picklejar Python module"""

from setuptools import setup

setup(name='picklejar',
      version='1.1',
      description='Read and write multiple pickles to a single file',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='https://bitbucket.org/isaiah1112/picklejar',
      py_modules=['picklejar'],
      license='GNU Lesser General Public License v3 or later (LGPLv3+)',
      install_requires=['dill>=0.2.4',
                        ],
      platforms='any',
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      )
