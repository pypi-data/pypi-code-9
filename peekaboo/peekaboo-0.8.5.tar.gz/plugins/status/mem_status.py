#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil

def mem_status():
    data = {}

    vmem = dict(psutil.virtual_memory()._asdict())
    data['mem.free_kb'] = int(vmem['available']) / 1024
    data['mem.total_kb'] = int(vmem['total']) / 1024
    data['mem.used_kb'] = data['mem.total_kb'] - data['mem.free_kb']
    data['mem.used_pct'] = int(vmem['percent'])

    swap = dict(psutil.swap_memory()._asdict())
    data['swap.free_kb'] = int(vmem['free']) / 1024
    data['swap.total_kb'] = int(vmem['total']) / 1024
    data['swap.used_kb'] = int(vmem['used']) / 1024
    data['swap.used_pct'] = int(vmem['percent'])

    return data

if __name__ == "__main__":
    print mem_status()
