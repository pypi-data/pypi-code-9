import os, sys
from pprint import pprint
from .jnlparse import *

t = {}
dv = {}

for r in P4Journal(sys.argv[1]):
    action = r[0]
    t[action] = t.get(action, 0)+1

    if action=='@dv@':
        tbl, clientpath = r[2:4]
        toks = clientpath.split('/')
        if len(toks) < 3:
            continue
        client = toks[2]
        if tbl not in dv:
            dv[tbl] = {}
        dv[tbl][client] = dv.get(tbl, {}).get(client, 0)+1



pprint(t)
pprint(dv)
