#!/usr/bin/env python
# -*- coding: utf-8 -*-

def cpu_info():
    f = open('/proc/cpuinfo', 'r')
    data = {
        'cpu.model': 'Unknown',
        'cpu.processors': 0,
        'cpu.threads_per_core': 0
    }

    cpu_id = None
    cpu_ids = { '0': None }
    for line in f.readlines():
        cols = line.split(':', 2)
        if len(cols) < 2:
            continue
        key = cols[0].strip()
        val = cols[1].strip()
        if key == 'model name':
            data['cpu.model'] = val.split('-')[0]
        elif key == 'processor':
            data['cpu.processors'] += 1
        elif key == 'physical id':
            cpu_id = val
            cpu_ids[cpu_id] = None
        elif key == 'cpu MHz':
            data['cpu.speed_mhz'] = int(float(val))
        elif key == 'core id':
            core_id = val
            if cpu_id == '0' and core_id == '0':
                data['cpu.threads_per_core'] += 1
        elif key == 'flags':
                data['cpu.flags'] = val.split()
        elif key == 'Features':
                data['cpu.flags'] = val.split()
    f.close()

    data['cpu.sockets'] = len(cpu_ids)
    if data['cpu.threads_per_core'] > 0:
        data['cpu.cores_per_socket'] = data['cpu.processors'] / data['cpu.sockets'] / data['cpu.threads_per_core']
    else:
        data['cpu.threads_per_core'] = 1
        data['cpu.cores_per_socket'] = 1

    return data

if __name__ == "__main__":
    print cpu_info()
