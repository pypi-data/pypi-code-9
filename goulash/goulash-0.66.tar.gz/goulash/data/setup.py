#!/usr/bin/env python
""" setup.py for {{project_name}}
"""

import os
import sys
from setuptools import setup, find_packages
# make sure that finding packages works, even
# when setup.py is invoked from outside this dir
this_dir = os.path.dirname(os.path.abspath(__file__))
if not os.getcwd() == this_dir:
    os.chdir(this_dir)

# make sure we can import the version number so that it doesn't have
# to be changed in two places. pkg/__init__.py is also free
# to import various requirements that haven't been installed yet
sys.path.append(os.path.join(this_dir, '{{pkg}}'))
from version import __version__
sys.path.pop()

base_url = 'https://github.com/{{author}}/{{pkg_name}}/'
packages = [x for x in find_packages() if x not in ['tests']]
setup(
    name='{{pkg_name}}',
    version=__version__,
    description='',
    author='{{author}}',
    author_email='',
    url=base_url,
    download_url=base_url + '/tarball/master',
    packages=packages,
    keywords=['{{pkg_name}}'],
    install_requires=[
        'addict',       # dictionary utility
        'Importing'     # for lazy imports
    ],
    entry_points=dict(
        console_scripts=[
            '{{pkg_name}} = {{pkg_name}}.bin._{{pkg_name}}:entry',
        ]),
    package_data={'': ['*.*', '{{pkg_name}}/data/*.*']},
    include_package_data=True,
)
