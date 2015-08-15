#!/usr/bin/env python

import subprocess
import signal
import sys
import os
import datetime


CLEARER = '.trggr/clearer.pipe'


def handler(signum, frame):
    sys.exit(0)


def clear():
    subprocess.call(["clear"])


def main():
    while True:
        fname = os.path.join(os.getcwd(), CLEARER)
        try:
            pipe = os.open(fname, os.O_RDONLY)
            clear()
            print datetime.datetime.now()
            finput = os.fdopen(pipe)
            line = finput.readline()
            finput.close()
        except OSError:
            pass

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    main()
