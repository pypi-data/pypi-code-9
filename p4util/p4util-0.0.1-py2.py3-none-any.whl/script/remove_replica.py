#!/usr/bin/env python3

from __future__ import print_function
import P4
import sys

def delete_replica(replica):
    p4 = P4.P4()
    p4.connect()

    for c in p4.run_configure("show", replica):
        p4.run_configure("unset", "{}#{}".format(replica, c["Name"]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need replica name")
        sys.exit(1)
    replica = sys.argv[1]

    delete_replica(replica)

