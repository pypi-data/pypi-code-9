#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import re

def _get_display_adapter(path):
    # Get pci bus, device and function
    pci = re.split(':|\.', path.replace('/sys/bus/pci/devices/0000:', ''))
    bus_num = pci[0]
    device_num = pci[1]
    device_func = '.' + pci[2]

    # Get vendor id
    f = open(path + '/vendor', 'r')
    vendor_id = f.readline().rstrip().replace('0x', '')
    f.close

    # Get device id
    f = open(path + '/device', 'r')
    device_id = f.readline().rstrip().replace('0x', '')
    f.close

    # Get boot display adapter
    f = open(path + '/boot_vga', 'r')
    boot_device = bool(f.readline().rstrip())
    f.close

    # Get vendor and device name
    vendor_name = ''
    device_name = ''
    no_cols = 1
    with open('/usr/share/hwdata/pci.ids') as f:
        for line in f:
            col = re.split('\s+', line, no_cols)
            if col[0] == vendor_id:
                vendor_name = col[1].rstrip()
                no_cols += 1
                continue
            if vendor_name != '' and col[1] == device_id:
                device_name = col[2].rstrip()
                break
            if vendor_name != '' and col[0] != '':
                break

    key = 'display.%s%s%s' % (bus_num, device_num, device_func.lstrip('.'))
    data = {}
    data[key + '.path'] = path
    data[key + '.pci.bus'] = bus_num
    data[key + '.pci.device'] = device_num
    data[key + '.pci.function'] = device_func
    data[key + '.vendor.id'] = vendor_id
    data[key + '.vendor.name'] = vendor_name
    data[key + '.device.id'] = device_id
    data[key + '.device.name'] = device_name
    data[key + '.boot_device'] = boot_device

    return data

def display_adapters():
    # Find display adapters
    data = {}
    files = glob.glob('/sys/bus/pci/devices/*/class')
    for file in files:
        f = open(file, 'r')

        # Only consider devices with device class 0x030000
        if f.readline().rstrip() == '0x030000':
            data.update(_get_display_adapter(file.replace('/class', '')))
        f.close()
    return data

if __name__ == "__main__":
    print display_adapters()
