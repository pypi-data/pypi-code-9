from setuptools import setup, find_packages
import os

# Variable
version = '1.0'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='bst.pygasus.session',
      version=version,
      description='Server session for bst.pygasus framework',
      long_description=long_description,
      keywords='pygasus web framework extjs',
      author='codeix',
      author_email='samuel.riolo@biel-bienne.ch',
      url='https://github.com/bielbienne/bst.pygasus.session',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      namespace_packages=['bst.pygasus'],
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      """,
      classifiers=[
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'License :: OSI Approved :: Zope Public License',
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta'
      ],
      )
