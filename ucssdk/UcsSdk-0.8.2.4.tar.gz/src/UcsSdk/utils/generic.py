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
This module provides short methods to interact with ucsm.
"""


def get_mo_by_dn(handle, dn):
    mos = handle.GetManagedObject(None, None, {"Dn": dn})
    if mos:
        return mos[0]
    return None


def get_children_by_dn(handle, parent_dn, in_hier=False):
    return handle.GetUcsChild(inDn=parent_dn, inHierarchical=in_hier)


def add_mo_by_dn_overwrite(handle, class_id, dn, **prop_values):
    add_params = {"Dn": dn}
    add_params.update(prop_values)
    add_mo = handle.AddManagedObject(None, class_id, add_params, modifyPresent=True)
    if add_mo:
        return add_mo[0]
    return add_mo

def modify_mo(handle, input_mo, **prop_values):
    return handle.SetManagedObject(input_mo, None, prop_values)

def get_mo_hierarchy_by_dn(handle, dn):
    return handle.GetManagedObject(None, None, {"Dn": dn}, inHierarchical=True)

def get_child_mo_by_classid(handle, parent_mo, child_class_id, in_hier=False):
    return handle.GetManagedObject(inMo=parent_mo, classId=child_class_id, inHierarchical=in_hier)

def get_child_mo_by_rn(handle, parent_mo, child_rn):
    mos = handle.GetManagedObject(parent_mo, None, {"Rn": child_rn})
    if mos:
        return mos[0]
    return mos

def add_mo_under_parent(handle, parent_mo, child_class_id, over_write=False, **prop_values):
    return handle.AddManagedObject(parent_mo, child_class_id, prop_values, modifyPresent=over_write)

def modify_mo_by_dn(handle, class_id, dn, **prop_values):
    set_params = {"Dn": dn}
    set_params.update(prop_values)
    set_mo = handle.SetManagedObject(None, class_id, set_params)
    if set_mo:
        return set_mo[0]
    return set_mo

def remove_mo_by_dn(handle, class_id, dn, **prop_values):
    remove_params = {"Dn": dn}
    remove_params.update(prop_values)
    return handle.RemoveManagedObject(None, class_id, remove_params)


def remove_mo(handle, input_mo, **prop_values):
    return handle.RemoveManagedObject(input_mo, None, prop_values)
