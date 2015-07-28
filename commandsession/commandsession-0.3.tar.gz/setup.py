#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requirements = [
    'boltons'
]

setup(
    name='commandsession',
    version='0.3',
    description="Small session wrapper for subprocess popen helpers.",
    author="Mike Waters",
    author_email='robert.waters@gmail.com',
    url='https://github.com/mikewaters/command-session',
    packages=[
        'commandsession',
    ],
    package_dir={'commandsession':
                 'commandsession'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='commandsession',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
