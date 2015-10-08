#!/usr/bin/env python

from setuptools import setup, find_packages

entry_points = [
]


setup(
    name='toolkit',
    version='0.0.1',
    description='toolkit for script and utils',
    url='http://github.com/yufeiminds/toolkit',
    license='MIT',
    keywords='toolkit tool jinja2 unicode template',

    author='Yufei Li',
    author_email='yufeiminds@gmail.com',

    include_package_data=True,
    packages=find_packages(),
    entry_points={"console_scripts": entry_points},
    zip_safe=False,

    tests_require=[
        'pytest==2.5.2',
        'pytest-cov==1.8.1',
        'mock==1.0.1',
    ],

    #package_data={'folder': ['']},
    install_requires=open('requirements.txt').readlines(),
)

