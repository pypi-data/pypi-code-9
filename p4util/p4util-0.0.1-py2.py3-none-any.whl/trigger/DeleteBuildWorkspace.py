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
#         notice, this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer in the
#         documentation and/or other materials provided with the
#         distribution.
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
# Maintainer: Sven Erik Knop, sknop@perforce.com
#

from __future__ import print_function
import sys
import P4

def check_client(formfile, formname, kargs):
    p4 = P4.P4(**kargs)
    with p4.connect():
    
        with open(formfile) as f:
            content = f.read()
        
        newclient = p4.parse_client(content)
        
        if p4.run_clients("-e", formname):
            client = p4.fetch_client(formname)
            
            if "ServerID" in client:
                # check if the server id of the new client matches
                # if not, or if the server id is missing, delete the build client first
                if ("ServerID" in newclient and client["ServerID"] != newclient["ServerID"]) or \
                    not "ServerID" in newclient:
                    p4.delete_client(formname)
        
            else:
                if ("ServerID" in newclient) and not "ServerID" in client:
                    print( "\n\nTrying to switch a client workspace to a build workspace.\n" \
                           "Please delete original workspace on master first.\n" )
                return 1
        
    return 0

if __name__ == "__main__":
    kargs = {}
    args = []
    
    for arg in sys.argv[1:]:
        if "=" in arg:
            (key,val) = arg.split("=")
            kargs[key] = val
        else:
            args.append( arg )
    
    if len(args) < 2:
        print("Usage: formfile formname [kargs]")
        sys.exit(0)
    
    formfile = args[0]
    formname = args[1]
    
    retVal = check_client(formfile, formname, kargs)

    sys.exit(retVal)