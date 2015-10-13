#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xwot.py - Python tools for the extended Web of Things
# Copyright (C) 2015  Alexander Rüedlinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Alexander Rüedlinger'

import argparse
import os.path
from xwot.compiler import Compiler
from xwot.compiler.frontend.processing import JSONLDDescriptionBuilder


def xwotc():
    """
    xwot compiler command
    """

    backends = Compiler.BACKENDS.keys()
    parser = argparse.ArgumentParser(description='xwot compiler')
    parser.add_argument('-p', dest='platform', type=str, default='klein', choices=backends, nargs='?',
                        help='platform to use')

    parser.add_argument('-o', dest='output_dir', type=str, default='out-app', nargs='?',
                        help='name of the output directory')

    parser.add_argument(dest='xwot_file', metavar='f', type=str,
                        help='xwot file')
    args = parser.parse_args()
    compiler = Compiler(input_file=args.xwot_file, output_dir=args.output_dir, platform=args.platform)
    compiler.compile()


def xwotd():
    """
    xwot description builder command
    """

    parser = argparse.ArgumentParser(description='xwot description builder')
    parser.add_argument('xwot_file', metavar='xwot file', type=str, nargs=1, help='a xwot file')

    parser.add_argument('-o', dest='output_filepath', type=str, default=None, nargs='?',
                        help='path of the output file')

    args = parser.parse_args()

    xml_filepath = args.xwot_file[0]
    description_builder = JSONLDDescriptionBuilder()
    out = description_builder.build(xml_file=xml_filepath)

    output_filepath = args.output_filepath
    if output_filepath is None:
        output_filepath = os.path.basename(xml_filepath) + ".jsonld"

    with open(output_filepath, "w+") as f:
        f.write(out)

