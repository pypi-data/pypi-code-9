#!/usr/bin/env python

'Module configuration.'

from distutils.core import setup
import with_aws_config

setup(
    name='with_aws_config',
    version='1.0.1',
    description='Set AWS envars from `aws configure`, then run a command.',
    long_description=file('README.rst').read(),
    author='Garth Kidd',
    author_email='garth@garthk.com',
    url='https://github.com/garthk/with_aws_config',
    license='MIT',
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
    ],
    py_modules=['with_aws_config'],
    scripts=['bin/with-aws-config'],
)
