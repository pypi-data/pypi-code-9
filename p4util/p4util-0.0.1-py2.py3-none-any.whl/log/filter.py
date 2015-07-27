#!/usr/bin/env python3
'''Cut down the volume of P4LOG entries by remove all track
outputs without any lock wait+held timings.

This is for administrators who always log with track=1 and find
the log files too big to process - like TRACK2SQL and friends.

Usage
=====

Reading from files. They can be optionally compressed with Gzip,
Bzip2, XZ or LZMA:

  python3 filter.py log log.gz log.bz2 log.xz

Or from STDIN:

  zcat log.gz | python3 filter.py

'''

# from .helper import *
import argparse
import bz2
import gzip
import lzma                     # new in Python 3.3
import re
import sys

def gen_file_handles(fnames, mode='rt', encoding='utf8', errors='surrogateescape'):
    # surrogateescape was added in Python 3.x
    for f in fnames:
        if f.endswith('.gz'):
            fd = gzip.open(f, mode=mode, encoding=encoding, errors=errors)
        elif f.endswith('.xz') or f.endswith('.lzma'):
            fd = lzma.open(f, mode=mode, encoding=encoding, errors=errors)
        elif f.endswith('.bz2'):
            fd = bz2.open(f, mode=mode, encoding=encoding, errors=errors)
        elif f == '-':
            bstream = sys.stdin.detach()
            import io
            fd = io.TextIOWrapper(bstream, encoding=encoding, errors=errors)
        else:
            fd = open(f, mode=mode, encoding=encoding, errors=errors)
        yield fd


def gen_lines(file_handles):
    for fd in file_handles:
        for line in fd:
            yield line.rstrip() # remove any trailing whitespaces


def gen_log_entries(lines):
    e = []
    for l in lines:
        if l.startswith('Perforce server ') and l.endswith(':'):
            if e:
                yield e
            e = []
        e.append(l)
    yield e                     # end of file

re_locks_read_write = re.compile(r'---   locks read/write (\d+)/(\d+) rows get\+pos\+scan put\+del (\d+)\+(\d+)\+(\d+) (\d+)\+(\d+)')
re_tot_lock_wait_held = re.compile(r'---   total lock wait\+held read/write (\d+)ms\+(\d+)ms/(\d+)ms\+(\d+)ms')
re_max_lock_wait_held = re.compile(  r'---   max lock wait\+held read/write (\d+)ms\+(\d+)ms/(\d+)ms\+(\d+)ms')

L = {                           # LIMITS
    'DB_LOCKS'      : ( 1, 1, 1000,   10000,   100000,   100000),
    'DB_ROWS_IN'    : ( 1, 1, 10000,  100000,  1000000,  10000000),
    'DB_ROWS_OUT'   : ( 1, 1, 1000,   10000,   100000,   100000),
    'DB_READ_WAIT'  : ( 1, 1, 100,    1000,    5000,     5000),
    'DB_WRITE_WAIT' : ( 1, 1, 100,    1000,    5000,     5000),
    'DB_READ_HELD'  : ( 1, 1, 100,    100,     5000,     5000),
    'DB_WRITE_HELD' : ( 1, 1, 100,    100,     500,      500),
}

def myfilter(entry, lvl):
    '''
    Return False if the log entry should be skipped
    '''
    trackoutput = False
    for line in entry:
        if line.startswith('--- '):
            # track output
            trackoutput = True

        m = re_locks_read_write.match(line)
        if m:
            rl,wl,gr,pr,sr,putr,delr = map(int, m.groups())
            if rl > L['DB_LOCKS'][lvl] or wl > L['DB_LOCKS'][lvl] or \
               gr+sr > L['DB_ROWS_IN'][lvl] or putr+delr > L['DB_ROWS_OUT'][lvl]:
                return True

        m = re_tot_lock_wait_held.match(line)
        if m:
            rw,rh,ww,wh = map(int, m.groups())
            if rw > L['DB_READ_WAIT'][lvl] or rh > L['DB_READ_HELD'][lvl] or \
               ww > L['DB_WRITE_WAIT'][lvl] or wh > L['DB_WRITE_HELD'][lvl]:
                return True

        m = re_max_lock_wait_held.match(line)
        if m:
            rw,rh,ww,wh = map(int, m.groups())
            if rw > L['DB_READ_WAIT'][lvl] or rh > L['DB_READ_HELD'][lvl] or \
               ww > L['DB_WRITE_WAIT'][lvl] or wh > L['DB_WRITE_HELD'][lvl]:
                return True
    if trackoutput:
        return False
    return True


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='A filter for P4LOG')
    ap.add_argument('-t', '--tracklevel', type=int, default=5, choices=[0,1,2,3,4,5])
    ap.add_argument('-e', '--error-handler', choices='strict ignore replace surrogateescape'.split(),
            default='surrogateescape', help='decode error handler')
    ap.add_argument('inputs', nargs='*', default=['-'])
    args = ap.parse_args()
    print(args)

    for e in gen_log_entries(gen_lines(gen_file_handles(args.inputs, errors=args.error_handler))):
        if myfilter(e, args.tracklevel):
            print( '\n'.join(e) )
