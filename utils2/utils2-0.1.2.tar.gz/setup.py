from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='utils2',
    version='0.1.2',
    description='Utils for various scenarios',
    long_description=long_description,
    url='https://github.com/eyalev/py_utils',
    author='Eyal Levin',
    author_email='eyalev@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['utils2'],
    install_requires=['six', 'python-dateutil', 'requests'],
)
