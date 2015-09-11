#!/usr/bin/env python

"""Install the Deis command-line client."""


try:
    from setuptools import setup
    USE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    USE_SETUPTOOLS = False

try:
    LONG_DESCRIPTION = open('README.rst').read()
except IOError:
    LONG_DESCRIPTION = 'Deis command-line client'

try:
    APACHE_LICENSE = open('LICENSE').read()
except IOError:
    APACHE_LICENSE = 'See http://www.apache.org/licenses/LICENSE-2.0'

KWARGS = {}
if USE_SETUPTOOLS:
    KWARGS = {'entry_points': {'console_scripts': ['deis = deis:main']}}
else:
    KWARGS = {'scripts': ['deis']}


with open('requirements.txt') as f:
    required = f.read().splitlines()
    required = [r for r in required if r.strip() and not r.startswith('#')]


setup(name='deis',
      version='1.9.post1',
      license=APACHE_LICENSE,
      description='Command-line Client for Deis, the open PaaS',
      author='Engine Yard',
      author_email='info@deis.io',
      url='https://github.com/deis/deis',
      keywords=[
          'opdemand', 'deis', 'paas', 'cloud', 'coreos', 'docker', 'heroku',
          'aws', 'ec2', 'digitalocean', 'gce', 'azure', 'linode', 'openstack'
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet',
          'Topic :: System :: Systems Administration',
      ],
      py_modules=['deis'],
      data_files=[
          ('.', ['README.rst']),
      ],
      long_description=LONG_DESCRIPTION,
      install_requires=required,
      zip_safe=True,
      **KWARGS)

print """
\033[93mNOTE: Download newer clients from deis.io\033[0m
=========================================

This is v1.9.1 of the `deis` CLI, the final Python version available at
https://pypi.python.org/pypi. Newer versions are available from http://deis.io.

Install the latest `deis` client for Linux or Mac OS X with:

    $ curl -sSL http://deis.io/deis-cli/install.sh | sh

The installer puts `deis` in your current directory, but you should move it
somewhere in your $PATH:

    $ ln -fs $PWD/deis /usr/local/bin/deis

More details are available at http://docs.deis.io/en/latest/using_deis/install-client/
"""
