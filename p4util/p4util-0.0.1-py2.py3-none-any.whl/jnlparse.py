#!/usr/bin/env python3
'''-*- mode: python -*-

Lester's journal parser in Python!

$Id: //guest/lester_cheung/p4util/p4util/jnlparse.py#2 $
$Change: 9988 $
$DateTime: 2014/08/13 20:31:36 $
$Author: lester_cheung $

TODO
----
* handles ckps in different encodings
* handles messed up checkpoints with mixed encodings (open streams in binary mode)

'''
import os
import sys
import six
import gzip
from pprint import pprint
from datetime import datetime
from .helper import log, bail
from six import print_

# def decode_jnl_string(s):
#     if not s.startswith(b'@'):
#         try:
#             assert(not s.endswith(b'@'))
#         except Exception as e:
#             print(e)
#             pprint(s)
#         return s
#     return s.strip(b'@').replace(b'@@', b'@')

def trace(name, data):
    '''trace a generator'''
    for d in data:
        print_(name, '=>', d, end='') # the "end" argument will break in python2.7
        yield d

def gen_lines(*files, mode='rt', encoding=None, errors=None):
    '''input filenames, generates lines'''
    for f in files:
        if f.endswith('.gz'):
            input = gzip.open(f, mode=mode, encoding=encoding, errors=errors)
        else:
            input = open(f, mode=mode, encoding=encoding, errors=errors)
        for line in input:
            yield line

def gen_recs(lines):
    '''input lines, generates record lines'''
    rec_actions = '@pv@ @dv@ @rv@ @ex@ @nx@ @mx@'.split()
    rec = []
    for line in lines:
        if rec and len(line)>3 and \
           line[0:4] in rec_actions: # record ends
            yield '\n'.join(rec)
            rec = []
        rec.append(line)

def gen_filter_rectypes(recs, include=[], exclude=[]):
    for i in include:
        if i in exclude:
            include.remove(i)

    for r in recs:
        if len(r)<4:
            yield r             # corrupted record?
        if r[0:4] in exclude:
            continue
        if include:
            if r[0:4] in include:
                yield r
            continue
        yield r

def gen_filter_tables(recs, include=[], exclude=[]):
    for i in include:
        if i in exclude:
            exclude.remove(i)
    for r in recs:
        s = r.split(None, 3)
        if len(s) < 3:
            yield r
        if s[2] in exclude:
            continue
        if include:
            if s[2] in include:
                yield r
            continue
        yield r

def gen_tokens(rec):
    tok = []
    in_quote = False
    for c in rec:
        if tok and not in_quote and c == ' ':
            yield ''.join(tok)
            tok = []
            continue
        if c == '@':
            in_quote = not in_quote
        tok.append(c)

class P4Journal(object):

    def __init__(self, *journals, rectypes=[], skip_rectypes=[], tables=[], skip_tables=[]):
        recs = gen_recs(gen_lines(*journals))
        if rectypes or skip_rectypes:
            # recs = trace('gen_recs', recs)
            recs = gen_filter_rectypes(recs, include=rectypes, exclude=skip_rectypes)
            # recs = trace('gen_filter_rectypes', recs)
        if tables or skip_tables:
            recs = gen_filter_tables(recs, include=tables, exclude=skip_tables)
        self.recs = recs

    def __iter__(self):
        return self

    def __next__(self):
        return list(gen_tokens(self.recs.__next__()))

    def next(self):             # python 2.7 style
        return self.recs.next()


if __name__ == '__main__':
    fname,tbl = sys.argv[1:3]
    j = P4Journal(fname
                  ,rectypes=['@pv@']
                  ,tables=[tbl]
    )
    i=0
    started = datetime.now()
    for r in j:
        i+=1
        cols = sys.argv[3:]
        if cols:
            for idx in sys.argv[3:]:
                print_("{} ".format(r[int(idx)]), end='')
            print_()
        else:
            pprint(r)
    dt = datetime.now() - started
    log.info('emitted {} records, in {}'.format(i, dt))
    log.info('{:,.3f} bytes/sec'.format(jnl.parsed_bytes/dt.total_seconds()))

    # for line in gen_lines(*sys.argv[1:]):
    #     print_ (line, end='')
