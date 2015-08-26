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

import sys
import os
import os.path

from backend.KleinBackendBuilder import KleinBackendBuilder
from backend.FlaskBackendBuilder import FlaskBackendBuilder
from backend.SinatraBackendBuilder import SinatraBackendBuilder
from backend.ExpressBackendBuilder import ExpressBackendBuilder
from frontend.parser import Parser
from frontend.processing import JSONLDDescriptionPrinter
from frontend.processing import TreeCleaner


class Compiler(object):

    BACKENDS = {
        'flask': FlaskBackendBuilder,
        'klein': KleinBackendBuilder,
        'express': ExpressBackendBuilder,
        'sinatra': SinatraBackendBuilder
    }

    def __init__(self, input_file, output_dir, platform):
        self._xwot_file = input_file
        self._output_dir = output_dir
        self._platform = platform

    def _parse_input_file(self, file_path):
        # parse xml xwot file
        parser = Parser()
        root_node = parser.parse(file_path)
        return root_node

    def _check_input_file(self, file_path):
        # check if input file exists
        if not os.path.exists(file_path):
            print("Input file does not exist: %s " % file_path)
            sys.exit(1)

    def _clean_tree(self, root_node):
        cleaner = TreeCleaner()
        root_node.accept(cleaner)

    def _build_backend(self, root_node):
         # select backend builder
        backend_builder = self.BACKENDS[self._platform]
        builder = backend_builder()

        # build backend
        root_node.accept(builder)

        for file_name, code in builder.output().items():
            file_name = os.path.join(self._output_dir, file_name)
            path = os.path.dirname(file_name)

            # if path does not exit
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(file_name))

            with open(file_name, 'w+') as f:
                f.write(code)

    def _create_description(self, root_node):
        file_name = os.path.join(self._output_dir, 'description.jsonld')
        description_printer = JSONLDDescriptionPrinter('')
        root_node.accept(description_printer)
        out = description_printer.output()

        with open(file_name, 'w+') as f:
            f.write(out)

    def _create_xml_xwot_file(self, xml_filepath):
        xml_str = open(xml_filepath, "r").read()
        file_name = os.path.join(self._output_dir, 'device.xwot')

        with open(file_name, 'w+') as f:
            f.write(xml_str)

    def compile(self):
        self._check_input_file(self._xwot_file)
        root_node = self._parse_input_file(self._xwot_file)

        self._clean_tree(root_node)
        self._build_backend(root_node)
        self._create_description(root_node)
        self._create_xml_xwot_file(self._xwot_file)

