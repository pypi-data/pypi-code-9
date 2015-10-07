#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='liqpay-python',
    packages=find_packages(),
    version='1.0',
    description='LiqPay Python SDK',
    url='https://github.com/liqpay/sdk-python',
    include_package_data=True,
    keywords=['liqpay'],
    install_requires=['requests']
)
