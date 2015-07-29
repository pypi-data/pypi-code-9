
"""
Manager for device catalog
"""

import logging
import sys

import six
from roboticeclient.common.manager import manager_factory

from . import base

LOG = logging.getLogger("devices")


def initialize(self):
    pass


def some_event(self):
    pass

subclass_body_dict = {
    "initialize": initialize,
    "some_event": some_event
}


class MetricManager(base.BaseManager):

    SCOPE = "device-catalog/metric"


class HostsManager(base.BaseManager):

    SCOPE = "device-catalog/host"


class DeviceCategoryManager(base.BaseManager):

    SCOPE = "device-catalog/category"


class BusPortManager(base.BaseManager):

    SCOPE = "device-catalog/bus-port"


class BusManager(base.BaseManager):

    SCOPE = "device-catalog/bus"


class ImageManager(base.BaseManager):

    SCOPE = "device-catalog/image"


class DeviceCatalogManager(base.BaseManager):

    SCOPE = "device-catalog"

    client_class = base.BaseManager

    manager_classes = [("images", ImageManager),
                       ("bus_ports", BusPortManager),
                       ("bus", BusManager),
                       ("hosts", HostsManager),
                       ("metrics", MetricManager)]

    def init_managers(self, **kwargs):

        for manager in self.manager_classes:

            Manager=type(manager[1].__name__, (manager_factory(self.client_class), manager[1]), {
                "initialize": initialize,
                "some_event": some_event
            })
            setattr(self, manager[0], Manager(**kwargs))

        return True

    def __init__(self, **kwargs):
        # init submanagers
        self.init_managers(**kwargs)
        # init self
        super(DeviceCatalogManager, self).__init__(**kwargs)
