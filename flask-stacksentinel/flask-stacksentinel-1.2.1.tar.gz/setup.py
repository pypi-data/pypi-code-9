"""
Flask-SQLite3
-------------

This is the description for that library
"""
from setuptools import setup, find_packages

setup(
    name='flask-stacksentinel',
    version='1.2.1',
    url='https://github.com/StackSentinel/stacksentinel-flask',
    author="Jeri MgCuckin",
    author_email="jerymcguckin@stacksentinel.com",
    description='Stack Sentinel error tracking integration with Flask',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    platforms='any',
    install_requires=[
        'Flask',
        'stacksentinel'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    license = 'Apache License (2.0)'
)
