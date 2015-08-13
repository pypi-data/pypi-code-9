"""rds_sort - Sort RDS files by time of first RDS record
Usage:
    rds_sort

File names are given on stdin.

List of sorted file names is printed to stdout.

"Age" of the file is determined by reading the first valid RDS record in the
file and using timestamp mentioned there.

If there are two files having the same timestamp (which are expressed with
precission of seconds) in the first RDS record, the command returns status 1.
"""
import sys
from py.path import local
import re
from itertools import groupby


# Pattern for parsing RDS record
RDSPATT = re.compile((r'^(?P<rds>[0-9A-Za-z\*]{16})\;'
                      '(?P<sig>[0-9a-zA-Z]{1,2})\;'
                      '(?P<par2>[0-9a-zA-Z]{1,2})\;'
                      '(?P<freq>[0-9\.]+ MHz)\;'
                      '(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)$'))


def get_rdstime(fname):
    """Read RDS file and return first found timestamp string

    Note, that the timestamp string must be in ISO format YYYY-MM-DDTHH:MM:SSZ

    Return None, if no such datetime was found.
    """
    with fname.open() as f:
        for line in f:
            line = line.strip()
            try:
                m = RDSPATT.search(line)
                ts = m.group("ts")
                return ts
            except AttributeError:
                continue


def main():
    fnames = sys.stdin.read().splitlines()
    # convert fnames into py.path.local instances

    fnames = [local(fname.strip()) for fname in fnames]

    # check, the files exist
    for fname in fnames:
        msg = "{fname} must exist".format(fname=fname.strpath)
        assert fname.exists(), msg

    # find timestamps of RDS records (as list of tuples (fname, ts))
    file_times = []
    for fname in fnames:
        ts = get_rdstime(fname)
        file_times.append((fname, ts))
    file_times.sort(key=lambda itm: itm[1])
    err_found = False
    for ts, fnames in groupby(file_times, key=lambda itm: itm[1]):
        fnames = list(fnames)
        if ts is None:
            msg = "WARNING: Some file(s) have no valid RDS record. Ignoring:\n"
            sys.stderr.write(msg)
            for fname, ts in fnames:
                msg = "- {fname.strpath}\n".format(fname=fname)
                sys.stderr.write(msg)
            continue
        elif len(fnames) > 1:
            err_found = True
            msg = "ERROR: Multiple files with data starting at {ts} found:\n"
            sys.stderr.write(msg.format(ts=ts))
            for fname, ts in fnames:
                msg = "- {fname.strpath}\n".format(fname=fname)
                sys.stderr.write(msg)
        for fname, ts in fnames:
            print(fname.strpath)
    if err_found:
        sys.exit(1)


def script():
    from docopt import docopt
    docopt(__doc__)
    main()


if __name__ == "__main__":
    script()
