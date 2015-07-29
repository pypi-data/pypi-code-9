#!/usr/bin/env python
import sys
import os
from itertools import cycle
from cPickle import dump
from mysql.utilities.common.parser import SlowQueryLog

def preparte_outputs(output_dir, threads):
    outputs = []
    for i in range(threads):
        filename = '%s/%s.data' % (output_dir, i)
        if os.path.isfile(filename):
            raise Exception("Output dir must be empty")

        outputs.append(open(filename, 'wa'))
    return outputs

def prepare_log(logfile, threads=8, output_dir="prepared"):
    log = SlowQueryLog(open(logfile))
    outfiles = cycle(preparte_outputs(output_dir, threads))

    for line in log:
        out_file = outfiles.next()
        dump(line, out_file)


def main():
    if len(sys.argv) < 2:
        print "Usage: prepare filename"
        sys.exit(1)

    prepare_log(sys.argv[1])


if __name__ == "__main__":
    main()
