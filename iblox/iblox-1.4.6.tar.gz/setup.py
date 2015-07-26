#!/usr/bin/env python2
# coding=utf-8
"""Setup file for iblox module"""

from setuptools import setup

setup(name='iblox',
      version='1.4.6',
      description='Python Infoblox WAPI Module',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='https://bitbucket.org/isaiah1112/infoblox',
      py_modules=['iblox'],
      license='GNU Lesser General Public License v3 or later (LGPLv3+)',
      install_requires=['simplejson>=3.6.5',
                        'requests>=2.7.0',
                        ],
      platforms='any',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Development Status :: 5 - Production/Stable',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
