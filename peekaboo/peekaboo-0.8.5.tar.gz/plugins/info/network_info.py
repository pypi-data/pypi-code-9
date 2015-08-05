#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import netifaces
import netaddr

exclude = ['lo', 'usb0', 'docker0']

def network_info():
    data = {}
    for ifn in netifaces.interfaces():
        link = netifaces.ifaddresses(ifn)[netifaces.AF_LINK][0]
        inet = None
        if ifn in exclude:
            continue
        try:
            inet = netifaces.ifaddresses(ifn)[netifaces.AF_INET][0]
        except:
            pass

        try:
            data['interface.' + ifn + '.ipv4'] = inet['addr']
        except:
            pass
        try:
            data['interface.' + ifn + '.broadcast'] = inet['broadcast']
        except:
            pass
        try:
            data['interface.' + ifn + '.netmask'] = inet['netmask']
        except:
            pass
        try:
            data['interface.' + ifn + '.hwaddr'] = link['addr']
        except:
            pass
        try:
            cidr = netaddr.IPNetwork('{0}/{1}'.format(inet['addr'], inet['netmask']))
            data['interface.' + ifn + '.network2'] = str(cidr.network)
        except:
            pass
    return data

if __name__ == "__main__":
    print network_info()
