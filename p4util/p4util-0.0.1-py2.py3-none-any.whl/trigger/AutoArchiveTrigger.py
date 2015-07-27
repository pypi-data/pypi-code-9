#!/usr/bin/env python3
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
# Only files of type binary and only those with extensions in ARCHIVE_EXTENSIONS will be archived

from __future__ import print_function
 
import P4
from P4Triggers import P4Trigger
import sys
import os.path

ARCHIVE_EXTENSIONS = [ ".fbx", ".mov", ".pdf" ]

class AutoArchiveTrigger(P4Trigger):

    def __init__( self, archive, kept, **kargs):
        kargs['charset'] = 'none'
        P4Trigger.__init__(self, **kargs)
      
        # need to reset the args in case a p4config file overwrote them
        for (k,v) in kargs.items():
            setattr( self.p4, k, v)
        
        self.archive = archive
        self.kept = kept
        
    def setUp( self ):
        info = self.p4.run_info()[0]
        if "unicode" in info and info["unicode"] == "enabled":
            self.p4.charset = "utf8"
        self.p4.exception_level = 1 # ignore WARNINGS like "no such file"
        self.p4.prog = "AutoArchiveTrigger"
 
    def validate( self ):
        names = []
        for changed_file in self.change.files:
            rev = changed_file.revisions[0]
            if not ("binary" in rev.type): 
                continue
            
            (name, ext) = os.path.splitext(rev.depotFile)
            if not ext.lower() in ARCHIVE_EXTENSIONS:
                continue 
    
            names.append(changed_file.depotFile)

        to_be_archived = []
        filelogs = self.p4.run_filelog(names)
        for candidate in filelogs:
            if len(candidate.revisions) > self.kept:
                to_be_archived.append("{}#{}".format(candidate.depotFile, candidate.revisions[self.kept].rev ))
        
        if to_be_archived:
            self.p4.run_archive("-hD", self.archive, to_be_archived)
        
        return True

# main routine.
# If called from the command line, go in here

if __name__ == "__main__":
    archive = None
    kept = None
    kargs = {}
    try:
      for arg in sys.argv[2:]:
        (key,value) = arg.split("=")
        if key == "archive":
            archive = value
        elif key == "kept":
            kept = int(value)
            if kept < 1:
                print("Need to keep at least one revision, got kept={}. Bailing out ...".format(kept))
                sys.exit(0)
        else:
            kargs[key] = value
    except:
        print("Error, expecting arguments in form key=value. Bailing out ...")
        sys.exit(0)
        
    if not archive or not kept:
        print("Required arguments archive= or kept= missing")
        sys.exit(0)
    
    ct = AutoArchiveTrigger( archive, kept, **kargs )
    sys.exit( ct.parseChange( sys.argv[1] ) )