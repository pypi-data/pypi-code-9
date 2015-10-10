from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

version = '0.0.2'

#pylint:disable=R0904
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        #pylint: disable=W0201
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(name='probe-rdirwatcher',
      version=version,
      description="watch remote directory for changes",
      scripts=['scripts/run_rdirwatcher.py'],
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Petr Zikan',
      author_email='zikan.p@gmail.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'paramiko',
          'docopt',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      tests_require=['pytest'],
      namespace_packages=['probe'],
      package_data={'probe.rdirwatcher': ['cfg/rdirwatcher.cfg', 'cfg/rdirwatcher_logging.cfg']},
      cmdclass={'test': PyTest},
      )
