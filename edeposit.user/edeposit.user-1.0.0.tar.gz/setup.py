# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='edeposit.user',
      version=version,
      description="User Metadata and UX for project eDeposit",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author=u'Jan Stavěl',
      author_email='stavel.jan@gmail.com',
      url='https://github.com/edeposit/edeposit.user',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['edeposit'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.documentviewer',
          'z3c.unconfigure',
          # -*- Extra requirements: -*-
      ],
      extras_require = {
        'test': ['plone.app.testing',
                 'plone.app.robotframework',
             ]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
