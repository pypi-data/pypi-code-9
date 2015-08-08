#!/usr/bin/env python

from setuptools import setup, find_packages

from semantic_ui import __version__


setup(
    name='crispy-semantic-ui',
    version='.'.join(map(str, __version__)),
    description='Semantic UI template pack for crispy forms',
    url='https://github.com/alexey-grom/crispy-semantic-ui',
    author='alxgrmv@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-crispy-forms',
                      'django'],
)
