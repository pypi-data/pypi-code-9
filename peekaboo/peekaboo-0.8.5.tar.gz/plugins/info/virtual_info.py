#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

def virtual_info():
    output = Popen(['lspci'], stdout=PIPE).communicate()[0]

    data = { 'system.is_virtual': False }
    model = output.lower()
    if 'system.vmware' in model:
       data['system.virtual'] = 'VMware'
       data['system.is_virtual'] = True
    elif 'virtualbox' in model:
       data['system.virtual'] = 'VirtualBox'
       data['system.is_virtual'] = True
    elif 'qemu' in model:
       data['system.virtual'] = 'kvm'
       data['system.is_virtual'] = True
    elif 'virtio' in model:
       data['system.virtual'] = 'kvm'
       data['systen.is_virtual'] = True
    return data

if __name__ == "__main__":
    print virtual_info()
