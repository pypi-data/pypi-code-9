# -*- coding: UTF-8 -*-
# Copyright © 2015, Michał Przybyś <michal@przybys.eu>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of
#    conditions and the following disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Setuptools-Autometa's setup script.

**NOTE:** Do not use this setup script as an example, as it works around the fact that
Setuptools-Autometa is not yet installed!
"""
import os
import setuptools
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
import setuptools_autometa

# Please note, that this is not the way Setuptools-Autometa is intended to be used.
meta = setuptools_autometa._autometa('setuptools_autometa', os.path.dirname(__file__))

setuptools.setup(
    name='Setuptools-Autometa',
    version=meta['version'],
    license='Simplified BSD License',
    description=meta['description'],
    long_description=meta['long_description'],
    author='Michał Przybyś',
    author_email='michal@przybys.eu',
    url='https://przybys.eu/software/setuptools-autometa',
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development'
    ],
    keywords=[
        'automatic',
        'description',
        'setuptools',
        'version'
    ],
    py_modules=[
        'setuptools_autometa'
    ],
    entry_points={
        'distutils.setup_keywords': [
            'autometa = setuptools_autometa:autometa_keyword',
            'autometa_fields = setuptools_autometa:autometa_fields_keyword'
        ]
    },
    include_package_data=True,
    zip_safe=True
)
