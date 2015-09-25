__author__ = 'yue'

from setuptools import setup, find_packages

setup(
    name = 'ehcCli',
    version = '0.0.1',
    keywords = ('ehc', 'cli'),
    description = 'a simple command line tool for ehc',
    license = 'ehc License',
    install_requires = ['click>=0.6', 'tabulate>=0.7.5', 'requests>=2.2.1'],
    author = 'jingyue',
    author_email = 'jingyue@zetyun.com',
    packages = find_packages(),
    platforms = 'any',
    scripts=[
        'bin/ehccli'
    ]
)
