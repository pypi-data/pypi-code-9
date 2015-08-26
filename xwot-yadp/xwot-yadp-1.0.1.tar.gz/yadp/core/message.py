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

import logging
import hashlib

from . import constant


logger = logging.getLogger('message')


class Message(object):

    def __init__(self, start_line, headers=None, payload='', method=None, urn=None, protocol=None):
        self._start_line = start_line
        self._headers = headers
        self._payload = payload
        self._method = method
        self._urn = urn
        self._protocol = protocol
        self._headers = headers or {}
        self._headers['HASH'] = hashlib.md5(payload).hexdigest()

    @property
    def is_ok(self):
        return self._headers['HASH'] == hashlib.md5(self._payload).hexdigest()

    @property
    def hash(self):
        return self._headers['HASH']

    @property
    def start_line(self):
        return self._start_line

    @property
    def payload(self):
        return self._payload

    @property
    def headers(self):
        return self._headers

    @property
    def urn(self):
        return self._urn

    @property
    def protocol(self):
        return self._protocol

    @property
    def method(self):
        return self._method

    @property
    def location(self):
        return self._headers.get('LOCATION', None)

    @property
    def port(self):
        if self._headers.get('PORT'):
            try:
                port = int(self._headers.get('PORT'))
                return port
            except:
                return constant.UNICAST_PORT

        return constant.UNICAST_PORT

    @property
    def content_type(self):
        return self._headers.get('CONTENT-TYPE', None)

    @property
    def accept(self):
        return self._headers.get('ACCEPT', None)

    def __str__(self):
        # make start line
        msg_str = "%s%s" % (self._start_line, constant.CRLN)

        # add header key values
        for key, value in self._headers.items():
            msg_str += "%s: %s%s" % (key, value, constant.CRLN)

        # indicate start of the payload
        msg_str += '<<<!' + constant.CRLN

        msg_str += self._payload

        # indicate end of the payload and end of the message
        msg_str += constant.CRLN + '!>>>' + constant.CRLN
        return msg_str


class Parser(object):

    STATE_HEADERS = 'read_headers'
    STATE_PAYLOAD = 'read_payload'
    STATE_END = 'read_end'
    METHODS = ['FIND', 'BYEBYE', 'ALIVE', 'UPDATE']
    RESPONSE = 'RESPONSE'

    def parse(self, message_str):
        state = self.STATE_HEADERS

        lines = message_str.split(constant.CRLN)
        start_line = lines[0]
        triple_value = start_line.split()

        urn = triple_value[1]

        if triple_value[0] in self.METHODS:
            method = triple_value[0]
            protocol = triple_value[2]
        else:
            method = self.RESPONSE
            protocol = triple_value[0]

        headers = dict()
        payload_buffer = list()

        for line in lines[1::]:
            # check if we encounter the payload
            if line == '<<<!' and state == self.STATE_HEADERS:
                state = self.STATE_PAYLOAD

            # check if we're reading header key values
            elif state == self.STATE_HEADERS:
                key, value = line.split(': ')  # TODO: fix hack!
                key = key.strip()
                value = value.strip()
                headers[key] = value

            # check if we reach the end of the payload
            elif line == '!>>>' and state == self.STATE_PAYLOAD:
                state = self.STATE_END

            # check if we're reading the payload
            elif state == self.STATE_PAYLOAD:
                payload_buffer.append(line)

            logger.debug("current state: %s, len: %s" % (state, len(line)))

        if state == self.STATE_END:
            payload = constant.CRLN.join(payload_buffer)
            return Message(start_line=start_line, headers=headers, payload=payload,
                           method=method, urn=urn, protocol=protocol)
        raise Exception


class Protocol(object):
    """
    Responsible for implementing the protocol message service.
    It provides service primitives for sending find, bye bye and alive messages.

    """

    def _create_start_line(self, method, urn):
        start_line = "%s %s %s" % (method, urn, constant.PROTOCOL)
        return start_line


class ServiceProtocol(Protocol):

    def __init__(self, m_sender, u_sender):
        logger.debug("init protocol")
        self._multicast_sender = m_sender
        self._unicast_sender = u_sender

    def send_response(self, urn, payload, addr, port, headers=None):
        headers = headers or {}
        start_line = "%s %s %s" % (constant.PROTOCOL, urn, "ok")
        msg = Message(start_line=start_line, headers=headers, payload=payload)
        logger.debug("send response to search request: %s" % urn)
        ip, _ = addr
        self._unicast_sender.send(msg.__str__(), ip, port)

    def send_alive(self, urn, payload, headers=None):
        headers = headers or {}
        start_line = self._create_start_line("ALIVE", urn)
        msg = Message(start_line=start_line, headers=headers, payload=payload)
        self._multicast_sender.send(message=msg.__str__())

    def send_byebye(self, urn, headers):
        start_line = self._create_start_line("BYEBYE", urn)
        msg = Message(start_line=start_line, headers=headers)
        self._multicast_sender.send(msg.__str__())

    def send_update(self, urn, payload, headers=None):
        headers = headers or {}
        start_line = self._create_start_line("UPDATE", urn)
        msg = Message(start_line=start_line, headers=headers, payload=payload)
        self._multicast_sender.send(message=msg.__str__())


class ClientProtocol(Protocol):

    def __init__(self, m_sender):
        logger.debug("init protocol")
        self._multicast_sender = m_sender

    def send_find(self, urn, headers=None):
        logger.debug("send find: %s" % urn)
        headers = headers or {}
        start_line = self._create_start_line("FIND", urn)
        msg = Message(start_line=start_line, headers=headers)
        self._multicast_sender.send(msg.__str__())