#!/usr/bin/env python

from setuptools import setup

VERSION = __import__('statico').__version__

setup(
    name='statico',
    version=VERSION,
    description='Static site generator',
    long_description=open('README.rst').read(),
    author='Ossama Edbali',
    author_email='ossedb@gmail.com',
    url='https://github.com/oss6/statico/',
    license='MIT',
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ],
    packages=['statico'],
    include_package_data=True,
    entry_points={
        "console_scripts": ['statico = statico.statico:run']
    },
    install_requires=[
        'pathlib',
        'feedparser',
        'github3.py',
        'Jinja2',
        'livereload',
        'Markdown',
        'MarkupSafe',
        'oauthlib',
        'pytz',
        'PyYAML',
        'requests',
        'requests-oauthlib',
        'uritemplate.py',
        'Pygments',
        'colorama',
        'python-slugify',
        'pyinotify'
    ]
)
