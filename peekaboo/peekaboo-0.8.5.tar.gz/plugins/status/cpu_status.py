#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
from collections import namedtuple

def cpu_status():
    data = {}

    cpu = psutil.cpu_times()
    data['cpu.user_sec'] = cpu.user
    data['cpu.system_sec'] = cpu.system
    data['cpu.idle_sec'] = cpu.idle

    return data

if __name__ == "__main__":
    print cpu_status()

