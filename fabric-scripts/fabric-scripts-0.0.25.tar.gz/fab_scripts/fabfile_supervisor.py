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
def logs(bytes=20):
    logs = ['/tmp/supervisord.log', '/tmp/nginx.log', '/tmp/app_server.log']
    for log in logs:
        with settings(warn_only=True):
            env.run('tail -%s %s' % (bytes, log))

@task
def start_all(config_file=None):
    if config_file:
        env.run('supervisord -c %s' % config_file)
    else:
        if os.path.exists('./supervisord.conf'):
            env.run('supervisord')
        else:
            d = os.path.dirname(__file__)
            config_file = os.path.join(d, 'supervisord.conf')
            env.run('supervisord -c %s' % config_file)

@task
def status(toolset=None):
    r = env.run('supervisorctl status', capture=True)
    bad_statuses = ['STOPPED', 'STARTING', 'BACKOFF', 'STOPPING']
    for status in bad_statuses:
        if status in r:
            print(red(r))
            break
    critical_statuses = ['EXITED', 'FATAL', 'UNKNOWN']
    for status in bad_statuses:
        if status in r:
            print(red(r))
            abort('Process problems')

@task
def stop_all(folder=None, ports=[]):
    print(yellow('Stopping %s' % folder))
    directory = folder if folder else os.getcwd()
    with env.cd(directory):
        env.run('supervisorctl stop all')
        env.run('supervisorctl shutdown')
    def is_any_port_occupied(ports):
        with quiet():
            for port in ports:
                occupied = env.run('lsof -i:%s' % port, capture=True)
                if occupied:
                    return occupied
            return False
    ports = ports or [env.port, env.port + 1]
    wait_for(20, 0.5, is_any_port_occupied, ports)
