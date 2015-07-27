#!/usr/bin/python
#
# Client Workspace Checker
#
# Start easy : list all workspaces with name | age | # have entries | # open files
#
# This script resets the access date to now and therefore can only be used once !!!

from __future__ import print_function
import P4
from datetime import datetime

class ClientInfo:
    def __init__( self, name, age, have, opened):
        self.name = name
        self.age = age
        self.have = have
        self.opened = opened
        
    def __str__( self ):
        return "%s | %s days | %s have | %s opened" % ( self.name, self.age, self.have, self.opened )
    
class ClientChecker:
    def __init__( self ):
        self.p4 = P4.P4()
        self.p4.connect()
        self.clients = []
        
    def run( self ):
        for client in self.p4.run_clients():
            name = client['client']
            lastAccess = datetime.utcfromtimestamp( int(client['Access']) )
            age = datetime.now() - lastAccess
            have = self.getNumberHaveEntries( name )
            opened = self.getNumberOpened( name )
            
            self.clients.append( ClientInfo( name, age.days, have, opened ) )
            
    def getNumberHaveEntries( self, client ):
        try:
            sizes = self.p4.run_sizes( "-s", "//...@%s" % client)
            return int( sizes[0][ 'fileCount' ] )
        except P4.P4Exception as err:
            print(err)
            return 0
    
    def getNumberOpened( self, client ):
        opened = self.p4.run_opened( "-C", client )
        return len( opened )

    def report( self ):
        for info in self.clients:
            print(info)

if __name__ == "__main__":
    info = ClientChecker()
    info.run()
    info.report()
