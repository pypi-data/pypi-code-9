#!/usr/bin/env python 
#
# Copyright (c) 2010, Sven Erik Knop, Perforce Software. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1.  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
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

# User contributed content on the Perforce Public Depot is not supported by Perforce,
# although it may be supported by its author. This applies to all contributions 
# even those submitted by Perforce employees.
#
# For any questions or problems please contact me at sknop@perforce.com 
# 
# python script to emulate a potential 'p4 zip'
#
# Usage: python p4zip.py [options] archive file[revRange] ...
#   options: 
#           -p [--port] P4PORT
#           -c [--client] P4CLIENT, used as the view template


import P4
import zipfile
from optparse import OptionParser

class PrintZip:
    def __init__( self, options, filename ):
        self.options = options
        self.filename = filename
        self.p4 = P4.P4()
    
    def process(self, args):
        self.zipfile = zipfile.ZipFile(self.filename, 'w', zipfile.ZIP_DEFLATED, True)
        try:
            if self.options.port: self.p4.port = self.options.port
            if self.options.client: self.p4.client = self.options.client
            if self.options.manifest: self.manifest = ""
            
            self.p4.connect()
            self.setupMap()
            
            for arg in args:
                print( "processing %s" % arg )
            result = self.p4.run_print(arg)
            while len(result) > 0:
                # bit of Python black magic to shift the first two elements out
                (dname, content), result[:2] = result[:2], []
                fname = self.map.translate(dname['depotFile'])
                if self.options.manifest:
                    manifestEntry = dname['depotFile'] + '#' + dname['rev']
                    self.manifest += manifestEntry + '\n'
            
                self.zipfile.writestr(fname, content)
        except P4.P4Exception as e:
            print( e )
        except Exception as e:
            print( "Something failed: " + str(e))
            raise
        finally:
            self.p4.disconnect()
            if self.options.manifest:
                self.zipfile.writestr("Manifest", self.manifest)
            self.zipfile.close()
    
    def setupMap(self):
        cl = self.p4.fetch_client()
        m1 = P4.Map(cl._view)
        m2 = P4.Map("//" + cl._client + "/... ...")
        self.map = P4.Map.join(m1, m2)
    
if __name__ == "__main__":
    usage = "usage: %prog [options] archive file[revRange] ..."
    version = "1.1"
    
    parser = OptionParser(usage, version=version)
    parser.add_option("-p", "--port", dest="port", help="P4PORT")
    parser.add_option("-c", "--client", dest="client", help="P4CLIENT")
    parser.add_option("-m", "--manifest", action="store_true", dest="manifest", help="Add manifest file")
    (options, args) = parser.parse_args()
    if( len(args) < 2 ):
        parser.error("incorrect number of arguments")
    
    p = PrintZip(options, args[0])
    p.process(args[1:])
    