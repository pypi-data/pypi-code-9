#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, Command, find_packages
import sys


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


if 'sdist' in sys.argv or 'develop' in sys.argv:
    try:
        os.chdir('stdimage')
        from django.core import management
        management.call_command('compilemessages')
    finally:
        os.chdir('..')


setup(
    name='django-stdimage',
    version='2.0.6',
    description='Django Standarized Image Field',
    author='codingjoe',
    url='https://github.com/codingjoe/django-stdimage',
    author_email='info@johanneshoppe.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", ".egg-info"]),
    include_package_data=True,
    install_requires=[
        'pillow>=2.5',
        'progressbar2>=2.7',
    ],
    cmdclass={'test': PyTest},
)
