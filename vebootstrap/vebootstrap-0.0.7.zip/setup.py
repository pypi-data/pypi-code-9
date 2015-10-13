# -*- encoding:utf-8 -*-
from os import path
import codecs
from setuptools import setup


with codecs.open(path.join(path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='vebootstrap',
    version='0.0.7',
    author='tomoemon',
    author_email='bach48+github_tomoemon@gmail.com',
    packages=['vebootstrap'],
    scripts=[],
    install_requires=['virtualenv'],
    description = 'Virtualenv bootstrapper',
    long_description = long_description,
    url = 'https://github.com/tomoemon/vebootstrap',
    license = 'MIT',
    platforms = ['POSIX', 'Windows', 'Mac OS X'],
    zip_safe=False,
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Topic :: Utilities',
          'Topic :: Software Development'
    ]
)
