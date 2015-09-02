import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name             = 'ltg',
      version          = '0.1.0',
      author           = 'Aljosha Friemann',
      author_email     = 'aljosha.friemann@gmail.com',
      description      = 'link to git',
      license          = None,
      keywords         = ["utility", "configuration", "git", "linux"],
      url              = 'https://bitbucket.org/afriemann/ltg',
      # download_url     = 'https://bitbucket.org/afriemann/ltg/get/v0.1.0.tar.gz',
      packages         = ['ltg'],
      long_description = read('README.rst'),
      classifiers      = [],
      entry_points     = {'console_scripts': ['ltg=ltg.cli:run']}
)
