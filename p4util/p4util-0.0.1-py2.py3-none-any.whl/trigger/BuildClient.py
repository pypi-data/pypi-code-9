#!/usr/bin/env python

# This trigger is supposed to be used as a form-commit trigger for clients
# It will check that the client is a build client with the ServerID set

from __future__ import print_function
import P4
import sys
import logging.config
import os

LOGFILE = "build_client_logger.cfg"

def transfer_view( user, port, client):
    p4_build = P4.P4()
    p4_build.user = user
    p4_build.port = port
    p4_build.client = client["Client"] # need to set client, or saving the client fails
    p4_build.connect()
    
    p4_build.save_client(client)
    
    p4_build.disconnect()
    
def replicate_to_build( user, port, form_file ):
    p4_master = P4.P4()
    p4_master.user = user
    p4_master.port = port
    p4_master.connect()
    
    with open(form_file) as f:
        content = f.read()
    
    client = p4_master.parse_client(content)
    if 'ServerID' in client:
        serverid = client._serverid
        logging.debug("Called for client {} with ServerID".format(client["Client"], serverid))
        
        for s in p4_master.run_servers():
            if s["ServerID"] == serverid:
                build_port = s['Address']
                transfer_view(user, build_port, client)
                return
        logging.error("Found serverID in client but no matching server spec!")
    
    p4_master.disconnect()
    return
    
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage user port form-file", file=sys.stderr)
        sys.exit(1)
    
    user = sys.argv[1]
    port = sys.argv[2]
    form_file = sys.argv[3]
        
    if os.path.isfile(LOGFILE):
        logging.config.fileConfig(LOGFILE)
    
    replicate_to_build(user, port, form_file)
    