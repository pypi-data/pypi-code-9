#!/usr/bin/env python2

__author__ = 'pgmillon'

import sys
import json

def main():
    if len(sys.argv) == 2:
        infile = sys.stdin
        outfile = sys.stdout
        path = sys.argv[1]
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'rb')
        outfile = sys.stdout
        path = sys.argv[2]
    else:
        raise SystemExit(sys.argv[0] + " [infile] 'property'")
    with infile:
        try:
            obj = json.load(infile)
        except ValueError, e:
            raise SystemExit(e)
    with outfile:
        outfile.write(eval(path, {}, {"this": obj}) + '\n')

if __name__ == '__main__':
    main()
