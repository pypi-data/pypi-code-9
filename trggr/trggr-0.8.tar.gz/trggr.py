#!/usr/bin/env python

import signal
import sys
import os
import time
import re


WAIT_TIME = 0.05  # wait for OS to setup pipe on the terminal

CLEARER = '.trggr/clearer.pipe'
WATCHER = '.trggr/watcher.pipe'


def handler(signum, frame):
    sys.exit(0)


def clear():
    try:
        fname = os.path.join(os.getcwd(), CLEARER)
        fd = os.open(fname, os.O_WRONLY | os.O_NONBLOCK)
        os.write(fd, "_hi_\n")
        os.close(fd)
    except OSError:
        sys.stderr.write("trggrclear.py is not running\n")


def matcher():
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    else:
        pattern = ".*"
    return re.compile(pattern)


def main():
    lasttest = None
    m = matcher()
    while True:
        fname = os.path.join(os.getcwd(), WATCHER)
        pipe = os.open(fname, os.O_RDONLY)
        clear()
        time.sleep(WAIT_TIME)
        finput = os.fdopen(pipe)
        line = finput.readline()
        fname = line.split(' ')[0]
        if m.search(os.path.basename(fname)):
            lasttest = fname
        if lasttest:
            sys.stdout.write(lasttest + "\n")
            sys.stdout.flush()
        finput.close()

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    main()
