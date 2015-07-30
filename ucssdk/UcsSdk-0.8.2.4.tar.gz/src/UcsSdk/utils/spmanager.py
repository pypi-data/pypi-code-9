"""Copyright 2013 Cisco Systems, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
This module is responsible for download the ccoimage.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Mos import LsbootPolicy
from UcsBase import UcsException, UcsUtils
sys.path.remove(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generic import add_mo_by_dn_overwrite, get_children_by_dn, get_mo_by_dn, modify_mo
import exception

boot_device_meta_dict = {
    "cdrom": ("lsbootVirtualMedia", "read-only-vm", [], {"Order": None}),
    "floppy": ("lsbootVirtualMedia", "read-write-vm", [], {"Order": None}),
    "pxe": ("lsbootLan", "lan", ["lsbootLanImagePath"], {'Type': 'lan',
                                                         'Access': 'read-only',
                                                         'Prot': 'pxe',
                                                         "Order": None}),
    "lsbootLanImagePath": ("lsbootLanImagePath", "path-primary", [],
                           {'Type': 'primary',
                            'VnicName': 'eth0'}),
    "disk": ("lsbootStorage", "storage", ["LsbootLocalStorage"], {"Order": None}),
    "LsbootLocalStorage": ("LsbootLocalStorage", "local-storage",
                           ["LsbootDefaultLocalImage"], {}),
    "LsbootDefaultLocalImage": ("LsbootDefaultLocalImage", "local-any", [],
                                {"Order": None})
}

boot_device_rn = {"read-only-vm": "cdrom",
                  "read-only-local-vm": "local_cd",
                  "read-only-remote-vm": "remote_cd",
                  "read-write-vm": "floopy",
                  "read-write-local-vm": "local_floppy",
                  "read-write-remote-vm": "remote_floppy",
                  "read-write-drive-vm": "virtual_drive",
                  "lan": "pxe",
                  "storage": "disk"}


class BootDeviceMeta(object):
    def __init__(self, *args):
        self.class_id = args[0]
        self.rn = args[1]
        self.child = args[2]
        self.config = args[3]


class BootPolicy(object):
    def __init__(self, ucsm_handle, org_dn, boot_policy_name):
        self.__handle = ucsm_handle
        self.__org_dn = org_dn
        self.__boot_policy_dn = org_dn + "/boot-policy-" + boot_policy_name
        self.__boot_policy_cfg = {LsbootPolicy.NAME: boot_policy_name,
                                  LsbootPolicy.PURPOSE: "operational",
                                  LsbootPolicy.REBOOT_ON_UPDATE: "no",
                                  LsbootPolicy.ENFORCE_VNIC_NAME: "no"
                                  }
        self.__boot_policy_obj = None

    def create(self):
        operation = "create_boot_policy"
        try:
            self.__boot_policy_obj = add_mo_by_dn_overwrite(self.__handle,
                                                            LsbootPolicy.ClassId(),
                                                            self.__boot_policy_dn,
                                                            **self.__boot_policy_cfg)
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
            boot_device = None
            boot_devices = get_children_by_dn(self.__handle, self.__boot_policy_dn)
            if boot_devices:
                for boot_device_mo in boot_devices:
                    if boot_device_mo.Order == 1:
                        boot_device = boot_device_rn[boot_device_mo.Rn]
                        break

            return {'boot_device': boot_device, 'persistent': None}
        except UcsException as ex:
            print "Cisco client exception: %ss." %(ex)
            raise exception.UcsOperationError(operation=operation, error=ex)

    def add_boot_device(self, boot_device_name, order=None):
        operation = "add_boot_device"
        boot_device_meta = BootDeviceMeta(*boot_device_meta_dict[boot_device_name])
        boot_device_dn = UcsUtils.MakeDn([self.__boot_policy_dn,
                                           boot_device_meta.rn])

        try:
            boot_policy = get_mo_by_dn(self.__handle, self.__boot_policy_dn)
            if not boot_policy:
                raise exception.UcsOperationError(operation=operation,
                                                  error="Unknown BootPolicy %s" % (
                                                      self.__boot_policy_dn))
            existing_boot_devices = get_children_by_dn(self.__handle,
                                                       self.__boot_policy_dn)
            if existing_boot_devices:
                boot_order_dict = {}
                boot_device_present = False
                boot_device_order = None
                for existing_boot_device in existing_boot_devices:
                    boot_order_dict[int(existing_boot_device.Order)] = existing_boot_device
                    if boot_device_dn == existing_boot_device.Dn:
                        boot_device_present = True
                        boot_device_order = int(existing_boot_device.Order)
                        if order and boot_device_order != order:
                            continue
                        return

                max_boot_order = max(boot_order_dict)

                if boot_device_present:
                    my_boot_device = boot_order_dict[boot_device_order]
                    other_boot_device = boot_order_dict[order]
                    self.__handle.StartTransaction()
                    self.__modify_boot_device(my_boot_device, order)
                    self.__modify_boot_device(other_boot_device, boot_device_order)

                    #                     modify_mo(self.__handle, input_mo=my_boot_device,
                    #                                                             Order=order)
                    #                     modify_mo(self.__handle, input_mo=other_boot_device,
                    #                                                 Order=boot_device_order)
                    self.__handle.CompleteTransaction()
                else:
                    if not order:
                        self.__config_boot_device(self.__boot_policy_dn, boot_device_meta, max_boot_order + 1)
                    elif order and order in boot_order_dict:
                        other_boot_device = boot_order_dict[order]
                        self.__handle.StartTransaction()
                        self.__config_boot_device(self.__boot_policy_dn, boot_device_meta, order)
                        self.__modify_boot_device(other_boot_device, max_boot_order + 1)

                        #                         modify_mo(self.__handle, input_mo=other_boot_device,
                        #                                                 Order=max_boot_order + 1)
                        self.__handle.CompleteTransaction()
                    else:
                        self.__config_boot_device(self.__boot_policy_dn, boot_device_meta, order)
            else:
                if not order:
                    self.__config_boot_device(self.__boot_policy_dn, boot_device_meta, 1)
                else:
                    self.__config_boot_device(self.__boot_policy_dn, boot_device_meta, order)

        except UcsException as ex:
            raise exception.UcsOperationError(operation=operation, error=ex)

    def __config_boot_device(self, parent_dn, boot_device_meta, order):
        child_class_id = boot_device_meta.class_id
        child_dn = UcsUtils.MakeDn([parent_dn, boot_device_meta.rn])
        child_config = boot_device_meta.config
        if child_config.has_key("Order"):
            child_config["Order"] = order

        operation = "create %s" % (child_dn)
        try:
            device_obj = add_mo_by_dn_overwrite(self.__handle,
                                                child_class_id,
                                                child_dn,
                                                **child_config)
        except UcsException as ex:
            raise exception.UcsOperationError(operation=operation,
                                              error=ex)

        if boot_device_meta.child:
            child_device_name = boot_device_meta.child[0]
            child_device_meta = BootDeviceMeta(*boot_device_meta_dict[child_device_name])
            self.__config_boot_device(device_obj.Dn, child_device_meta, order)

    def __modify_boot_device(self, boot_device_mo, order):
        if boot_device_mo.classId == "LsbootStorage":
            self.__config_boot_device(self.__boot_policy_dn,
                                      BootDeviceMeta(*boot_device_meta_dict["disk"]),
                                      order)
        else:
            modify_mo(self.__handle, input_mo=[boot_device_mo], Order=order)


class SPManager():
    def __init__(self, ucsm_handle, service_profile_dn, boot_policy_name=None):
        self.__handle = ucsm_handle
        self.__service_profile_dn = service_profile_dn
        self.__org_dn, self.__service_profile_rn = service_profile_dn.split(
            "/ls-", -1)
        if not boot_policy_name:
            self.__boot_policy_name = self.__service_profile_rn
        else:
            self.__boot_policy_name = boot_policy_name
        
        self.__boot_policy = BootPolicy(self.__handle, self.__org_dn, self.__boot_policy_name)

    def create_boot_policy(self):
        self.__boot_policy.create()

    def set_boot_device(self, boot_device_name):
        self.__boot_policy.add_boot_device(boot_device_name, order=1)
        self.attach_boot_policy()

    def get_boot_device(self):
        service_profile = get_mo_by_dn(self.__handle, self.__service_profile_dn)

        operation = "get_boot_device"
        if not service_profile:
            raise exception.UcsOperationError(operation=operation,
                                              error="Invalid Service Profile")

        if not service_profile.BootPolicyName:
            boot_dn = UcsUtils.MakeDn([self.__service_profile_dn, "boot-policy"])
            class_id = "LsbootDef"
        else:
            boot_dn = UcsUtils.MakeDn([self.__org_dn, "boot-policy-%s"%service_profile.BootPolicyName])
            class_id = "LsbootPolicy"

        operation = "get_boot_device"
        try:
            boot_device = None
            boot_devices = get_children_by_dn(self.__handle, boot_dn)
            if boot_devices:
                for boot_device_mo in boot_devices:
                    if int(boot_device_mo.Order) == 1:
                        boot_device = boot_device_rn[boot_device_mo.Rn]
                        break
            return {'boot_device': boot_device, 'persistent': None}
        except UcsException as ex:
            print "Cisco client exception: %ss." %(ex)
            raise exception.UcsOperationError(operation=operation, error=ex)

    def attach_boot_policy(self):
        service_profile = get_mo_by_dn(self.__handle, self.__service_profile_dn)
        operation = ""
        if not service_profile:
            raise exception.UcsOperationError(operation=operation,
                                              error="Invalid Service Profile")
        service_profile = modify_mo(self.__handle, [service_profile],
                                    BootPolicyName=self.__boot_policy_name)

    def detach_boot_policy(self):
        service_profile = get_mo_by_dn(self.__handle, self.__service_profile_dn)
        operation = ""
        if not service_profile:
            raise exception.UcsOperationError(operation=operation,
                                              error="Invalid Service Profile")
        service_profile = modify_mo(self.__handle, [service_profile],
                                    BootPolicyName="")
