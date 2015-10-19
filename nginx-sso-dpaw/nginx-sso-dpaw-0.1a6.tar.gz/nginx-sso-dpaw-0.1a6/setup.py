#!/usr/bin/env python

from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

install_requires = []
version = ('0.1a6')

setup(
    name='nginx-sso-dpaw',
    version=version,
    install_requires=install_requires,
    packages=['nginx_sso'],
    include_package_data=True,
    author='Rocky Chen',
    author_email='asi@dpaw.wa.gov.au',
    maintainer='Rocky Chen',
    maintainer_email='asi@dpaw.wa.gov.au',
    license='BSD 3-Clause License',
    url='https://bitbucket.org/dpaw/nginx-sso',
    description='Nginx SSO library for DPaW internal applications.',
    long_description=README,
    keywords=['auth', 'sso', 'nginx', 'dpaw'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
)
