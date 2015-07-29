#!/usr/bin/env python
import sys
import os
import argparse
import logging

from itertools import cycle
from cPickle import dump
from mysql.utilities.common.parser import SlowQueryLog

logging.basicConfig()
log = logging.getLogger(__name__)


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
            log.error("outdir exists but is not a directory")
            sys.exit(1)

def check_outdir(output_dir, force=False):
    data_files = [f for f in os.listdir(output_dir) if f.endswith('.data')]
    if data_files:
        if force:
            map(os.unlink, [os.path.join(output_dir, f) for f in data_files])
        else:
            log.error("Data files already present on outdir, you can ignore this error with --force")
            sys.exit(1)


def prepare_log(logfile, threads=8, output_dir="prepared", force=False, databases=""):
    log = SlowQueryLog(open(logfile))
    outfiles = cycle(preparte_outputs(output_dir, threads, force))

    # if databases was provided, convert to a list
    if databases:
        databases = [d.strip() for d in databases.split(',')]

    for line in log:
        # skip entries not included in databases
        if databases and line.database not in databases:
            continue

        out_file = outfiles.next()
        dump(line, out_file)


def main():
    parser = argparse.ArgumentParser(
        prog="mysql-replay-prepare",
        description="""Parse a mysql slow log and prepare files for the mysql-replay tool""")

    parser.add_argument('-p', '--parallel', help='how many processes will be used to becnhmark the server', default=8, type='int')
    parser.add_argument('-o', '--outdir', help='directory where prepared files will be stored', default='PREPARED')
    parser.add_argument('-f', '--force', action='store_true', help='if outdir already exists and is not empty, delete data files on it')
    parser.add_argument('-d', '--databases', help='filter databases to prepare, one or more separated by commas', default="")
    parser.add_argument('slowlog', help='The mysql slow log to process')
    args = parser.parse_args()

    prepare_log(args.slowlog, args.parallel, args.outdir, args.force, args.databases)


if __name__ == "__main__":
    main()
