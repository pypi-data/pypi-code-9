#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil

def mem_info():
    data = {}

    vmem = dict(psutil.virtual_memory()._asdict())
    data['mem.total_kb'] = int(vmem['total']) / 1024

    return data

if __name__ == "__main__":
    print mem_info()
