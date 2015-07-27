#!/usr/bin/python
#
# Trigger script to prevent changing file types to +S
#
# ChangeTypeTrigger.py
#
#
# Copyright Sven Erik Knop (c) 2009 Perforce Software, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1.  Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL PERFORCE SOFTWARE, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# $Id$
# 
# 

from __future__ import print_function

import sys
import P4
from P4Triggers import P4Trigger

class ChangeTypeTrigger(P4Trigger):

    def __init__( self, **kargs):
        kargs['charset'] = 'none'
        kargs['api_level'] = 62
        P4Trigger.__init__(self, **kargs)
      
      # need to reset the args in case a p4config file overwrote them
        for (k,v) in kargs.iteritems():
            setattr( self.p4, k, v)
    
    USER_MESSAGE = """
        
    Your submission has been rejected because the following file
    changed its file type to +S
    
    file = %s 
    type = %s
    """
    
    def setUp( self ):
        info = self.p4.run_info()[0]
        if "unicode" in info and info["unicode"] == "enabled":
            self.p4.charset = "utf8"
        self.p4.exception_level = 1 # ignore WARNINGS like "no such file"
        self.p4.prog = "ChangeTypeTrigger"
 
    def validate( self ):
        for file in self.change.files:
            rev = file.revisions[0]
            if not (rev.action == "edit"): 
                continue
	
            if 'S' in rev.type:
                self.message( self.USER_MESSAGE % ( file.depotFile, rev.type) )
                return False
        return True

# main routine.
# If called from the command line, go in here

if __name__ == "__main__":
    kargs = {}
    try:
        for arg in sys.argv[2:]:
            (key,value) = arg.split("=")
            kargs[key] = value
    except:
        print("Error, expecting arguments in form key=value. Bailing out ...")
        sys.exit(0)
        
    ct = ChangeTypeTrigger( **kargs )
    sys.exit( ct.parseChange( sys.argv[1] ) )
