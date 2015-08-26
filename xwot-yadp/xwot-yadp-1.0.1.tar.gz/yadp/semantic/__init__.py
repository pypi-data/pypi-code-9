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
__all__ = ['client', 'debug', 'quiet']

import logging
from .core import Client
from yadp.core import constant




SEMANTIC_YADP_CLIENT = None


def debug():
    logging.basicConfig(level=logging.DEBUG)


def quiet():
    logging.basicConfig(level=logging.NOTSET)


def client(port=constant.UNICAST_PORT):
    global SEMANTIC_YADP_CLIENT

    if SEMANTIC_YADP_CLIENT is None:
        import yadp
        yadp_client = yadp.client(port=port)
        SEMANTIC_YADP_CLIENT = Client(yadp_client)

    return SEMANTIC_YADP_CLIENT