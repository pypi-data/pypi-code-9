# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

from setuptools import setup, find_packages

setup(
    name = 'torhandlers',
    packages = find_packages(exclude=('tests', 'examples',)),
    version = '0.1',
    description = 'Library with tornado framework handlers similar to Django\'s CBV\'s',
    author = 'Alex Bo',
    author_email = 'bosha@the-bosha.ru',
    url = 'https://github.com/bosha/torhandlers',
    keywords = ['tornado', 'django', 'generic', 'json', 'ajax', 'rest'],
    install_requires=['tornado', 'sqlalchemy', 'wtforms'],
    test_suite='tests',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
)
