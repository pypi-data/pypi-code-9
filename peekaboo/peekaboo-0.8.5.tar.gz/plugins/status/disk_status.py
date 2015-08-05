#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
from collections import namedtuple

allowed_fs = [ 'ext3', 'ext4', 'xfs', 'hfs' ]

def disk_status():
    data = {}

    for disk in psutil.disk_partitions():
        if disk.fstype in allowed_fs:
            usage = psutil.disk_usage(disk.mountpoint)
            if disk.mountpoint == '/':
                key = 'disk.root'
            else:
                key = 'disk.%s' % disk.mountpoint.lstrip('/').replace('/', '_').lower()
            data[key + '.mountpoint'] = disk.mountpoint
            data[key + '.free_kb'] = int(usage.free / 1024)
            data[key + '.total_kb'] = int(usage.total / 1024)
            data[key + '.used_kb'] = int(usage.used / 1024)
            data[key + '.used_pct'] = int(usage.percent)

    return data

if __name__ == "__main__":
    print disk_status()
