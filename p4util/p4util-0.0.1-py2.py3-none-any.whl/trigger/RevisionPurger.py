#!/usr/bin/python
# -*- coding: <utf-8> -*-
#
# RevisionPurger
#
#*******************************************************************************
# Copyright (c) 2009, Perforce Software Ltd.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1.  Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
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
#*******************************************************************************
# $Id: //guest/lester_cheung/p4util/p4util/trigger/RevisionPurger.py#2 $
#
# RevisionPurger 
# This script is to be used as a change-commit trigger
#
# It will check if a previous revision of a submitted file exists and purge
# the archive file for that previous revision from the depot, leaving an empty
# file behind. The script also adjusts the digest in the meta data to avoid errors
# during a verify.
#
# To enable the script to purge files, the DEBUG variable needs to be set to False. 
# With DEBUG enabled, the script will only send out a message stating the file it would purge.
#
# Other parameters to set:
# P4USER and P4PORT. The user needs to be a super user to access librarian information
#   If the user has a password, a long-lasting ticket should be used.
#
# REVISIONS_TO_KEEP: currently set to 1. This can be adjusted to keep more than one revision
# filterMap: define which files should be purged. The default here is //....pak. This should match
#   the file name argument in the change-commit trigger in the triggers table.
#
# REMOVED_COMMENT: the content of the purged file will be set to this. 
#   Set to "" to save the most space.
# arguments: %change%

from __future__ import print_function
import P4
import sys
import os, os.path, gzip
from datetime import datetime

# environment - set this before enabling the trigger
P4USER="sknop"
P4PORT="1666"

# tunable parameters
DEBUG=True # set to True to only print out the purge command
REVISIONS_TO_KEEP=1
REMOVED_COMMENT="Removed by trigger"

# add all filters for files you want to consider for purging
filterMap = P4.Map()
filterMap.insert("//....pak")
# add additional filters here for other file patterns

class P4Change:
    """Encapsulates a Perforce change. Basically a pretty wrapping around p4.run_describe()"""
    def __init__( self, desc ):
        self.change = desc[ "change" ]
        self.user = desc[ "user" ]
        self.client = desc[ "client" ]
        self.desc = desc[ "desc" ]
        self.time = datetime.utcfromtimestamp( int( desc[ "time" ] ) )
        self.status = desc[ "status" ]
        
        self.files = []
        if "depotFile" in desc:
            for n, d in enumerate( desc[ "depotFile" ] ):
                df = P4.DepotFile(d)
                dr = df.new_revision()
                dr.type = desc[ "type" ][ n ]
                dr.rev = desc[ "rev" ][ n ]
                dr.action = desc[ "action" ][ n ]
                self.files.append( df )
        
        
        self.jobs = {}
        if "job" in desc:
            for n, j in enumerate( desc[ "job" ] ):
                self.jobs[j] = desc[ "jobstat" ][ n ]


