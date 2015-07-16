# -*- coding: utf-8 -*-
#
# Copyright 2015 Grigoriy Kramarenko <root@rosix.ru>
#
# This file is part of RosixDocs theme for Sphinx.
#

from setuptools import setup, find_packages
import rosixdocs

setup(
    name='rosixdocs',
    version=rosixdocs.__version__,
    description='Theme for Sphinx from Rosix projects.',
    long_description=open('README.rst').read(),
    author='Grigoriy Kramarenko',
    author_email='root@rosix.ru',
    url='https://bitbucket.org/djbaldey/rosixdocs',
    license='MIT',
    platforms='any',
    zip_safe=False,
    packages=['rosixdocs'],
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
)
