import os

from distutils.core import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

# Meta information
DESCRIPTION = ("Python package for solving assortative matching models with " +
               "two-sided heterogeneity.")

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Education',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Python :: 3.4',
               'Topic :: Scientific/Engineering',
               ]

setup(
      name="pyam",
      packages=['pyam'],
      version='0.2.0-alpha',
      description=DESCRIPTION,
      long_description=read('README.rst'),
      license="MIT License",
      author="davidrpugh",
      author_email="david.pugh@maths.ox.ac.uk",
      url='https://github.com/davidrpugh/pyAM',
      classifiers=CLASSIFIERS,
      )