class RevisionPurger:
    def __init__( self, changeNo ):
        self.changeNo = changeNo
        self.p4 = P4.P4()
        self.p4.port = P4PORT
        self.p4.user = P4USER
        
    def process( self ):
        self.p4.connect()
        try:
            self.buildDepotMap()
            self.change = P4Change( self.p4.run_describe( self.changeNo )[0] )
            for f in self.change.files:
                r = f.revisions[0]
                
                if filterMap.includes(f.depotFile) and self.filePurgeable(f):
                    self.checkFile( f.depotFile + "#" + str(int(r.rev) - REVISIONS_TO_KEEP) )
        except Exception as e:
            print("RevisionPurger Exception : ", e)
        finally:
            self.p4.disconnect()
            
    
    def filePurgeable(self, f):
        r = f.revisions[0]
        rev = int(r.rev)
        type = r.type
        action = r.action
        
        if rev > REVISIONS_TO_KEEP:
            if "binary" in type and not "D" in type and not "S" in type:
                if action == "integrate" or action == "edit": # TODO: should we add delete here?
                    return True
        return False
    
    def buildDepotMap(self):
        """Creates the depot map for easy translation from depotFile to librarianFile"""
        serverRoot = self.p4.run_info()[0]["serverRoot"]
        self.depotMap = P4.Map()
        for depot in self.p4.run_depots():
            if depot["type"] != "remote":
                map = depot["map"]
                if map[0:-4].find("/") == -1:
                    map = os.path.normpath(serverRoot + "/" + map)
                self.depotMap.insert("//%s/..." % depot["name"], map)

    def checkFile( self, f ):
        """Checks if this file can be purged. It must not be a lazy copy \
           and cannot have lazy copies itself without successor"""
        
        fstats = self.p4.run_fstat( '-Ocz', f )[0]
        
        if fstats['lbrFile'] == fstats['depotFile']:
            # "Its the source"
            if 'lazyCopyFile' in fstats:
                # "... but there are lazy copies:"
                # need to check every lazy copy. If only one has no next revision, bail!
                for (lf, lr) in zip(fstats["lazyCopyFile"], fstats["lazyCopyRev"]):
                    if not self.successorExists(lf+lr):
                        # "No successors exist for at least one file"
                        return False # did not delete the file
                    # all lazy copies have successor - delete the file
            if self.successorExists(f): # make sure the parent has a successor, thanks Tony
                self.deleteDepotFile(fstats)
                return True
            return False
        else:
            # "Its a lazy copy, need to find parent"
            return self.checkFile(self.checkParent(f))
            
    def fileRev( self, f ):
        return f.depotFile + "#" + f.revisions[0].rev

    def successorExists(self, f):
        successors = self.p4.run_files("-a", f + ",#head")
        if len(successors) > REVISIONS_TO_KEEP: 
            return True
        return False
    
    def checkParent(self, f):
        df = self.p4.run_filelog(f)[0]
        for r in df.revisions:
            if r.action == "integrate":
                for i in r.integrations:
                    if i.how == "copy from":
                        return "%s#%d" % (i.file, i.erev)
            elif r.action == "branch":
                for i in r.integrations:
                    if i.how == "branch from":
                        return "%s#%d" % (i.file, i.erev)
        raise Exception("Cannot find the source of the integration - obliterate?")
    
    def deleteDepotFile(self, fstats):
#        print("RevisionPurgeremover: Deleting %s %s type %s" % (fstats['lbrFile'], fstats['lbrRev'], fstats['lbrType']))

        compressed = self.lbrTypeCompressed( fstats["lbrType"] )
        fileName = self.getFileName( fstats["lbrRev"], compressed )
        libFile = self.getLibrarianFile( fstats["lbrFile"],  fileName)

        if DEBUG:
            print("Would delete", libFile)
        else:
            os.unlink(libFile)
            
            if compressed:
                f = gzip.GzipFile(libFile, "wb")
            else:
                f = open(libFile, "wb")
    
            f.write(REMOVED_COMMENT)
            f.close()
                            
            rev = fstats['depotFile'] + "#" + fstats['headRev'] + "," + fstats['headRev']
            self.p4.run_verify("-v", rev)
        
    def getFileName( self, lbrFile, compressed ):
        result = lbrFile
        if compressed:
            result += ".gz"
        return result
        
    def getLibrarianFile( self, lbrFile, fileName):
        path = self.getLibrarianDirectory( lbrFile )
        
        afile = path + os.sep + fileName
        if not os.path.isfile( afile ):
            raise Exception("Cannot find file %s" % afile )
        
        return afile
        
    def lbrTypeCompressed( self, lbrType ):
        if (lbrType == "ubinary") or (lbrType == "uxbinary") or ("F" in lbrType):
            return False
        return True

    def getLibrarianDirectory( self, lbrFile):
        path = self.depotMap.translate(lbrFile)
        
        if path:
            path += ",d"
            path = os.path.normpath(path)
            
            if not os.path.isdir(path):
                raise Exception("Cannot find directory %s for lbrFile %s" % (path, lbrFile))
            return path
        else:
            raise Exception("Cannot translate %s into directory" % lbrFile)

if __name__ == "__main__":
    if len( sys.argv ) < 1:
        sys.stderr.write("Not enough arguments\n")
        sys.exit(1)
    
    remove = RevisionPurger( sys.argv[1])
    remove.process()
