"""rds_cycle
Usage:
    rds_cycle <rds_file>...

Reads RDS files in cycle and prints their lines in rate of
11.4 lines per second.

All lines following RDS data pattern

    2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:36:31Z
    24062469692E2043;33;40;92.6 MHz;2015-08-12T10:36:31Z
    2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:36:32Z

get timestamp updated to the current one.

All other lines are printed unchanged.
"""
from itertools import cycle, izip
from py.path import local
import time
from datetime import datetime
import re
import sys
import os


def ctimegen(interval=1.0/11.4):
    """Generate ctime, but not sooner than interval secs since last request."""

    nexttime = None
    while True:
        now = time.time()
        if now < nexttime:
            time.sleep(nexttime - now)
            now = nexttime
        nexttime = now + interval
        yield now

RDSPATT = re.compile((r'^(?P<rds>[0-9A-Za-z\*]{16})\;'
                      '(?P<sig>[0-9a-zA-Z]{1,2})\;'
                      '(?P<par2>[0-9a-zA-Z]{1,2})\;'
                      '(?P<freq>[0-9\.]+ MHz)\;'))


def formatline(rdsline, ctime):
    """Update time in RDS data record to the current one.

    If a line does not respect RDS pattern, AttributError exception
    is thrown.
    """
    m = RDSPATT.search(rdsline)
    rds = m.group("rds")
    sig = m.group("sig")
    par2 = m.group("par2")
    freq = m.group("freq")
    ts = datetime.utcfromtimestamp(ctime)
    msg = "{rds};{sig};{par2};{freq};{ts:%Y-%m-%dT%H:%M:%SZ}"
    return msg.format(rds=rds, sig=sig, par2=par2, freq=freq, ts=ts)


def main(fnames):
    # to prevent stdout buffering
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    # convert fnames into py.path.local instances
    fnames = map(local, fnames)

    # check, the files exists
    for fname in fnames:
        msg = "{fname} must exist".format(fname=fname.strpath)
        assert fname.exists(), msg

    timegen = ctimegen()
    for fname in cycle(fnames):
        with fname.open() as f:
            for line, ctime in izip(f, timegen):
                try:
                    print(formatline(line, ctime))
                except AttributeError:
                    print(line.rstrip())


def script():
    from docopt import docopt
    args = docopt(__doc__)
    main(args["<rds_file>"])


if __name__ == "__main__":
    script()
