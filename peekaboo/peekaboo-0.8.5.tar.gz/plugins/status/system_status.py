#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def load_avg_status():
    data = {}

    loadavg = os.getloadavg()
    data['system.load_avg.1min_pct'] = loadavg[0]
    data['system.load_avg.5min_pct'] = loadavg[1]
    data['system.load_avg.15min_pct'] = loadavg[2]
    return data

if __name__ == "__main__":
    print load_avg_status()
