#!/usr/bin/env python
#
# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from setuptools import setup
import metadata

app_name = metadata.name
version = metadata.version

long_description = open('docs/index.rst').read().split('split here', 1)[0] 

setup(
    name = "django-%s" % app_name,
    version = version,

    packages = [app_name],

    author = "Philip Roche",
    author_email = "phil.roche@ticket-text.com",
    maintainer = "Philip Roche",
    maintainer_email = "phil.roche@ticket-text.com",
    description = "This Django application you to prepend a string to your django app urls useful if you need to change themes based on url.",
    long_description = long_description,
    license = "MIT License",
    keywords = "django url",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ],
)
