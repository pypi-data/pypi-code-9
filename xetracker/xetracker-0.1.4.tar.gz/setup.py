import os

try:
  from setuptools import setup, Command
except:
  from distutils.core import setup, Command

class CleanCommand(Command):
  """Custom clean command to tidy up the project root."""
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    os.system("rm -vrf ./build ./dist ./*.pyc ./*.tar.gz ./*.egg-info")

config = {
  "name": "xetracker",
  "description": "Track the rates of the foreign currency traders",
  "author": "tasyrkin",
  "url": "https://github.com/tasyrkin/xetracker",
  "author_email": "tasyrkin@gmail.com",
  "version": "0.1.4",
  "install_requires": ["lxml", "psycopg2"],
  "packages": ["xetracker", "xetracker.model", "xetracker.persistance", "xetracker.fetchers"],
  "scripts": ["bin/xetracker"],
  "cmdclass": {
    "clean": CleanCommand
  },
  "test_suite": 'nose.collector',
  "tests_require": ['nose']
}

setup(**config)
