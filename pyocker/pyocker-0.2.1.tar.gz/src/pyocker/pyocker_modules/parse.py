#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml

def parse_config(filepath):
    try:
        with open(filepath, 'r') as f:
            config = yaml.load(f)
    except Exception as e:
        sys.stderr.write('Cannot read config file %s\n' % filepath)
        exit()
    return config
