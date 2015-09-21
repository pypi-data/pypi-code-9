# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='stock_info',
    version = '1.0.0',
    description= 'show the price of the stock',
    author = 'zhenchaozhu',
    author_email = 'zhenchaozhu@outlook.com',
    url = 'https://github.com/zhenchaozhu/stock_info',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stock = stock.main:main',
        ]
    },
    install_requires=[
        'requests',
    ]
)
