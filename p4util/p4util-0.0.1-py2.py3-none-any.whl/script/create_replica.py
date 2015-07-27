#!/usr/bin/env python
from __future__ import print_function
import P4
import sys

def make(name, option):
        return "{0}#{1}=".format(name, option)

def create_replica(root, name, target, number):
        p4 = P4.P4()
        p4.connect()

        p4.run_configure("set", make(name, "P4TARGET") + target)
        p4.run_configure("set", make(name, "P4TICKETS") + "{}.p4tickets".format(root))
        p4.run_configure("set", make(name, "db.replication") + "readonly")
        p4.run_configure("set", make(name, "lbr.replication") + "readonly")
        p4.run_configure("set", make(name, "monitor") + "1")
        p4.run_configure("set", make(name, "rpl.forward.all") + "1")
        p4.run_configure("set", make(name, "serviceUser") + "service_user")
        p4.run_configure("set", make(name, "startup.1") + "pull -i 1")
        for n in range(2, number + 2):
            p4.run_configure("set", make(name, "startup.{}".format(n)) + "pull -i 1 -u" )

        p4.disconnect()

if __name__ == "__main__":
        if len(sys.argv) < 5:
                print("Usage: create_repl root name P4TARGET number")
                sys.exit(1)
        root = sys.argv[1]
        name = sys.argv[2]
        target = sys.argv[3]
        number = int(sys.argv[4])

        create_replica(root, name, target, number)

