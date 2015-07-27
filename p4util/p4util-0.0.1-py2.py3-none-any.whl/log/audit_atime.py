#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Reads audit log from P4D and record last access time of depot file
revisions in an SQLite database. Any previous record of the same depot
file revision is discarded on update.

Usage:

  python audit_atime.py SQLite_DB < log.audit
  python -m p4util.log.audit_atime SQLite_DB < log.audit

You can setup P4D to write to a named pipe and have this script to
read from it. For example:

  mkfifo log.audit
  p4d -r P4ROOT -A log.audit
  python audit_atime.py SQLITE_DB < log.audit

To avoid P4D blocking on this script you can use buffer(1) to increase
the queue length of the named pipe. E.g.:

  buffer -i log.audit -p 75 | python audit_atime.py SQLITE_DB


$Author: lester_cheung $
$Revision: #1 $
$Date: 2014/12/08 $
Contact: @p4lester
'''

from __future__ import print_function
import sys
import sqlite3
from datetime import datetime

if __name__ == '__main__':
    # 2011/10/19 10:42:16 lcheung@ws 127.0.0.1 print //depot/Jam/MAIN/src/Jamfile#2

    print(sys.argv)
    if len(sys.argv) != 2:
        print('usage: {} <sqlite db>'.format(sys.argv[0]))
        sys.exit(1)

    conn = sqlite3.connect(sys.argv[1], detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.execute('''CREATE TABLE IF NOT EXISTS `audit`
                (dfile TEXT, rev INTEGER, atime datetime, who TEXT,
                host TEXT, cmd TEXT, PRIMARY KEY (dfile, rev))''')

    for line in sys.stdin:
        line = line.strip()
        try:
            date, time, user_ws, host, cmd, the_rest = line.split()
        except:
            continue            # what error?
        dp_rev = ''.join(the_rest)
        x = dp_rev.split('#')
        ## PY2: convert dfile to unicode, ignoring any errors.
        # dfile = unicode('#'.join(x[:-1]), 'utf-8', 'ignore')
        dfile = '#'.join(x[:-1])
        rev = x[-1]
        # atime = '%s %s' % (date.replace('/', '-'), time)
        atime = datetime.strptime(date+time, '%Y/%m/%d%H:%M:%S')
        vals = dfile, rev, atime, user_ws, host, cmd
        conn.execute('''INSERT OR REPLACE INTO
                    audit(dfile, rev, atime, who, host, cmd) VALUES
                    (?, ?, ?, ?, ?, ?)''', vals)

    conn.commit()
