'''

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = ['sxclient']
requires = ['requests']

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='sxclient',
    version='0.1.0',
    description='Python SX client-side library',
    long_description=readme,
    author='Skylable Ltd.',
    author_email='sx-users@lists.skylable.com',
    url='http://www.skylable.com/docs/python-sxclient',
    packages=packages,
    install_requires=requires,
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
