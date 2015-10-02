# -*- encoding:utf-8 -*-
from setuptools import setup

setup(
    name='vebootstrap',
    version='0.0.2',
    author='tomoemon',
    author_email='bach48+github_tomoemon@gmail.com',
    packages=['vebootstrap'],
    scripts=[],
    install_requires=['virtualenv'],
    description = 'Virtualenv bootstrapper',
    long_description = 'Importing this module automatically create virtualenv environment and apply requirements.txt',
    url = 'https://github.com/tomoemon/vebootstrap',
    license = 'MIT',
    platforms = ['POSIX', 'Windows', 'Mac OS X'],
    zip_safe=False,
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Topic :: Utilities',
          'Topic :: Software Development'
    ]
)
