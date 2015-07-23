from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='cfnparams',
    version='0.1',
    description='CloudFormation stack paramater utility.',
    author='Jonathan Sokolowski',
    author_email='jsok@expert360.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='aws cfn cloudformation stack',
    url='https://github.com/expert360/cfn-params',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto>=2.38.0',
    ],
    extras_require={
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'cfn-params = cfnparams:main',
        ],
    },
)
