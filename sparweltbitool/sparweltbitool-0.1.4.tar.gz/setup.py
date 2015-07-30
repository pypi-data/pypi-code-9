#!/usr/bin/env python

from setuptools import setup, find_packages

def readme():
    with open("README.rst") as f:
        return f.read()

setup(
    name="sparweltbitool",
    version='0.1.4',
    long_description=readme(),
    description='Standard modules used by Sparwelt GmbH BI Team in Web Services',
    summary="Python library with standard modules used by Sparwelt GmbH BI Team in Web Services.",
    author="Paweł Graczyk",
    author_email='abs-saas@sparwelt.de',
    py_modules=['sparweltbitool'],
    url="https://github.com/sparwelt/bitool.git",
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    include_package_data=True,
    platform="python",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
