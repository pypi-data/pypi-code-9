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


def requirements(*filenames):
    requires = []

    for filename in filenames:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    # Skip blank lines and comments
                    continue
                requires.append(line)

    return requires

setup(
    name='precs',
    version='0.1.0a2',
    description="Python implementation of record stream processing utilities.",
    long_description=readme + '\n\n' + history,
    author="Muhammad Umer Azad",
    author_email='umer.azad@gmail.com',
    url='https://github.com/umerazad/precs',
    packages=[
        'precs',
        'precs.processors'
    ],
    py_modules=['precs/precs'],
    entry_points='''
        [console_scripts]
        precs=precs.precs:cli
    ''',
    package_dir={'precs':
                 'precs'},
    include_package_data=True,
    install_requires=requirements('requirements.txt'),
    license="MIT",
    zip_safe=False,
    keywords='precs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=requirements('requirements-test.txt')
)
