# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

import sys
from codecs import open
from os import path
from contextlib import contextmanager


def abspath(filename):
  """
  Returns the absolute path for *filename* from this directory.

  """
  here = path.abspath(path.dirname(__file__))
  return path.join(here, filename)


def get_short_description(text):
  """
  Returns the first paragraph from *text*.

  """
  return [p.strip() for p in text.strip().split('\n\n')][0]


def get_long_description(filename):
  """
  Returns the contents of *filename* (UTF-8).

  """
  with open(abspath(filename), encoding='utf-8') as f:
    return f.read()


@contextmanager
def add_to_pypath(directory):
  """
  Puts the *directory* on the ``PYTHONPATH`` for the duration of execution.

  .. note:: The *directory* is relative to this file.

  """
  path = abspath(directory)
  sys.path.insert(1, path)
  yield
  del(sys.path[0])


with add_to_pypath('templator'):
  from templator import __VERSION__, __doc__


REQUIRES = []

REQUIRES_LINKS = [
  'git+https://git@bitbucket.org/brutusdmc/corelib.git#egg=corelib[full]',
]

EXTRAS_REQUIRE = {}

TESTS_REQUIRE = []


setup(
  # package
  name='templatory',
  version=__VERSION__,
  packages=find_packages(exclude=['tests']),
  install_requires=REQUIRES,
  extras_require=EXTRAS_REQUIRE,
  dependency_links=REQUIRES_LINKS,
  # scripts
  entry_points={
    'console_scripts': [
      'templator=templator.__main__:main'
    ],
  },
  # tests
  test_suite='tests',
  tests_require=TESTS_REQUIRE,
  # meta
  description=get_short_description(__doc__),
  long_description=get_long_description('README.md'),
  keywords='templates, jinja, jinja2, markdown, restructuredtext, json, yaml',
  url='https://github.com/brutus/templator',
  author='Brutus [DMC]',
  author_email='brutus.dmc@googlemail.com',
  license='GNU GPLv3',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'Environment :: Console',
    'Environment :: Web Environment',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ]
)
