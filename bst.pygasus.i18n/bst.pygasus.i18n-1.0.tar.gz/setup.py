from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='bst.pygasus.i18n',
      version=version,
      description="provide translations for bst.pygasus framework",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'License :: OSI Approved :: Zope Public License',
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta'
      ],
      rds='',
      author='codeix',
      author_email='samuel.riolo@biel-bienne.ch',
      url='https://github.com/bielbienne/bst.pygasus.i18n',
      keywords='pygasus web framework extjs',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['bst', 'bst.pygasus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'fanstatic',
          'zope.i18n',
          'python-gettext',
      ],
      entry_points='''
          [fanstatic.libraries]
          i18n = bst.pygasus.i18n:library

          [lingua.extractors]
          extjs = bst.pygasus.i18n.extractor:ExtjsExtractor
      '''
      )
