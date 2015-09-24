# -*- coding: utf-8 -*-
try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}


with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not
                                                     line.startswith('--'))
    ]

setup(
    name='python-odl',
    version='0.0.1',
    author='Beraldo Leal',
    author_email='beraldo@ncc.unesp.br',
    packages=["odl", "of"],
    url='http://github.com/beraldoleal/python-odl/',
    license='LICENSE.md',
    description='Python 2.x library for OpenDayLight interations via REST API.',
    install_requires=install_requires,
    scripts=[],
    keywords = ['odl', 'opendayligh', 'sdn', 'openflow', 'python', 'library', 'rest', 'api'],
    platforms = "Posix; MacOS X;",
    classifiers = ["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Operating System :: POSIX",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Internet",
                   "Topic :: System :: Networking",
                   "Programming Language :: Python :: 2.7"],
    **extra
)
