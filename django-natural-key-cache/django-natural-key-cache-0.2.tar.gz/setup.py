#!/usr/bin/env python
# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
setup script for natural_key_cache
'''
import os
from setuptools import setup, find_packages, Command

SETUP_DIRNAME = os.path.dirname(__file__)
if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)

REQS_FILE = os.path.join(os.path.abspath(SETUP_DIRNAME), 'requirements.txt')
REQUIREMENTS = []
with open(REQS_FILE) as rfh:
    for line in rfh.readlines():
        if not line or line.startswith('#'):
            continue
        REQUIREMENTS.append(line.strip())


class TestCommand(Command):
    '''
    Custom Test command.

    Runs test suite for test django project
    '''
    user_options = []

    def initialize_options(self):
        ''' no options '''
        pass

    def finalize_options(self):
        ''' no options '''
        pass

    def run(self):
        ''' Run django project test suite '''
        import sys, subprocess
        raise SystemExit(
            subprocess.call(['coverage',
                             'run',
                             '--source=natural_key_cache',
                             'tests/manage.py',
                             'test']))


class CleanCommand(Command):
    ''' Clean command '''
    description = 'Clean dist/build directories'
    user_options = []

    def initialize_options(self):
        ''' no options '''
        pass

    def finalize_options(self):
        ''' no options '''

    def run(self):
        ''' clean things up '''
        os.chdir(SETUP_DIRNAME)
        os.system('rm -rf ./build ./dist *.egg-info')


setup(
    name='django-natural-key-cache',
    version='0.2',
    license='ISC License',
    description='Cache manager for caching django models by natural keys',
    long_description='Cache manager for caching django models by natural keys',
    author='Timothy Messier',
    author_email='tim.messier@gmail.com',
    url='https://github.com/shadowfax-chc/django-natural-key-cache',
    packages=find_packages(exclude=('tests', 'doc')),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    keywords='django-natural-key-cache',
    cmdclass={
        'test': TestCommand,
        'clean': CleanCommand,
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
