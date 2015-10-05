#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'afp-cli',
          version = '1.1.1-0',
          description = '''Command line client for AWS federation proxy api''',
          long_description = '''=======
AFP CLI
=======

.. image:: https://travis-ci.org/ImmobilienScout24/afp-cli.png?branch=master
   :alt: Travis build status image
   :target: https://travis-ci.org/ImmobilienScout24/afp-cli

.. image:: https://img.shields.io/pypi/v/afp-cli.svg
   :alt: Version
   :target: https://pypi.python.org/pypi/afp-cli

Overview
========

The AFP CLI is the command line interface to access the
AWS Federation Proxy (AFP).

Its main use case is starting a new shell where your temporary
AWS credentials have been exported into the environment.

Configuration
=============

The **afp** command can be configured through yaml files in
the following direcories:

* ``/etc/afp-cli/*.yaml`` (global configuration)
* ``$HOME/.afp-cli/*.yaml`` (per-user configuration)

The yaml files are read in lexical order and merged via
`yamlreader <https://github.com/ImmobilienScout24/yamlreader>`_.
The following configuration options are supported:

* ``api_url: <api-url>``
  Defaults to lookup a FQDN of a host named **afp** via DNS and construct
  the server url from it: ``https://{FQDN}/afp-api/latest``
* ``user: <username>``
  Defaults to the currently logged in username

Example:

.. code-block:: yaml

    api_url: https://afp-server.my.domain/afp-api/latest
    user: myuser

CLI Tool
========

Get help text
-------------

.. code-block:: console

    $ afp [-h | --help]

List available account names and roles
--------------------------------------

For the currently logged-in user:

.. code-block:: console

    $ afp

The same for another user:

.. code-block:: console

    $ afp --user=username

Output format:

::

    <accountname>    <role1>,<role2>,...,<roleN>

Example output:

::

    abc_account    some_role_in_abc_account
    xyz_account    some_role_in_yxz_account,another_role_in_xyz

Use AWS credentials
-------------------

This starts a subshell in which the credentials have been exported into the
environment. Use the **exit** command or press **CTRL+D** to terminate the subshell.

Use credentials for currently logged in user and specified account and role:

.. code-block:: console

    $ afp accountname rolename

Use credentials for the currently logged in user for the *first* role:

.. code-block:: console

    $ afp accountname

As above, but specifying a different user:

.. code-block:: console

    $ afp --user=username accountname rolename

Specify the URL of the AFP server, overriding any config file:

.. code-block:: console

    $ afp --api-url=https://yourhost/some/path

Show and Export
---------------

In case you don't want to start a subshell or are using something other than
bash, you can use ``--show`` or ``--export`` to display the credentials. You
can use the usual UNIX tools to add/remove them from your environment.
``--show`` will just show them and ``--export`` will show them in format
suitable for an export into your environment, i.e. prefixed with ``export`` for
UNIX and ``set`` for Windows.


.. code-block:: console

   $ afp --show <myaccount> [<myrole>]
   Password for myuser:
   AWS_VALID_SECONDS='600'
   AWS_SESSION_TOKEN='XXX'
   AWS_SECURITY_TOKEN='XXX'
   AWS_SECRET_ACCESS_KEY='XXX'
   AWS_EXPIRATION_DATE='1970-01-01T01:00:00Z'
   AWS_ACCESS_KEY_ID='XXX'

.. code-block:: console

   $ afp --export <myaccount> [<myrole>]
   Password for myuser:
   export AWS_VALID_SECONDS='600'
   export AWS_SESSION_TOKEN='XXX'
   export AWS_SECURITY_TOKEN='XXX'
   export AWS_SECRET_ACCESS_KEY='XXX'
   export AWS_EXPIRATION_DATE='1970-01-01T01:00:00Z'
   export AWS_ACCESS_KEY_ID='XXX'


The following examples work in zsh, to add and remove them from your
environment:

Adding credentials:

.. code-block:: console

   $ eval $(afp --export <accountname>)

Removing them again:

.. code-block:: console

    $ env | grep AWS | cut -f 1 -d'=' | while read line ; do ; unset $line ; done ;
''',
          author = "Stefan Neben, Tobias Vollmer, Stefan Nordhausen, Enrico Heine",
          author_email = "stefan.neben@immobilienscout24.de, tobias.vollmer@immobilienscout24.de, stefan.nordhausen@immobilienscout24.de, enrico.heine@immobilienscout24.de",
          license = 'Apache License 2.0',
          url = 'https://github.com/ImmobilienScout24/afp-cli',
          scripts = ['scripts/afp'],
          packages = ['afp_cli'],
          py_modules = [],
          classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.6', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5'],
          entry_points={
          'console_scripts':
              ['afp=afp_cli.cli:main']
          },
             #  data files
             # package data
          install_requires = [ "docopt", "requests", "yamlreader>=3.0.1" ],
          
          zip_safe=True
    )
