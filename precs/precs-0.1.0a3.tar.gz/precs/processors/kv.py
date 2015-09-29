from __future__ import print_function
from click import echo
from functools import wraps
import json
import sys
import StringIO


def coroutine(func):
    @wraps(func)
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr

    return start


def parse_kv(rd, ed, fd, files):
    line_generator(files, record_generator(rd, entry_generator(ed, kv_generator(fd, publisher()))))


def line_generator(files, consumer):
    if files:
        for fname in files:
            with open(fname) as f:
                for l in f:
                    consumer.send(l)
    else:
        for l in sys.stdin:
            consumer.send(l)

    consumer.close()


@coroutine
def record_generator(delim, entry_gen):
    try:
        record = StringIO.StringIO()
        while True:
            data = (yield)
            if data:
                tokens = data.split(delim)
                if len(tokens) == 1 and len(tokens[0]) == len(data):
                    ''' This is the case where we didn't find any delimiter.
                        so we'll keep appending the data to the record.'''
                    record.write(data)
                elif len(tokens) == 1:
                    # We found exactly one record.
                    record.write(tokens[0])
                    entry_gen.send(record.getvalue())
                    record = StringIO.StringIO()
                else:
                    ''' This is the case where we found more than one records
                        on the same line.'''
                    # Send the first record.
                    record.write(tokens[0])
                    entry_gen.send(record.getvalue())
                    record = StringIO.StringIO()

                    # Send all but the last. We can't combine
                    for r in tokens[1:-1]:
                        entry_gen.send(r)

                    # Send the last record only if its complete.
                    last = tokens[-1]
                    if data.endswith(delim):
                        entry_gen.send(last)
                    else:
                        record.write(last)
    except GeneratorExit:
        entry_gen.send(record.getvalue())
        entry_gen.close()


@coroutine
def entry_generator(delim, kv_gen):
    try:
        while True:
            record = (yield)
            entries = record.split(delim)
            for entry in entries:
                entry = entry.strip()
                if entry:
                    kv_gen.send(entry)

            # None value signals end of record.
            kv_gen.send(None)
    except GeneratorExit:
        kv_gen.close()


@coroutine
def kv_generator(delim, pub):
    try:
        while True:
            data = (yield)
            if data:
                (k, d, v) = data.partition(delim)
                if False in (k, d, v):
                    # Its probably a bad record.
                    continue
                k = k.strip()
                v = v.strip()
                pub.send({k: v})
            else:
                # This was the end of record indicator
                pub.send(None)
    except GeneratorExit:
        pub.close()


@coroutine
def publisher():
    try:
        record = {}
        while True:
            p = (yield)
            if p:
                for k, v in p.items():
                    record[k] = v
            elif record:
                echo(json.dumps(record, sort_keys=True))
                record = {}
    except GeneratorExit:
        if record:
            echo(json.dumps(record, sort_keys=True))
