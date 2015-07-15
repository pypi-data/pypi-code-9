#!/usr/bin/python

import sys

f = open(sys.argv[1])
lines = f.readlines()

c = 0
for l in lines[3:]:
    c += 1
    if c %4 == 1:
        print l.strip()
    if c %4 == 3:
        print "\t", l.strip()
    if c %4 == 0:
        print l.strip()


