from setuptools import setup, find_packages
import os

version = '1.1.0'

tests_require = [
    'AccessControl',
    'Products.ATContentTypes',
    'Products.GenericSetup',
    'archetypes.schemaextender',
    'ftw.builder',
    'ftw.testing',
    'path.py',
    'plone.app.dexterity',
    'plone.app.testing',
    'plone.directives.form',
    'plone.namedfile',
    'unittest2',
    'zope.configuration',
    ]

setup(name='ftw.jsondump',
      version=version,
      description="JSON representation for plone content",
      long_description=open("README.rst").read() + "\n" + open(
        os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
        "Environment :: Web Environment",
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw json representation serialize dump',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.jsondump',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Acquisition',
        'Products.Archetypes',
        'Products.CMFCore',
        'Zope2',
        'plone.app.blob',
        'plone.dexterity',
        'plone.uuid',
        'setuptools',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
