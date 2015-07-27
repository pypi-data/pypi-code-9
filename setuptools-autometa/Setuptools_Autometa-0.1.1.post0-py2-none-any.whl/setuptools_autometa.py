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
"""Add autometa keyword to setuptools.setup for automatic version, description and long_desctiption.

To use it, pass module (without .py), or package name as autometa keyword argument for setup()::

    #! /usr/bin/env python
    from setuptools import setup

    setup(
        autometa='test',
        name='Test',
        packages=['test'],
        ...
    )

For example following package's __init__.py::

    \"""First line of docstring.

    Many
    more
    lines
    of
    docstring.
    \"""
    __version__ = '1.2.3.dev0'  # alternatively: (1, 2, 3, 'dev0')

Is equivalent to writing::

    setup(
        version='1.2.3.dev0',
        description='First line of docstring',
        long_description='Many\\nmore\\nlines\\nof\\ndocstring.'
        ...
    )

It will parse specified module file or package's __init__.py and set version to its __version__
attribute, description to first line of its docstring, and long_description to the rest of the
docstring. Additionally build_sphinx command's version and release will be set.

**NOTE:** Please note, that version is parsed by running
`ast.literal_eval <https://docs.python.org/3/library/ast.html#ast.literal_eval>`_
on the right side of assignment to __version__, so keep in mind that it can only be a string
literal, or a list/tuple of string/integer literals.

**NOTE:** Setuptools-Autometa assumes `PEP 0257 <https://www.python.org/dev/peps/pep-0257/>`_
compliant docstrings, that is first line has to end with a period and be separated from description
by a blank line.

Additionally you can whitelist which fields are to be parsed by using autometa_fields keyword
argument and setting it to an iterable of field names ('description', 'long_description', \
'version').

"""
__version__ = '0.1.1.post0'

import ast
import os
import sys


def _autometa(module, path, fields=None):
    if fields is not None and not fields:
        return {}

    target = os.path.join(path, *module.split('.'))
    if os.path.isdir(target):
        target = os.path.join(target, '__init__.py')
    else:
        target = '{}.py'.format(target)

    with open(target) as input:
        source = input.read()
    tree = ast.parse(source)

    meta = {}
    if not fields or fields.intersection({'description', 'long_description'}):
        docstring = ast.get_docstring(tree)
        if docstring:
            lines = docstring.splitlines()
            if not fields or 'description' in fields:
                meta['description'] = lines[0][:-1]
            if len(lines) > 2 and (not fields or 'long_description' in fields):
                meta['long_description'] = '\n'.join(lines[2:])

    if not fields or 'version' in fields:
        version = None
        for child in ast.iter_child_nodes(tree):
            if isinstance(child, ast.Assign):
                if '__version__' in (target.id for target in child.targets):
                    version = ast.literal_eval(child.value)
                    break

        if isinstance(version, (list, tuple)):
            meta['version'] = '.'.join(map(str, version))
        elif version is not None:
            meta['version'] = str(version)

    return meta


def _autometa_fields_keyword(dist, attr, value):
    pass


def _autometa_keyword(dist, attr, value):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))

    fields = None
    if dist.autometa_fields:
        fields = set(dist.autometa_fields)
    meta = _autometa(value, path, fields)

    for key, value in meta.items():
        setattr(dist.metadata, key, value)
    if 'version' in meta:
        if 'build_sphinx' not in dist.command_options:
            dist.command_options['build_sphinx'] = {}

        dist.command_options['build_sphinx']['release'] = ('setup.py', meta['version'])
        dist.command_options['build_sphinx']['version'] = ('setup.py', meta['version'])
