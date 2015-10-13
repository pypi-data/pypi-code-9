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
import socket
from xwot.compiler.frontend.processing import JSONLDDescriptionBuilder
import xmltodict
import json


def local_ip():
    # source: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s
            in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


def create_description(xwot_file, site='', base=None):
    description_builder = JSONLDDescriptionBuilder()
    out = description_builder.build(xml_file=xwot_file, site=site, base=base)
    return out


def dir_path(file):
    return os.path.dirname(os.path.realpath(file))


def parent_dir_path(file):
    return os.path.dirname(dir_path(file))



CONTENT_TYPES = {
    'application/xml': xmltodict.parse,
    'application/json': json.loads,
    'application/ld+json': json.loads
}


def deserialize(data, content_type):
    _list = content_type.split(';')  # parse content type headers e.g.: application/json;charset=UTF-8
    try:
        _content_type = _list[0]
        if _content_type in CONTENT_TYPES and data:
            deserializer = CONTENT_TYPES[_content_type]
            res = deserializer(data)
            return res
        else:
            return {}
    except:
        return {}