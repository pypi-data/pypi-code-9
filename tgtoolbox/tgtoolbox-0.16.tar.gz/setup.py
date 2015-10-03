# -*- coding: utf-8 -*-
__author__ = 'vahid'

import sys
import os
import re
py_version = sys.version_info[:2]
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


install_requires = [
    'tgext.datahelpers >= 0.2.0',
    'sqlalchemy>=0.7.0',
    "tw2.core",
    "tw2.forms",
    "tw2.tinymce",
    "tw2.recaptcha",
]

# reading pymlconf version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'tgtoolbox', '__init__.py')) as v_file:
        package_version = re.compile(r".*__version__\s*=\s*[\"'](.*?)[\"']", re.S).match(v_file.read()).group(1)


setup(
    name='tgtoolbox',
    version=package_version,
    description='',
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    packages=find_packages(exclude=['ez_setup']),
#    package_data={'tgtoolbox': ['widgets/templates/*/*',
#                                'smart_crud/templates/*/*']},
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=True
)
