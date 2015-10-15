#!/usr/bin/env python

import subprocess
import socket
import os
from probe.rdirwatcher import RDirWatcher
#from galog import GALog

DEBUG = 3

#GALog('test_rmdirwatcher.py', DEBUG)

def test_rdirwatcher():
    subprocess.call('touch /tmp/test_rdirwatcher', shell=True)
    subprocess.call('echo comp1 > /tmp/test_rdirwatcher', shell=True)
    subprocess.call('echo comp2 >> /tmp/test_rdirwatcher', shell=True)

    cfg = {
        'debug' : DEBUG,
        'pkey_file' : '{}/.ssh/id_rsa'.format(os.environ['HOME']),
        'hostname' : socket.gethostname(),
        'username' : os.environ['USER'],
        'watch_dir' : '/tmp',
        'watch_pattern' : 'test_rdirwatcher',
        'watch_max_age' : 500,
    }

    rdir_wathcer = RDirWatcher(cfg)
    comps = rdir_wathcer.check()
    print comps
    assert comps == ['comp1', 'comp2']

    #a little hack
    os.remove('rdirwatcher.log')

if __name__ == '__main__':
    test_rdirwatcher()
