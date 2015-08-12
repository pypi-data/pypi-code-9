#!/usr/bin/env python

from distutils.core import setup

setup(
    name='tp_to_statsd',
    version='0.1.2',
    description='Record TP figures using statsd.',
    author='James Aylett',
    author_email='james@tartarus.org',
    license='MIT',
    packages=['tp_to_statsd',],
    scripts=[
        'scripts/tp_to_statsd',
    ],
    install_requires=[
        'requests>=2.3.0',
        'statsd>=3.0.0',
        'python-slugify>=1.1.3',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
