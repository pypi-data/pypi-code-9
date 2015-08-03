from setuptools import setup, find_packages

version = '1.0.1'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='bst.pygasus.demo',
      version=version,
      description="Demo web application build with bst.pygausus framework",
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
      author='Steve Aschwanden',
      author_email='steve.aschwanden@biel-bienne.ch',
      url='https://github.com/bielbienne/bst.pygasus.demo',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['bst', 'bst.pygasus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bst.pygasus.core',
          'pyaml',
          'Whoosh',
          'Unidecode'
      ],
      extras_require=dict(test=['splinter']),
      test_suite='bst.pygasus.demo.tests.test_suite',
      entry_points={
          'fanstatic.libraries': ['demo = bst.pygasus.demo.extjs:library'],
      }
)
