#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import isfile
from subprocess import call, PIPE, CalledProcessError, check_output

def _cmd_exists(cmd):
    return call("type " + cmd, shell=True,
        stdout=PIPE, stderr=PIPE) == 0

def _get_dmi_info(name, fname):
    val = ''
    if os.access(fname, os.R_OK):
        f = open(fname, 'r')
        val = f.readline()
        f.close
    elif _cmd_exists('sudo') and _cmd_exists('dmidecode'):
        try:
            val = check_output(['sudo', 'dmidecode', '-s', 'system-serial-number'])
        except:
            pass
    return val.strip()

def dmidecode_info():
    data = {}
    data['dmi.serial_number'] = _get_dmi_info('system-serial-number', '/sys/devices/virtual/dmi/id/product_serial')
    data['dmi.manufacturer'] = _get_dmi_info('system-manufacturer', '/sys/devices/virtual/dmi/id/chassis_vendor')
    data['dmi.product_version'] = _get_dmi_info('system-product-version', '/sys/devices/virtual/dmi/id/product_version')
    data['dmi.product'] = _get_dmi_info('system-product-name', '/sys/devices/virtual/dmi/id/product_name')
    data['dmi.bios.date'] = _get_dmi_info('bios-release-date', '/sys/devices/virtual/dmi/id/bios_date')
    data['dmi.bios.vendor'] = _get_dmi_info('bios-vendor', '/sys/devices/virtual/dmi/id/bios_vendor')
    data['dmi.bios.version'] = _get_dmi_info('bios-version', '/sys/devices/virtual/dmi/id/bios_version')
    return data

if __name__ == "__main__":
    print dmidecode_info()
