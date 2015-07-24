# coding:utf-8

from setuptools import setup, find_packages

long_description = """\
Wrapper for `threading.local` with enhanced value accessor.

See detail @ http://github.com/tomokinakamaru/perth.

Copyright (c) 2015, Tomoki Nakamaru.

License: MIT
"""

setup(
    author='Tomoki Nakamaru',
    author_email='tomoki.nakamaru@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='',
    license='MIT',
    long_description=long_description,
    name='perth',
    packages=find_packages(),
    platforms='any',
    url='http://github.com/tomokinakamaru/perth',
    version='1.0.0'
)
