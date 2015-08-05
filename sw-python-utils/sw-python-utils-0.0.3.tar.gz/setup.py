# coding: utf-8
# python setup.py sdist register upload
from distutils.core import setup

setup(
    name='sw-python-utils',
    version='0.0.3',
    description='Soft Way company python utils.',
    author='Telminov Sergey',
    url='https://github.com/telminov/sw-python-utils',
    packages=['swutils', 'swutils.tests',],
    license='The MIT License',
    install_requires=[
        'netifaces', 'pycrypto'
    ],
)
