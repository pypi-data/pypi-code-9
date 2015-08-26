# Copyright 2014 OpenStack Foundation
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from UcsBase import UcsException
sys.path.remove(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helper as ucs_helper
import exception
from spmanager import SPManager


class BootDeviceHelper(object):
    """Cisco UCS Service Profile Boot Device helper."""

    def __init__(self, helper=None):
        """Initialize with UCS Manager details.

            :param helper: helper object
            :param password: Login user password
            """
        self.helper = helper
        self.sp_manager = SPManager(helper.handle, helper.service_profile)

    def set_boot_device(self, device, persistent=False):
        """Set the boot device for the node.

            Set the boot device to use on next reboot of the node.
            :param device: the boot device, one of
            :mod:`ironic.common.boot_devices`.
            :param persistent: Boolean value. True if the boot device will
                persist to all future boots, False if not.
                Default: False. Ignored by this driver.
            :raises: UcsOperationError if it UCS Manager reports any error.
            """

        operation = "set_boot_device"
        try:
            self.sp_manager.create_boot_policy()
            self.sp_manager.set_boot_device(device)

        except UcsException as ex:
            raise exception.UcsOperationError(operation=operation, error=ex)

    def get_boot_device(self):
        """Get the current boot device for the node.

            Provides the current boot device of the node. Be aware that not
            all drivers support this.

            :raises: InvalidParameterValue if any connection parameters are
                incorrect.
            :raises: MissingParameterValue if a required parameter is missing
            :returns: a dictionary containing:

            :boot_device: the boot device, one of
            :mod:`ironic.common.boot_devices` or None if it is unknown.
            :persistent: Whether the boot device will persist to all
                future boots or not, None if it is unknown.
            """
        operation = 'get_boot_device'
        try:
            boot_device = self.sp_manager.get_boot_device()
            return boot_device
        except UcsException as ex:
            print(_("Cisco client exception: %(msg)s."), {'msg': ex})
            raise exception.UcsOperationError(operation=operation, error=ex)
