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

requirements = [
    "requests==2.8.1"
]

test_requirements = [
    "python-coveralls"
]

setup(
    name='gingerit',
    version='0.5.8',
    long_description="Correcting spelling and grammar mistakes based on the context of complete sentences. Wrapper around the gingersoftware.com API",
    author='Tim Kleinschmidt',
    author_email='tim.kleinschmidt@gmail.com',
    url='https://github.com/Azd325/gingerit',
    packages=[
        'gingerit',
    ],
    package_dir={'gingerit':
                 'gingerit'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
