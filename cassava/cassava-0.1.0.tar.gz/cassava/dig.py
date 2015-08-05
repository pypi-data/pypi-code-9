#!/usr/bin/env python
# investigate.py
"""
Dig domains. [FIXME]
"""

import subprocess
from utils import is_ip
from dbcache import dbcache

@dbcache
def dig(indicator):
    '''Perform a quick `dig +short` on the domain/IP. Platform dependent!!'''
    if is_ip(indicator):
        dig = subprocess.Popen('dig -x {} +short'.format(indicator),
                               shell=True, stdout=subprocess.PIPE)
        dig = dig.stdout.read()
    else:
        dig = subprocess.Popen('dig {} +short'.format(indicator),
                               shell=True, stdout=subprocess.PIPE)
        dig = dig.stdout.read().strip()
    if dig == '':
        dig = 'error digging {}'.format(indicator)
    return dig
