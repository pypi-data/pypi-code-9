#!/usr/bin/env python
import sys
import warnings

from os import path

from pkg_resources import parse_requirements

from setuptools import setup, find_packages


name = 'tinbox-client'  # PyPI name
package_name = name.replace('-', '_')  # Python module name
package_path = 'src'  # Where does the package live?

# Filesystem path to the module that contains the get_version() method
version_file = path.join(package_path, package_name, 'version.py')

here = path.dirname(path.abspath(__file__))

# Add src dir to path
sys.path.append(package_path)


# Get the long description from the relevant file
long_description = None

try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except Exception as exc:
    warnings.warn('Could not read README.rst in {}: {}'.format(here, exc))


def get_version(module_filename):
    """
    Get the version from a version module inside our package. This is
    useful if we import our main modules in package/__init__.py,
    which will cause ImportErrors if we try to import package/version.py
    using the regular import mechanism.

    :return: result of ``<version-module>.get_version()``
    """
    context = {}

    # exec the version module
    with open(module_filename) as fp:
        exec(fp.read(), context)

    # Call the module function 'get_version'
    return context['get_version']()


def get_requirements(filename):
    return [str(r) for r in parse_requirements(open(filename).read())]


setup(
    name=name,
    version=get_version(version_file),
    author='Joar Wandborg',
    author_email='joar@5monkeys.se',
    url='https://github.com/5monkeys/tinbox-client',
    license='MIT',
    description='Tinbox client library',
    long_description=long_description,
    package_dir={'': package_path},  # Package lives in ./src
    packages=find_packages(package_path),
    install_requires=get_requirements('requirements.txt')
)
