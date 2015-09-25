#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='Flask-NSQ',
    version='0.1.0',
    description="Adds NSQ support for your Flask application",
    long_description=readme + '\n\n' + history,
    author="Nikhil Kalige",
    author_email='nikhilkalige@gmail.com',
    url='https://github.com/nikhilkalige/flask-nsq',
    packages=[
        'flask_nsq',
    ],
    package_dir={'flask_nsq':
                 'flask_nsq'},
    include_package_data=True,
    install_requires=[
        'Flask'
    ],
    license="MIT",
    zip_safe=False,
    keywords='flask-nsq',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
