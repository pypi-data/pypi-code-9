#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yadp  - Yet Another Discovery Protocol
# Copyright (C) 2015  Alexander Rüedlinger
#
# This file is part of Yadp.
#
# Yadp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Yadp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yadp.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

__author__ = 'Alexander Rüedlinger'
__all__ = ['client', 'service', 'debug', 'quiet', 'create_description', 'create_device']

import logging
import os
from .twisted import Client
from .twisted import Service
from twisted.internet import reactor
from .core import constant
from .core import device

YADP_SERVICE = None
YADP_CLIENT = None


def debug():
    logging.basicConfig(level=logging.DEBUG)


def quiet():
    logging.basicConfig(level=logging.NOTSET)


def client(port=constant.UNICAST_PORT):
    global YADP_CLIENT

    if YADP_CLIENT is None:
        YADP_CLIENT = Client(reactor=reactor, port=port)
        reactor.addSystemEventTrigger('before', 'shutdown', YADP_CLIENT.shutdown)

        return YADP_CLIENT

    return YADP_CLIENT


def service():
    global YADP_SERVICE

    if YADP_SERVICE is None:
        YADP_SERVICE = Service(reactor=reactor)
        reactor.addSystemEventTrigger('before', 'shutdown', YADP_SERVICE.shutdown)

        return YADP_SERVICE

    return YADP_SERVICE


def create_device(urn, location,  **kwargs):
    content_type = kwargs.get('content_type', None)
    content = kwargs.get('content', None)
    description = kwargs.get('description', None)

    if type(content_type) is str and type(content) is str:
        description = device.Description(content=content, content_type=content_type)

    # fallback
    if description is None:
        description = device.Description(content_type='application/json', content='{}')

    return device.Device(urn=urn, location=location, descriptions=[description])


def create_description(content_type, content):
    return device.Description(content_type=content_type, content=content)


_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def get_public_frontend_path():
    return os.path.join(_ROOT, 'frontend', 'public')


def get_public_frontend_file(file):
    return os.path.join(_ROOT, 'frontend', 'public', file)