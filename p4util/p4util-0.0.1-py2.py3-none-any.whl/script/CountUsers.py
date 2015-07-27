#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Sven Erik Knop, Perforce Software Ltd
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1.  Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PERFORCE
# SOFTWARE, INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# User contributed content on the Perforce Public Depot is not supported by Perforce,
# although it may be supported by its author. This applies to all contributions
# even those submitted by Perforce employees.
#
# CountUsers.py
#
# This python script will count unique users in a range of Perforce Servers
# The script takes a config file that contains the list of servers, and the user name and password 
# to connect. The user can (and should) be a non-privileged user 
# 
# The configuration file is a CSV file with the fields P4PORT,P4USER,P4PASSWD
# Lines starting with # are ignored as comments

from __future__ import print_function
import argparse
import sys
import P4
import re

CONFIG = "countUsers.cfg"

class P4Server:
    def __init__(self, port, user, password):
        self.p4 = P4.P4()
        self.p4.port = port
        self.p4.user = user
        self.p4.password = password
        
        self.p4.connect()
        self.p4.run_login()
        
    def get_users(self):
        users = self.p4.run_users()
        names = [ u['User'] for u in users ]
        
        return names
    
class CountUsers:
    def __init__(self, config, verbose):
        self.config = config
        self.verbose = verbose
    
        self.get_servers()
        
    def get_servers(self):
        with open(self.config) as f:
            content = f.read()
            
        splitContent = content.split('\n')
        servers = [ re.split(',\W*', x) for x in splitContent if x and x[0] != '#' ]
        
        self.servers = []
        for s in servers:
            server = P4Server(s[0], s[1], s[2])
            self.servers.append( server)
        
    def count(self):
        
        allUsers = set()
        for server in self.servers:
            users = server.get_users()
            for u in users:
                allUsers.add(u)
        
        return len(allUsers), sorted(allUsers)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="CountUsers",
        epilog="Copyright (C) 2013 Sven Erik Knop, Perforce Software Ltd"
    )
    
    parser.add_argument('-c', '--config', default=CONFIG, help="Default is " + CONFIG)
    parser.add_argument('-v', '--verbose', action='store_true', help="Provide output on stdout")

    options = parser.parse_args()
    
    countUsers = CountUsers(options.config, options.verbose)
    
    total, userList = countUsers.count()
    
    print("Total = {}".format(total))
    if options.verbose:
        print("Unique Users = {}".format(userList))
 