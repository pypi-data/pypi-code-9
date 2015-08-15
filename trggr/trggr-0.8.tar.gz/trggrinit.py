#!/usr/bin/env python

import signal
import sys
import os


CLEARER = 'clearer.pipe'
WATCHER = 'watcher.pipe'


def handler(signum, frame):
    sys.exit(0)


def main():
    try:
        basedir = os.path.join(os.getcwd(), '.trggr')
        os.mkdir(basedir)
        os.mkfifo(os.path.join(basedir, CLEARER))
        os.mkfifo(os.path.join(basedir, WATCHER))
    except OSError:
        pass

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    main()
