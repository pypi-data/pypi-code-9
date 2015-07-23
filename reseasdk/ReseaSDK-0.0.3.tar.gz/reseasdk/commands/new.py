import os
import re
import sys
import jinja2
import reseasdk
from reseasdk.helpers import error, generating, exec_cmd

HELP = """
Usage: reseasdk new package_name
""".strip()

README_TEMPLATE = """\
# {{ package_name }}

"""

GITIGNORE_TEMPLATE = """\
/build
/packages
"""

PACKAGE_YML_TEMPLATE = """\
name: {{ package_name }}
category:    # application, library or interface
license:     # MIT, BSD 2-clause, BSD 3-clause, Public Domain, GPLv2
summary:     # brief explanation
description: # longer explanation

warning:     # some important things to note
info:        # what we should know

author: {{ author }}
email: {{ email }}
homepage:    # e.g. http://example.com/foo/bar

# Required packages
requires: []
lib_requires: []

# Interfaces which this package uses
uses: []

# Interfaces which this package implements
implements: []


#
#  Type definitions
#
type:


#
#  Interface definitions
#
interface:


#
#  Build configuration definitions
#
config:


#
#  Build rules
#
build:
  sources: []


#
#  early-startup: If it is `yes`, STARTUP() MUST return.
#
#  It is essential for applications that needed before
#  initializing the threading system (`thread` package).
#
early-startup: no

"""

CONFIG_BUILD_YML_TEMPLATE = """\
BUILTIN_APPS: []
ALLOW_EXTERNAL: no
HAL:  userspace
TEST: yes
STARTUP_WITH_THREAD: yes
"""

CONFIG_TEST_YML_TEMPLATE = """\
BUILTIN_APPS: []
HAL:  userspace
TEST: yes
STARTUP_WITH_THREAD: yes
"""

FILES = [
    # (filepath, template)
    ('README.md', README_TEMPLATE),
    ('.gitignore', GITIGNORE_TEMPLATE),
    ('package.yml', PACKAGE_YML_TEMPLATE),
    ('config.release.yml', CONFIG_BUILD_YML_TEMPLATE),
    ('config.test.yml', CONFIG_TEST_YML_TEMPLATE),
    ('src/.gitkeep', ''),
    ('Documentation/.gitkeep', '')
]
PACKAGE_NAME_REGEX = '[a-z_][a-z0-9_]*'


def main(args):
    try:
        package_name = args[0]
    except IndexError:
        sys.exit(HELP)

    if re.match(PACKAGE_NAME_REGEX, package_name) is None:
        error('The package name must be lowercase_with_underscore (regex: {})'
              .format(PACKAGE_NAME_REGEX))

    #
    #  generate the package directory
    #
    generating('MKDIR', package_name)
    try:
        os.mkdir(package_name)
    except FileExistsError:
        error("Directory already exists: '{}'".format(package_name))

    #
    #  Variables used in templates
    #
    author = exec_cmd('git config --get user.name', ignore_failure=True).strip()
    email = exec_cmd('git config --get user.email', ignore_failure=True).strip()

    #
    #  generate directories and files
    #
    for path,tmpl in FILES:
        f = '{}/{}'.format(package_name, path)
        dir = os.path.dirname(f)

        if not os.path.exists(dir):
            generating('MKDIR', dir)
            os.mkdir(dir)

        generating('GEN', f)
        open(f, 'w').write(jinja2.Template(tmpl).render(**locals()))

    #
    # intialize as a new Git repository
    #
    exec_cmd('git init .', cwd=package_name)

