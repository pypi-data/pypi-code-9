#!/usr/bin/env python

from setuptools import setup

setup(
    name='slamon-agent',
    version='1.1.0',
    description='Python implementation of a SLAMon Agent',
    url='https://github.com/SLAMon/slamon-python-agent',
    author='SLAMon',
    author_email='slamon.organization@gmail.com',
    license='Apache License v2.0',
    platforms=['Python 3.3+'],
    long_description='The implementation of SLAMon agent on Python 3.4. The agent connects to an Agent Fleet Manager, \
and executes tasks retrieved.\nAimed to be used on Unix platforms. The agent can be used either from a python script \
or via command line script.\nRead more from the repository for examples and instructions.',
    packages=[
        'slamon_agent',
        'slamon_agent.handlers',
    ],
    install_requires=[
        'python_dateutil>= 2.4.2, <3.0',
        'requests>=2.5.4.1, <3.0'
    ],
    entry_points={
        'console_scripts': [
            'slamon-agent = slamon_agent.agent:main'
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Monitoring'
    ]
)
