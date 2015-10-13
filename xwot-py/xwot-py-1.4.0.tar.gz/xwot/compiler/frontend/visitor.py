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
import copy


class Visitable:

    def accept(self, node):
        raise NotImplementedError


class Visitor(object):
    def visit_entity(self, node):
        raise NotImplementedError

    def visit_resource(self, node):
        raise NotImplementedError

    def visit_device_resource(self, node):
        raise NotImplementedError

    def visit_sensor_resource(self, node):
        raise NotImplementedError

    def visit_service_resource(self, node):
        raise NotImplementedError

    def visit_actuator_resource(self, node):
        raise NotImplementedError

    def visit_tag_resource(self, node):
        raise NotImplementedError

    def visit_context_resource(self, node):
        raise NotImplementedError

    def visit_publisher_resource(self, node):
        raise NotImplementedError

    def visit_publisher_client_resource(self, node):
        raise NotImplementedError

    def visit_device(self, node):
        raise NotImplementedError

    def visit_sensor(self, node):
        raise NotImplementedError

    def visit_actuator(self, node):
        raise NotImplementedError

    def visit_tag(self, node):
        raise NotImplementedError


class BaseVisitor(Visitor):

    def __init__(self):
        self._entity_node = None
        self._nodes = []

    def before(self):
        pass

    def after(self):
        pass

    def before_resource(self, node):
        pass

    def after_resource(self, node):
        pass

    def visit_entity(self, node):
        #node.set_name('RootResource')
        self._entity_node = node
        self._nodes.append(node)
        self.before()
        self.handle_entity(node)
        [child.accept(self) for child in node.children() if child.is_virtual()]
        self.after()

    def visit_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_device_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_device_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_sensor_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_sensor_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_service_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_service_resource(node)
        self.after_resource(node)

    def visit_actuator_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_actuator_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_tag_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_tag_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_context_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_context_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_publisher_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_publisher_resource(node)
        self.after_resource(node)

        node2 = copy.deepcopy(node)
        nodename = 'ClientResource'.join(node2.name().rsplit('Resource', 1))
        if node.name() == nodename:
            nodename += 'Client'
        node2.set_name(nodename)
        node2.set_fullpath(node2.fullpath()+'/<clientid>')
        self._nodes.append(node2)
        self.before_resource(node2)
        self.handle_publisher_client_resource(node2)
        self.after_resource(node2)



    def visit_device(self, node):
        pass

    def visit_sensor(self, node):
        pass

    def visit_actuator(self, node):
        pass

    def visit_tag(self, node):
        pass

    def handle_entity(self, node):
        pass

    def handle_resource(self, node):
        pass

    def handle_device_resource(self, node):
        pass

    def handle_sensor_resource(self, node):
        pass

    def handle_tag_resource(self, node):
        pass

    def handle_context_resource(self, node):
        pass

    def handle_service_resource(self, node):
        pass

    def handle_actuator_resource(self, node):
        pass

    def handle_publisher_resource(self, node):
        pass

    def handle_publisher_client_resource(self, node):
        pass
