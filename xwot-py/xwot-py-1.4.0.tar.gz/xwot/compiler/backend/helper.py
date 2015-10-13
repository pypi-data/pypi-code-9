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

import os


class OutputPrinter(object):
    """
    OutputPribter is used to generate code.
    """

    def __init__(self):
        # a key in the dictionary represents a file name
        # each key is associated with a list of strings
        # the strings are more or less expressions or statements in some programming language
        self._output = {}

    def indent(self, items):
        return "\n".join([("    %s" % item) for item in items])

    def _add_line(self, item, node_name):
        node_name = tuple(node_name)
        if node_name not in self._output:
            self._output[node_name] = []

        self._output[node_name].append(item)
        self._output[node_name].append("\n")

    def code(self, lines, node_name):
        lines.append("")
        [self._add_line(item, node_name) for item in lines]

    def flatten(self, items):
        return [val for sub_list in items for val in sub_list]

    def flush(self):
        dic = {}
        for node_name, lines in self._output.items():
            out = ''
            for line in lines:
                out += line
            simple_node_name = os.path.join(*node_name)
            dic[simple_node_name] = out

        self._output = {}
        return dic
