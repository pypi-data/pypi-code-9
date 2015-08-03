from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='bst.pygasus.core',
      version=version,
      description="Pygasus web framework working with ExtJs",
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

      keywords='pygasus web framework extjs',
      author='codeix',
      author_email='samuel.riolo@biel-bienne.ch',
      url='https://github.com/bielbienne/bst.pygasus.core',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['bst', 'bst.pygasus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bst.pygasus.wsgi',
          'bst.pygasus.resources',
          'bst.pygasus.scaffolding',
          'bst.pygasus.datamanager',
          'bst.pygasus.security',
          'bst.pygasus.i18n',
          'js.extjs',
          'martian',
          'grokcore.component',
          'zope.interface',
          'Genshi'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
