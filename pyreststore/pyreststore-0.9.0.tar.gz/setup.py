# -*- coding: utf-8; mode: Python; -*-
#
# [Distutils] [issue152] setuptools breaks 
# with from __future__ import unicode_literals in setup.py
#
# from __future__ import unicode_literals

import os
import re
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def get_metadata():
    r = {}
    initfna = os.path.join('pyreststore', 'pyreststore', '__init__.py')
    init_py = open(initfna).read()
    r['version'] = re.search('__version__ = ["\']([^"\']+)["\']', 
                             init_py).group(1)
    r['author'] = re.search('__author__ = ["\']([^"\']+)["\']', 
                             init_py).group(1)
    r['license'] = re.search('__license__ = ["\']([^"\']+)["\']', 
                             init_py).group(1)
    return r

metadata = get_metadata()

print('Current metadata: {!s}'.format(metadata))
print('Packages: {!s}:'.format(
    find_packages(where='pyreststore',
                  exclude=['tests*','*.migrations'])))

if sys.argv[-1] == 'publish':
    version = metadata['version']
    if os.system('pip freeze | grep wheel'):
        print('wheel not installed.\nUse `pip install wheel`.\nExiting.')
        sys.exit()
    if os.system('pip freeze | grep twine'):
        print('twine not installed.\nUse `pip install twine`.\nExiting.')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    print('You probably want to also tag and finish the relese now:')
    print('  git flow release finish {:s}'.format(version))
    print('  git push --tags')
    sys.exit()

setup(
    name = 'pyreststore',
    version = metadata['version'],
    packages = find_packages(where='pyreststore',
                             exclude=['tests*','*.migrations']),
    package_dir = {'':'pyreststore'},
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    install_requires=['django',
                      'django-filter',
                      'djangorestframework',
                      'djangorestframework-jwt',
                      'django-rest-swagger',
                      'django-filter',
                  ],
    # metadata for upload to PyPI
    zip_safe=False,
    author = metadata['author'],
    author_email = 'peter.dahl.vestergaard@gmail.com',
    description = 'Python implementation of a REST based storage',
    license = metadata['license'],
    keywords = "REST",
    url = 'https://github.com/peterdv/pyreststore',   
)
