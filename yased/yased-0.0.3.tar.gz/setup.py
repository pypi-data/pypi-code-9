# coding: utf-8

from setuptools import setup


setup(
    name='yased',
    version='0.0.3',
    description='Yet another simplest events dispatcher',
    url='https://github.com/pavelpat/yased',
    author='Pavel Patrin',
    author_email='pavelpat@ya.ru',
    packages=['yased'],
    package_dir={'': 'src'},
    test_suite='tests'
)
