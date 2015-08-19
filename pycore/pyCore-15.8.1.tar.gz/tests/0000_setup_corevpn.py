"""
Copyright (c) 2014 Maciej Nabozny

This file is part of OverCluster project.

OverCluster is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess
import settings
import urllib2
import os
from testutils import ssh_call


def setup_module(module):
    global core_address
    core_address = urllib2.urlparse.urlparse(settings.address).hostname


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_install_coretalk():
    global core_address
    ssh_call(core_address, 'root', 'apt-get install --yes --force-yes corevpn')


def test_enable_extension():
    global core_address
    ssh_call(core_address, 'root', "sed -i 's/LOAD_API = \[/LOAD_API = \[\"vpn\", /g' /etc/cloudOver/overClusterConf/config.py")
    ssh_call(core_address, 'root', "sed -i 's/LOAD_CI_API = \[/LOAD_CI_API = \[\"ciVpn\", /g' /etc/cloudOver/overClusterConf/config.py")
    ssh_call(core_address, 'root', "sed -i 's/LOAD_MODELS = \[/LOAD_MODELS = \[\"vpn\", /g' /etc/cloudOver/overClusterConf/config.py")


def test_migate_db():
    global core_address
    ssh_call(core_address, 'root', 'overCluster_admin makemigrations')
    ssh_call(core_address, 'root', 'overCluster_admin migrate')


def test_restart_services():
    ssh_call(core_address, 'root', 'service apache2 restart')
    ssh_call(core_address, 'root', 'service overcluster-core restart')
