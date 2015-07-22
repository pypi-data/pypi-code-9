# -*- coding: utf-8 -*-
import re
import sys
import codecs
import socket
import subprocess
from websocket import create_connection
from subprocess import Popen, PIPE
from os import makedirs
from os.path import exists, dirname
from .daemon import Daemon


def write(dist, content):
    dir_ = dirname(dist)
    if not exists(dir_):
        makedirs(dir_)
    with codecs.open(dist, 'w', 'utf-8') as f:
        f.write(content)


class Process(Daemon):

    def __init__(self, websocket, dist, s_dist, p_dist):
        super(Process, self).__init__(pidfile='/tmp/daemon-glb-slave.pid')
        self.websocket = websocket
        self.dist = dist
        self.s_dist = s_dist
        self.p_dist = p_dist
        self.conn = self._get_connection()
        self._run()

    def _get_connection(self):
        try:
            return create_connection(self.websocket)
        except socket.error as e:
            print "Connection failed: %r" % e
            sys.exit(1)

    def _get_local_address(self):
        return re.search('\d+\.\d+\.\d+\.\d+',
                         Popen('ifconfig', stdout=PIPE).stdout.read()).group(0)

    def _run(self):
        while True:
            self.conn.send(self._get_local_address())
            res_content = self.conn.recv()
            if res_content:
                res = eval(res_content)
                self.write_pems(res['crts'])
                self.update_cfg(res['cfg'])
                self.reload_service()

    def stop(self):
        self.conn.close()
        super(Process, self).stop()

    def update_cfg(self, content):
        write(self.dist, content)

    def write_pems(self, pems):
        for pem in pems:
            file_name = "%s_%s.pem" % (pem['domain'], pem['port'])
            file_content = "\n".join(pem['certificate'].values())
            write("%s%s" % (self.p_dist, file_name), file_content)

    def reload_service(self):
        subprocess.call('%s reload' % self.s_dist, shell=True)
