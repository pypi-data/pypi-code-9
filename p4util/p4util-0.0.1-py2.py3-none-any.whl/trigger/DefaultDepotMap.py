#!/usr/bin/env python

from __future__ import print_function
import P4
import sys

def set_map(filename, basePath):
    p4 = P4.P4()

    with open(filename) as f:
        content = f.read()
    depotSpec = p4.parse_depot(content)
    
    depot = depotSpec['Depot']
         
    depotMap = basePath + "/" + depot + "/..."

    depotSpec['Map'] = depotMap

    content = p4.format_depot(depotSpec)

    with open(filename, "w") as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: depotspec basepath")
        sys.exit(1)

    filename = sys.argv[1]
    basePath = sys.argv[2]

    set_map(filename, basePath)
