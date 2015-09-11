# -*- coding: utf-8 -*-
"""
This module contains the tool of plone.recipe.apache
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.3.3'

long_description = (
    read('README.txt')
    + '\n' +
    read('plone', 'recipe', 'apache', 'building.txt')
    + '\n\n' +
    read('plone', 'recipe', 'apache', 'configuring.txt')
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '==============\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '========\n'
    )
entry_point = 'plone.recipe.apache:Recipe'
entry_points = {"zc.buildout": [
              "build = plone.recipe.apache:BuildRecipe",
              "config = plone.recipe.apache:ConfigureRecipe",
              #"instance = plone.recipe.apache:ConfigureRecipe",
              ]}

tests_require=['zope.testing', 'zc.buildout', 'Cheetah']

setup(name='plone.recipe.apache',
      version=version,
      description="An zc buildout for build and configure apache",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='plone recipe apache configure',
      author='Paris sprint 2008',
      author_email='products-developers@lists.plone.org',
      url='https://svn.plone.org/svn/collective/buildout/plone.recipe.apache',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        # -*- Extra requirements: -*-
                        'zc.recipe.cmmi',
                        "Cheetah>1.0,<=2.2.1",
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'plone.recipe.apache.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
