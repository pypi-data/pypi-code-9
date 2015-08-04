#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('lisa_api')


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name='lisa-api',
    version=version,
    url='http://www.lisa-project.net',
    license='Apache',
    description='LISA Project API',
    author='Julien Syx',
    author_email='julien@lisa-project.net',  # SEE NOTE BELOW (*)
    packages=get_packages('lisa_api'),
    package_data=get_package_data('lisa_api'),
    scripts=['lisa_api/lisa-api-cli'],
    install_requires=[
        'pip==1.5.6',
        'djangorestframework',
        'django>=1.8',
        'mysqlclient',
        'django-rest-swagger',
        'stevedore',
        'colorlog',
        'six',
        'kombu',
        'requests',
        'cookiecutter',
        'mistune',
        'django-compressor',
        'django-libsass'
    ],
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    entry_points={
        'lisa.api.tts': [
            'pico = lisa_api.api.tts.pico:Pico',
            'google = lisa_api.api.tts.google:Google',
        ],
        'lisa.api.speak': [
            'rabbitmq = lisa_api.api.speak.rabbitmq:Rabbitmq',
        ]

    },

)

# (*) Please direct queries to the discussion group, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
