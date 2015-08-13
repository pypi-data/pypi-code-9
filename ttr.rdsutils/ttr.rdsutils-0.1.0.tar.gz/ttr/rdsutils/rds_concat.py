"""rds_concat - Concatenate RDS records from set of RDS files
Usage:
    rds_concat

File names are given on stdin.

It reads file names from stdin and prints to stdout all lines from all the
files.

If there are timestamp overlaps (last record of last file reports later datetime
than fist record in following file), warnings are printed to stderr and the
command exists with exit code 1
"""
from py.path import local
import re
import sys

# Pattern for parsing RDS record
RDSPATT = re.compile((r'^(?P<rds>[0-9A-Za-z\*]{16})\;'
                      '(?P<sig>[0-9a-zA-Z]{1,2})\;'
                      '(?P<par2>[0-9a-zA-Z]{1,2})\;'
                      '(?P<freq>[0-9\.]+ MHz)\;'
                      '(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$'))


def logerr(msg):
    sys.stderr.write(msg + "\n")


def get_rec_rdstime(line):
    """Convert RDS record line into timestamp string
    The timestamp string must be in ISO format YYYY-MM-DDTHH:MM:SSZ

    Throws AttributeError exception, if timestamp was not found.
    """
    return RDSPATT.search(line).group("ts")


def main():
    fnames = sys.stdin.read().splitlines()
    # convert fnames into py.path.local instances

    fnames = [local(fname.strip()) for fname in fnames]

    # check, the files exist
    for fname in fnames:
        msg = "{fname} must exist".format(fname=fname.strpath)
        assert fname.exists(), msg

    err_found = False
    last_ts = None
    for fname in fnames:
        with fname.open() as f:
            for lnum, line in enumerate(f):
                line = line.strip()
                try:
                    ts = get_rec_rdstime(line)
                except AttributeError:
                    print(line)
                    continue

                if last_ts and (ts < last_ts):
                    err_found = True
                    msg = ("ERROR: File: {fname.strpath}:{lnum}: "
                           "time overlap (last>current): {last_ts} > {ts}")
                    msg = msg.format(fname=fname,
                                     lnum=lnum,
                                     last_ts=last_ts,
                                     ts=ts)
                    logerr(msg)
                last_ts = ts
                print(line)
    if err_found:
        sys.exit(1)


def script():
    from docopt import docopt
    docopt(__doc__)
    main()


if __name__ == "__main__":
    script()
