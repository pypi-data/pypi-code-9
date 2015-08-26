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

__author__ = 'Alexander Rüedlinger'

TTL = 1  # time-to-live
MULTICAST_ADDR = "224.0.0.15"  # multicast group
BIND_ADDR = "0.0.0.0"
MULTICAST_PORT = 2015
UNICAST_PORT = 2016

NAME = "YADP"
VERSION = "1.0"
PROTOCOL = "%s/%s" % (NAME, VERSION)

CRLN = "\r\n"
FLAGS = 0

RECEIVE_MAX_BYTES = 500000  # 8 KiB
ANNOUNCEMENT_INTERVAL = 60  # 1 minute
ANNOUNCEMENT_EXPIRATION = 300  # 5 minutes

FIND = 'FIND'
ALIVE = 'ALIVE'
BYEBYE = 'BYEBYE'
RESPONSE = 'RESPONSE'
UPDATE = 'UPDATE'