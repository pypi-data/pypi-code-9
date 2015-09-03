
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import salesmachine-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'salesmachine'))
from version import VERSION

long_description = '''
Salesmachine.io is the next generation of CRM.

This is the official python client that wraps the Salesmachine.io REST API (http://salesmachine.io).

Documentation and more details at https://github.com/salesmachine-io/salesmachine-python
'''

setup(
    name='salesmachine-python',
    version=VERSION,
    url='https://github.com/salesmachine-io/salesmachine-python',
    author='Salesmachine',
    author_email='team@salesmachine.io',
    maintainer='Salesmachine',
    maintainer_email='team@salesmachine.io',
    test_suite='salesmachine.test.all',
    packages=['salesmachine', 'salesmachine.test'],
    license='MIT License',
    install_requires=[
        'python-dateutil',
        'requests',
        'six'
    ],
    description='The hassle-free way to integrate Salesmachine.io into any python application.',
    long_description=long_description
)
