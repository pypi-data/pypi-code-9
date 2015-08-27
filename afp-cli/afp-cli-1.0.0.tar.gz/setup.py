#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'afp-cli',
          version = '1.0.0',
          description = '''Command line client for aws federation proxy api''',
          long_description = '''AFP CLI
**************************

Overview
========
The AFP CLI is the command line interface to access the AWS Federation Proxy.

Its main use case is starting a new shell where your temporary AWS
credentials have been exported into the environment.


Configuration
~~~~~~~~~~~~~

The **afp-cli** command can be globally configured with a yaml file:
    ``/etc/aws-federation-client/api.yaml``

Syntax:
    ``api_url: <api-url>``

Each user's home directory can override this setting in the same way, using
    ``$HOME/.aws-federation-client/api.yaml``


CLI Tool
========

Get help text
~~~~~~~~~~~~~~~~~~~~~~
    ``aws-cli [-h | --help]``

List available account names and roles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the currently logged-in user:
    ``aws-cli``

The same for another user:
    ``aws-cli --user=username``

Output format:
    ``<accountname>    <role1>,<role2>,...,<roleN>``

Example output::

    abc_account     some_role_in_abc_account
    xyz_account     some_role_in_yxz_account,another_role_in_xyz

Export credentials
~~~~~~~~~~~~~~~~~~
This starts a subshell in which the credentials have been exported into the environment. Use
the "exit" command or press CTRL+D to terminate the subshell.

Export credentials for currently logged in user and specified account and role
    ``afp-cli --account=accountname --role=rolename``

As above, but specifying a different user:
    ``afp-cli --user=username --account=accountname --role=rolename``

Specify the URL of the AFP server, overriding any config file
    ``afp-cli --api-url=https://yourhost/some/path .....``

''',
          author = "Stefan Neben, Tobias Vollmer, Stefan Nordhausen, Enrico Heine",
          author_email = "stefan.neben@immobilienscout24.de, tobias.vollmer@immobilienscout24.de, stefan.nordhausen@immobilienscout24.de, enrico.heine@immobilienscout24.de",
          license = 'Apache License 2.0',
          url = 'https://github.com/ImmobilienScout24/afp-cli',
          scripts = ['scripts/afp-cli'],
          packages = ['afp_cli'],
          py_modules = [],
          classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.6', 'Programming Language :: Python :: 2.7'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "docopt", "requests", "yamlreader" ],
          
          zip_safe=True
    )
