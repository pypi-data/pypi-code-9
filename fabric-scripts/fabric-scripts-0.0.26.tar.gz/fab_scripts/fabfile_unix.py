# coding: utf-8
from __future__ import with_statement
from functools import wraps
import codecs
import json
import os
import platform
import re
import subprocess
import sys
import time

from fabric.api import *
from fabric.colors import *
from fabric.utils import abort
from fabric.contrib.console import confirm

from .fab_utils import *


@task
def nginx_install(install_dir='./opt', link_dir='.', version='1.8.0', headers_mod_version='0.25'):
    def download():
        local('wget http://nginx.org/download/nginx-%s.tar.gz' % version)
        local('tar -xvzf nginx-%s.tar.gz' % version)
        local('wget https://github.com/openresty/headers-more-nginx-module/archive/v%s.tar.gz' % headers_mod_version)
        local('tar -xvzf v%s.tar.gz' % headers_mod_version)

    def install(install_dir):
        # http://nginx.org/en/docs/configure.html
        nginx_modules = ' '.join([
            '--with-http_ssl_module',
            '--add-module=../headers-more-nginx-module-%s' % headers_mod_version,
            '--with-http_stub_status_module',
            '--with-http_gzip_static_module',
            '--with-http_gunzip_module',
            '--with-http_realip_module',
            '--with-http_secure_link_module',
            '--error-log-path=/tmp/nginx.log',
            # '--with-debug',
        ])
        install_dir = os.path.abspath(install_dir)
        local('rm -rf %s/' % install_dir)
        local('mkdir -p %s' % install_dir)
        with lcd('nginx-%s' % version):
            local('./configure --prefix=%s/nginx %s' % (install_dir, nginx_modules))
            local('make')
            local('make install')
        local('ln -sf %s/nginx/sbin/nginx %s' % (install_dir, link_dir))

    def clean():
        local('rm -rf nginx-%s*' % version)
        local('rm v%s.tar.gz*' % headers_mod_version)
        local('rm -rf headers-more-nginx-module-%s/' % headers_mod_version)
        local('rm -rf *_temp/')

    try:
        download()
        install(install_dir)
    finally:
        clean()

@task
def config_os():
    env.run('uname -a')
    env.run('ulimit -aH') # H = hard limit
    env.run('ulimit -n') # max number of open files
    # TIME_WAIT length in ms / default 15000
    env.run('sysctl net.inet.tcp.msl')
    # Update TIME_WAIT length
    env.run('sudo sysctl -w net.inet.tcp.msl=1000')
    # Number of ephemeral ports
    env.run('sysctl net.inet.ip.portrange.first net.inet.ip.portrange.last')
    # max sockets
    env.run('sysctl -a | grep somax')
    # max files
    env.run('sysctl -a | grep files')

@task
def update_config_os(config='default'):
    default = dict(time_wait_ms=15000, first_port_number=49152, max_sockets=128, max_open_files=12288, max_open_files_per_proc=10240)
    medium = dict(time_wait_ms=1000, first_port_number=32768, max_sockets=2048, max_open_files=24576, max_open_files_per_proc=20480)
    high = dict(time_wait_ms=300, first_port_number=10152, max_sockets=65536, max_open_files=65536, max_open_files_per_proc=65536)
    if config == 'medium':
        c = medium
    elif config == 'high':
        c = high
    else:
        c = default
    env.run('sudo sysctl -w net.inet.tcp.msl=%s' % c['time_wait_ms'])
    # Number of ephemeral ports = last (65536) - first
    env.run('sudo sysctl -w net.inet.ip.portrange.first=%s' % c['first_port_number'])
    env.run('sudo sysctl -w kern.ipc.somaxconn=%s' % c['max_sockets'])
    env.run('sudo sysctl -w kern.maxfiles=%s' % c['max_open_files'])
    env.run('sudo sysctl -w kern.maxfilesperproc=%s' % c['max_open_files_per_proc'])
    # Reuse TCP sockets
    # echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse
    # echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle
    env.run('sudo sh -c ulimit -HSn 200000')
    env.run('sudo ulimit -n %s' % c['max_open_files']) # max number of open file descriptors
