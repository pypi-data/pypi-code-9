#!/usr/bin/env python
import sys
import os
import argparse
from itertools import cycle
from cPickle import dump
from mysql.utilities.common.parser import SlowQueryLog

def preparte_outputs(output_dir, threads, force):
    create_outdir(output_dir)
    check_outdir(output_dir, force)

    outputs = []
    for i in range(threads):
        filename = '%s/%s.data' % (output_dir, i)
        outputs.append(open(filename, 'wa'))

    return outputs

def create_outdir(output_dir):
    if not os.path.isdir(output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir, 0755)
        else:
            raise Exception("outdir exists but is not a directory")

def check_outdir(output_dir, force=False):
    data_files = [f for f in os.listdir(output_dir) if f.endswith('.data')]
    if data_files:
        if force:
            map(os.unlink, [os.path.join(output_dir, f) for f in data_files])
        else:
            raise Exception("Data files already present on outdir, you can ignore this error with --force")


def prepare_log(logfile, threads=8, output_dir="prepared", force=False):
    log = SlowQueryLog(open(logfile))
    outfiles = cycle(preparte_outputs(output_dir, threads, force))

    for line in log:
        out_file = outfiles.next()
        dump(line, out_file)


def main():
    parser = argparse.ArgumentParser(
        prog="mysql-replay-prepare",
        description="""Parse a mysql slow log and prepare files for the mysql-replay tool""")

    parser.add_argument('-p', '--parallel', help='how many processes will be used to becnhmark the server', default=8)
    parser.add_argument('-o', '--outdir', help='directory where prepared files will be stored', default='PREPARED')
    parser.add_argument('-f', '--force', action='store_true', help='if outdir already exists and is not empty, delete data files on it')
    parser.add_argument('slowlog', help='The mysql slow log to process')
    args = parser.parse_args()

    prepare_log(args.slowlog, args.parallel, args.outdir, args.force)


if __name__ == "__main__":
    main()
