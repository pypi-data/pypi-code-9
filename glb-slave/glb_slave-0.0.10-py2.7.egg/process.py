# -*- coding: utf-8 -*-
import re
import sys
import json
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


def update_service_config(path, content):
    write(path, content)


def reload_service(service_path):
    subprocess.call('%s reload' % service_path, shell=True)


class Process(Daemon):

    def __init__(self, websocket, nginx_switch,
                 haproxy_cfg_dist, haproxy_service_dist, haproxy_ssl_dist,
                 nginx_conf_dist, nginx_service_dist, nginx_ssl_dist):
        super(Process, self).__init__(pidfile='/var/run/daemon-glb-slave.pid')
        self.websocket = websocket
        self.nginx_switch = nginx_switch
        self.haproxy_cfg_dist = haproxy_cfg_dist
        self.haproxy_service_dist = haproxy_service_dist
        self.haproxy_ssl_dist = haproxy_ssl_dist

        self.nginx_conf_dist = nginx_conf_dist
        self.nginx_service_dist = nginx_service_dist
        self.nginx_ssl_dist = nginx_ssl_dist
        self.conn = self._get_connection()
        #self.run()

    def _get_connection(self):
        try:
            return create_connection(self.websocket)
        except socket.error as e:
            print "Connection failed: %r" % e
            sys.exit(1)

    def _get_local_address(self):
        return re.search('\d+\.\d+\.\d+\.\d+',
                         Popen('ifconfig', stdout=PIPE).stdout.read()).group(0)

#    def _run(self):
#        self.conn.send(self._get_local_address())
#        while True:
#            res_content = self.conn.recv()
#            if res_content:
#                res = eval(res_content)
#                self.write_pems(res['crts'])
#                self.update_cfg(res['cfg'])
#                self.reload_service()

    def run(self):
        data = json.dumps(dict(addr=self._get_local_address(),
                               nginx_switch=self.nginx_switch))
        self.conn.send(data)
        while True:
            res_content = self.conn.recv()
            if res_content:
                res = json.loads(res_content)
                if 'haproxy' in res.keys():
                    self.run_with_haproxy(res['haproxy'])
                if 'nginx' in res.keys():
                    self.run_with_nginx(res['nginx'])

    def run_with_haproxy(self, val):
        self.write_haproxy_pems(val['crts'])
        update_service_config(self.haproxy_cfg_dist, val['haproxy_cfg'])
        reload_service(self.haproxy_service_dist)

    def run_with_nginx(self, val):
        self.write_nginx_ssl_files(val['ssl_files'])
        update_service_config(self.nginx_conf_dist, val['nginx_conf'])
        reload_service(self.nginx_service_dist)

    def stop(self):
        self.conn.close()
        super(Process, self).stop()

    def write_haproxy_pems(self, pems):
        for pem in pems:
            file_name = "%s_%s.pem" % (pem['domain'], pem['port'])
            file_content = "\n".join(pem['certificate'].values())
            write("%s%s" % (self.haproxy_ssl_dist, file_name), file_content)

    def write_nginx_ssl_files(self, ssl_files):
        for ssl_file in ssl_files:
            ssl_certificate = ssl_file['certificate_chain']
            ssl_certificate_key = ssl_file['private_key']
            write("%s%s" % (self.nginx_ssl_dist,
                            "%s.chained.crt" % ssl_file['name']),
                  ssl_certificate)
            write("%s%s" % (self.nginx_ssl_dist,
                            "%s.key" % ssl_file['name']),
                  ssl_certificate_key)
