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

import json
from visitor import Visitor
from parser import Parser


class TreeCleaner(Visitor):
    """
    TreeCleaner removes all physical nodes and adds absolute uri to all nodes.
    """

    def __init__(self):
        self._path = ['']

    def path(self):
        return "/".join(self._path)

    def visit_entity(self, node):
        virtual_children = [child for child in node.children() if child.is_virtual()]
        [child.accept(self) for child in virtual_children]
        node.set_children(virtual_children)

    def visit_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath
        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_device_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_sensor_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_service_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

    def visit_actuator_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_tag_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_context_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_publisher_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

    def visit_device(self, node):
        pass

    def visit_sensor(self, node):
        pass

    def visit_actuator(self, node):
        pass

    def visit_tag(self, node):
        pass


class JSONLDDescriptionPrinter(Visitor):
    """
    JSONLDDescriptionPrinter creates a minimal device description file in the jsonld format.
    """

    CHILDREN = 'knows'
    TYPE = "@type"
    ID = "@id"
    CONTEXT = '@context'

    def __init__(self, site='', base=None):
        self._output = None
        self._current = None
        self._site = self._remove_last_forwardslash(site)
        self._base = base
        self._path = [self._site]

    def _remove_last_forwardslash(self, site):
        _site = site
        if len(site) > 0:
            if site[-1] == '/':
                _site = site[0:-1]

        return _site

    @property
    def site(self):
        return self._site

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

    @site.setter
    def site(self, value):
        self._site = self._remove_last_forwardslash(value)
        self._path[0] = self._site

    def path(self):
        return "/".join(self._path)

    def visit_entity(self, node):
        self._output = {
            ("%s" % self.ID): '/',
            ("%s" % self.TYPE): 'xwot:Description',
            ("%s" % self.CHILDREN): []
        }

        before = self._output
        self._current = self._output[("%s" % self.CHILDREN)]

        [child.accept(self) for child in node.children() if child.is_virtual()]

        # overwrite entity resource and use the first child as root
        # entity resource has always at most one child !!!
        #self._output = self._output[("%s" % self.CHILDREN)][0]  # hack
        self._output[self.CONTEXT] = ["http://xwot.lexruee.ch/contexts/xwot"]

    def visit_resource(self, node):
        resource = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Web_resource",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Resource"
            },
            ("%s" % self.TYPE): 'xwot:Resource',
            ("%s" % self.CHILDREN): []
        }

        self._current.append(resource)
        before = self._current
        self._current = resource[("%s" % self.CHILDREN)]
        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_device_resource(self, node):
        device = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Computer_appliance",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Device"
            },
            ("%s" % self.TYPE): 'xwot:Device',
            ("%s" % self.CHILDREN): []
        }

        self._current.append(device)
        before = self._current
        self._current = device[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_sensor_resource(self, node):
        sensor = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Sensor",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Sensor"
            },
            ("%s" % self.TYPE): 'xwot:Sensor',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(sensor)

        before = self._current
        self._current = sensor[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_service_resource(self, node):
        service = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Service",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Service"
            },
            ("%s" % self.TYPE): 'xwot:Service'
        }
        self._current.append(service)

    def visit_actuator_resource(self, node):
        actuator = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            ("%s" % self.TYPE): 'xwot:Actuator',
            'sameAs': "http://www.productontology.org/id/Actuator",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Actuator"
            },
            ("%s" % self.CHILDREN): []
        }
        self._current.append(actuator)

        before = self._current
        self._current = actuator[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_tag_resource(self, node):
        tag = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Automatic_identification_and_data_capture",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Tag"
            },
            ("%s" % self.TYPE): 'xwot:Tag',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(tag)

        before = self._current
        self._current = tag[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_context_resource(self, node):
        context = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Context",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Context"
            },
            ("%s" % self.TYPE): 'xwot:Context',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(context)

        before = self._current
        self._current = context[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_publisher_resource(self, node):
        publisher = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'label': node.name(),
            'sameAs': "http://www.productontology.org/id/Publish%E2%80%93subscribe_pattern",
            'additionalType': {
                '@id': "http://xwot.lexruee.ch/vocab/core#Publisher"
            },
            ("%s" % self.TYPE): 'xwot:Publisher',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(publisher)

    def visit_device(self, node):
        device = {
            'label': node.name(),
            ("%s" % self.TYPE): 'xwot:Device',
            ("%s" % self.CHILDREN): []
        }

        self._current.append(device)
        before = self._current
        self._current = device[("%s" % self.CHILDREN)]

        for child in node.children():
            child.accept(self)

        self._current = before

    def visit_sensor(self, node):
        sensor = {
            'label': node.name(),
            ("%s" % self.TYPE): 'xwot:Sensor'
        }
        self._current.append(sensor)

    def visit_actuator(self, node):
        actuator = {
            'label': node.name(),
            ("%s" % self.TYPE): 'xwot:Actuator'
        }
        self._current.append(actuator)

    def visit_tag(self, node):
        tag = {
            'label': node.name(),
            ("%s" % self.TYPE): 'xwot:Tag'
        }
        self._current.append(tag)

    def output(self):
        if self._base is not None:
            self._output[self.CONTEXT].append({
                "@base": self._base
            })

        out = json.dumps(self._output, indent=4, sort_keys=True, separators=(',', ': '))
        return out


class DescriptionBuilder(object):

    def __init__(self, description_printer):
        self._description_printer = description_printer
        self._out = None

    def build(self, xml_file, site='', base=None):
        parser = Parser()
        root_node = parser.parse(xml_file)

        # set properties for creating absolute paths
        self._description_printer.site = site  # uses the site path as prefix for all relative uris
        self._description_printer.base = base  # sets the jsonld @base property in @context

        root_node.accept(self._description_printer)
        self._out = self._description_printer.output()
        return self._out

    def output(self):
        return self._out


class JSONLDDescriptionBuilder(DescriptionBuilder):

    def __init__(self):
        super(JSONLDDescriptionBuilder, self).__init__(JSONLDDescriptionPrinter())
