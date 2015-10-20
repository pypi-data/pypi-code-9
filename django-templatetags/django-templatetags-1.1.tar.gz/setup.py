# coding: utf-8

import os
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(current_dir, 'README.md')).read()

setup(
    name='django-templatetags',
    version='1.1',
    packages=['notification'],
    description='Custom template tags for notification',
    long_description=readme,
    author='Élysson MR',
    author_email='elyssonmr@gmail.com',
    url='https://github.com/elyssonmr/django_pkg/',
    license='MIT',
    install_requires=[
        'Django>=1.8',
    ]
)
