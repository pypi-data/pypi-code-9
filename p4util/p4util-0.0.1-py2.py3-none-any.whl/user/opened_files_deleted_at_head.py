#!/usr/bin/env python2.7

# User contributed content on the Perforce Public Depot is not supported
# by Perforce, although it may be supported by its author. This applies
# to all contributions even those submitted by Perforce employees.

# If you have any comments or need any help with the content of this
# particular folder, please contact lcheung@perforce.com, and I will
# try to help.

from __future__ import print_function
from .. import p4cli

if __name__ == '__main__':
    print('Note: you should run "p4 sync" before running this script.')
    p4 = p4cli.P4()
    p4.connect()
    havelist = p4.run_have()
    havefiles = [x['depotFile'] for x in havelist]

    for f in p4.run_opened():
        if f['depotFile'] not in havefiles:
            print("{}#head".format(f['depotFile']), '-', '{}#{}'.format(f['clientFile'], f['rev']))
