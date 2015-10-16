# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='edeposit.app.fields',
      version=version,
      description="Custom Plone fields and widgets for eDeposit project",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author=u'Jan Stavěl',
      author_email='stavel.jan@gmail.com',
      url='https://github.com/edeposit/edeposit.app.fields',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['edeposit', 'edeposit.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.dexterity [grok,relations]',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
