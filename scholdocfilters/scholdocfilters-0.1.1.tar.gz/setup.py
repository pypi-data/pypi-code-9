from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='scholdocfilters',
      version='0.1.1',
      description='Utilities for writing Scholdoc filters in Python',
      long_description=read('README.rst'),
      author='Tim T.Y. Lin',
      author_email='timtylin@gmail.com',
      url='http://github.com/timtylin/scholdoc-filters',
      py_modules=['scholdocfilters'],
      keywords=['scholdoc','pandoc'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Filters'
      ],
      )
