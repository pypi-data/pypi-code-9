from setuptools import setup

setup(
  name='dogic',
  version='0.1.dev4',
  packages=['dogic'],
  description='Run scripts from anywhere in docker containers',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4'
  ],
  install_requires=['docker-py==1.3.1'],
)
