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
__all__ = ['Receiver', 'Sender', 'BaseClient', 'BaseService']

import logging
import time

from .device import RemoteDevice
from .device import Description
from . import urn_matcher, constant, message


logger = logging.getLogger('core')


class Receiver(object):

    def receive(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class Sender(object):

    def send(self, message, ip, port):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class BaseClient(object):

    def __init__(self, port, m_sender):
        logger.debug("create client")

        self._port = port
        self._lookup_table = {}  # dictionary that stores discovered devices
        self._browse_callbacks = {}
        self._urn_matcher = urn_matcher.URNMatcher()
        self._parser = message.Parser()
        self._message_protocol = message.ClientProtocol(m_sender=m_sender)

        self._event_callbacks = {
            constant.ALIVE: [],
            constant.BYEBYE: [],
            constant.RESPONSE: [],
            constant.UPDATE: []
        }

        self._hook_init()

    def _hook_init(self):
        """
        Hook method.
        """

        pass

    def on_alive(self, hook, args=None):
        """
        Registers an alive hook method.
        """

        callbacks = self._event_callbacks[constant.ALIVE]
        if hook not in callbacks:
            callbacks.append((hook, args))

    def on_response(self, hook, args=None):
        """
        Registers a response hook method.
        """

        callbacks = self._event_callbacks[constant.RESPONSE]
        if hook not in callbacks:
            callbacks.append((hook, args))

    def on_byebye(self, hook, args=None):
        """
        Registers a byebye hook method.
        """

        callbacks = self._event_callbacks[constant.BYEBYE]
        if hook not in callbacks:
            callbacks.append((hook, args))

    def on_update(self, hook, args=None):
        """
        Registers a update hook method.
        """

        callbacks = self._event_callbacks[constant.UPDATE]
        if hook not in callbacks:
            callbacks.append((hook, args))

    def remove_on_alive(self, hook):
        """
        Removes an alive hook method.
        """

        callbacks = self._event_callbacks[constant.ALIVE]
        self._event_callbacks[constant.ALIVE] = [callback for (callback, args) in callbacks if callback is not hook]

    def remove_on_response(self, hook):
        """
        Removes a response hook method.
        """

        callbacks = self._event_callbacks[constant.RESPONSE]
        self._event_callbacks[constant.RESPONSE] = [callback for (callback, args) in callbacks if callback is not hook]

    def remove_on_byebye(self, hook):
        """
        Removes a byebye hook method.
        """

        callbacks = self._event_callbacks[constant.BYEBYE]
        self._event_callbacks[constant.BYEBYE] = [callback for (callback, args) in callbacks if callback is not hook]

    def remove_on_update(self, hook):
        """
        Removes a update hook method.
        """

        callbacks = self._event_callbacks[constant.UPDATE]
        self._event_callbacks[constant.UPDATE] = [callback for (callback, args) in callbacks if callback is not hook]

    def browse(self, urn, callback=None, duration=15,
               accept='application/ld+json,application/json,application/xml,text/html'):  # */*
        headers = {'ACCEPT': accept, 'PORT': self._port}

        urn_pattern = urn
        # TODO: 2) fix multiple description problem - alive messages

        deadline_time = time.time() + duration
        available = self._discovered_devices()
        if callback is not None:
            self._browse_callbacks[(urn_pattern, deadline_time)] = (callback, available)

        self._message_protocol.send_find(urn_pattern, headers)
        if callback is not None:
            [self._run_callback(callback, device, headers['ACCEPT']) for device in available
             if self._check_match(device.urn, urn_pattern)]

    def _run_callback(self, callback, _device, accept):
        logger.debug("run callback and do a cache lookup")
        if _device.description.content_type in accept or '*/*' in accept:
            callback(_device)

    def devices(self):
        return self._discovered_devices()

    def _discovered_devices(self):
        _devices = self._lookup_table.copy()
        return [_device for _, (_, _device) in _devices.items()]

    def discovered(self, urn=None, accept='application/ld+json,application/json,application/xml,text/html'):
        return [_device for _device in self._discovered_devices() if self._check_match(_device.urn, urn) and
                (_device.description.content_type in accept or '*/*' in accept)]

    def _check_match(self, device_urn, urn_pattern):
        """ 'subtype' problem / 'mini semantic' problem """
        if urn_pattern is None:
            return True

        return self._urn_matcher.match(device_urn, urn_pattern)

    def _run_browse_callbacks(self, _device):
        """
        Runs all registered browse callbacks.
        """

        current_time = time.time()
        for (urn, deadline_time), (browse_callback, available) in self._browse_callbacks.copy().items():
            if deadline_time > current_time and self._check_match(_device.urn, urn) \
                    and not self._check_available(_device, available):
                logger.debug("run callback")
                browse_callback(_device)  # run registered browse callback

            if deadline_time <= current_time:
                logger.debug("remove callback")
                del self._browse_callbacks[(urn, deadline_time)]

    def _run_event_callbacks(self, event, _device):
        """
        Runs all hook methods that are registered to the event 'event'.
        """

        callbacks = self._event_callbacks[event]
        for callback, args in callbacks:
            callback(_device, args)

    def _check_available(self, _device, available):
        matches = [d for d in available if _device.urn == d.urn and _device.location == d.location]
        return len(matches) > 0

    def _cleanup(self):
        logger.debug("cleanup")
        self._cleanup_callbacks()
        self._cleanup_lookup_table()

    def _cleanup_callbacks(self):
        current_time = time.time()
        for (urn, deadline_time), browse_callback in self._browse_callbacks.copy().items():
            if deadline_time <= current_time:
                logger.debug("remove callback")
                del self._browse_callbacks[(urn, deadline_time)]

    def _cleanup_lookup_table(self):
        current_time = time.time()
        for key, (last_update, _device) in self._lookup_table.copy().items():
            if current_time - last_update > constant.ANNOUNCEMENT_EXPIRATION:
                urn, location, content_type = key
                logger.debug("lookup entry expired: %s / %s" % (urn, location))
                del self._lookup_table[key]

    def dispatch(self, data, addr):
        # parse message
        #try:
            message = self._parser.parse(data)

            logger.debug("dispatch message method: %s" % message.method)

            # handle search request responses from a device
            if message.method == constant.RESPONSE:
                if not (message.urn, message.location, message.content_type) in self._lookup_table:
                    logger.debug("add new entry to lookup table %s \ %s \ %s" % (message.urn, message.location,
                                                                                 message.content_type))

                    if message.is_ok:
                        description = Description(content_type=message.content_type, content=message.payload)
                        _device = RemoteDevice(urn=message.urn,
                                               location=message.location,
                                               description=description)
                        self._lookup_table[(message.urn, message.location, message.content_type)] = (time.time(), _device)
                        # execute a callback....
                        self._run_browse_callbacks(_device)
                        self._run_event_callbacks(constant.RESPONSE, _device)

            # handle alive messages
            if message.method == constant.ALIVE:
                # if key (urn, location, content_type) is not present in lookup table then add it
                if not (message.urn, message.location, message.content_type) in self._lookup_table:
                    logger.debug("add new entry to lookup table %s \ %s" % (message.urn, message.location))
                    description = Description(content_type=message.content_type, content=message.payload)
                    _device = RemoteDevice(urn=message.urn, location=message.location, description=description)
                    self._lookup_table[(message.urn, message.location, message.content_type)] = (time.time(), _device)

                    self._run_event_callbacks(constant.ALIVE, _device)

                # if key (urn, location, content_type) is present in lookup table then just update the time
                if (message.urn, message.location, message.content_type) in self._lookup_table:
                    _, _device = self._lookup_table[(message.urn, message.location, message.content_type)]
                    self._lookup_table[(message.urn, message.location, message.content_type)] = (time.time(), _device)

            # handle update messages
            if message.method == constant.UPDATE:
                logger.debug("update entry in lookup table %s \ %s" % (message.urn, message.location))
                description = Description(content_type=message.content_type, content=message.payload)
                _device = RemoteDevice(urn=message.urn, location=message.location, description=description)
                self._lookup_table[(message.urn, message.location, message.content_type)] = (time.time(), _device)

                self._run_event_callbacks(constant.UPDATE, _device)

            # handle byebye message
            if message.method == constant.BYEBYE:
                for ((urn, location, content_type), _) in self._lookup_table.copy().items():
                    if urn == message.urn and location == message.location:
                        logger.debug("remove entry from lookup table %s \ %s" % (message.urn, message.location))

                        _time, _device = self._lookup_table[(urn, location, content_type)]
                        self._run_event_callbacks(constant.BYEBYE, _device)
                        del self._lookup_table[(urn, location, content_type)]

        #except:
        #    logger.debug("message parsing error")

    def _hook_shutdown(self):
        pass

    def shutdown(self):
        self._hook_shutdown()

    def run(self, run_reactor=True):
        raise NotImplementedError


class BaseService(object):

    class DeviceEntry(object):

        def __init__(self, announcement_time, device, passive):
            self._announcement_time = announcement_time
            self._device = device
            self._passive = passive

        @property
        def announcement_time(self):
            return self._announcement_time

        @announcement_time.setter
        def announcement_time(self, time_value):
            self._announcement_time = time_value

        @property
        def device(self):
            return self._device

        @device.setter
        def device(self, val):
            self._device = val

        @property
        def passive(self):
            return self._passive

    def __init__(self, m_sender, u_sender):
        logger.debug("create service")
        self._m_sender = m_sender
        self._u_sender = u_sender

        self._device_entries = {}  # registered device by the service
        self._browse_callbacks = {}
        self._urn_matcher = urn_matcher.URNMatcher()
        self._parser = message.Parser()
        self._message_protocol = message.ServiceProtocol(m_sender=m_sender, u_sender=u_sender)

        self._hook_init()

    def _hook_init(self):
        pass

    def _create_announcement_headers(self, device, description):
        # create header
        headers = {
            'LOCATION': device.location,
            'CONTENT-TYPE': description.content_type
        }
        return headers

    def _send_announcements(self):
        current_time = time.time()
        device_entries = self._device_entries.copy().items()  # (key, device_entry)

        # filter entries that have passive discovery disabled
        device_key_pairs = [(key, entry) for (key, entry) in device_entries if entry.passive is True]

        for key, device_entry in device_key_pairs:

            device = device_entry.device
            last_announcement = device_entry.announcement_time

            if len(device.descriptions) > 0:
                description = device.descriptions[0]

                # check if announcement is still fresh enough
                if current_time - last_announcement > constant.ANNOUNCEMENT_INTERVAL:
                    logger.debug("core - send announcements!")
                    headers = self._create_announcement_headers(device, description)
                    # send alive message
                    self._message_protocol.send_alive(urn=device.urn, payload=description.content, headers=headers)
                    device_entry.announcement_time = time.time()

    def register(self, device, passive=True):
        logger.debug("register device: %s" % str(device))
        key = (device.urn, device.location)
        self._device_entries[key] = self.DeviceEntry(device=device, announcement_time=time.time(),
                                                     passive=passive)  #(time.time(), device)
        if len(device.descriptions) > 0:
            # get first device description that is available
            description = device.descriptions[0]
            headers = self._create_announcement_headers(device, description)
            self._message_protocol.send_alive(urn=device.urn, payload=description.content, headers=headers)
        else:
            logger.debug("cannot announce device on the network - description is missing")

    def update(self, device):
        logger.debug("update device: %s" % str(device))
        key = (device.urn, device.location)
        if key in self._device_entries:
            device_entry = self._device_entries[key]
            device_entry.device = device

            if len(device.descriptions) > 0:
                # get first device description that is available
                description = device.descriptions[0]
                headers = self._create_announcement_headers(device, description)
                self._message_protocol.send_update(urn=device.urn, payload=description.content, headers=headers)
            else:
                logger.debug("cannot announce device on the network - description is missing")

    def unregister(self, device):
        logger.debug("unregister device: %s" % str(device))
        key = (device.urn, device.location)
        headers = dict()
        headers['LOCATION'] = device.location
        self._message_protocol.send_byebye(urn=device.urn, headers=headers)
        del self._device_entries[key]

    def dispatch(self, data, addr):
        # parse message
        message = self._parser.parse(data)
        logger.debug("dispatch message method: %s" % message.method)

        """"
            Device logic - active discovery
            Handle search request and send back a search request response.
        """

        # handle search requests
        if message.method == constant.FIND:
            device_entry_matches = [device_entry for (urn, location), device_entry in self._device_entries.items() if
                                    self._check_match(urn, message.urn)]

            # map device entries to devices
            devices = [entry.device for entry in device_entry_matches]

            for device in devices:
                description = self._select_description(device, message)

                if description:
                    port = message.port
                    headers = {'LOCATION': device.location, 'CONTENT-TYPE': description.content_type}
                    self._message_protocol.send_response(urn=device.urn, payload=description.content,
                                                         headers=headers, addr=addr, port=port)

    def _check_match(self, device_urn, message_urn):
        """ 'subtype' problem / 'mini semantic' problem """
        return self._urn_matcher.match(device_urn, message_urn)

    def _select_description(self, device, message):
        content_types = message.accept.split(",")
        content_types = [content_type.strip() for content_type in content_types]

        # select preferred content types and ignore wildcard
        preferred_content_types = [content_type for content_type in content_types if content_type != '*/*']

        # create description lookup table
        key_value_pairs = [(description.content_type, description) for description in device.descriptions]
        description_lookup = {d_content_type: d_content for (d_content_type, d_content) in key_value_pairs}

        if len(device.descriptions) > 0:
            # check preferred descriptions
            for preferred_content_type in preferred_content_types:  # iterate using the provided preference order
                if preferred_content_type in description_lookup:
                    description = description_lookup[preferred_content_type]
                    return description

            # fallback 1
            if "*/*" in content_types:
                return device.descriptions[0]

            # fallback 2
            return device.descriptions[0]

        return None

    def _send_byebye(self):
        for (urn, location), _ in self._device_entries.items():
            self._message_protocol.send_byebye(urn=urn, headers={'LOCATION': location})

    def _hook_shutdown(self):
        pass

    def shutdown(self):
        logger.debug("shutdown service")
        self._send_byebye()
        self._hook_shutdown()

    def run(self, run_reactor=True):
        raise NotImplementedError