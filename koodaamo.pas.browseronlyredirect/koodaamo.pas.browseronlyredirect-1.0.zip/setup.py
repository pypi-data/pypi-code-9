# -*- coding: utf-8 -*-
"""
This module contains the tool of koodaamo.pas.browseronlyredirect
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n')

setup(name='koodaamo.pas.browseronlyredirect',
      version=version,
      description="CookieAuthHelper to redirect only if user agent is a real browser",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Petri Savolainen',
      author_email='petri.savolainen@koodaamo.fi',
      url='http://github.com/koodaamo/koodaamo.pas.browseronlyredirect',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['koodaamo', 'koodaamo.pas'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      entry_points="""
      # -*- entry_points -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
