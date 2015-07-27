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

import P4
import sys
import argparse

class Context:
    def __init__(self, revisions, summary):
        self.revisions = revisions
        self.summary = summary
        
        self.p4 = P4.P4()
        self.p4.prog = "Directory Sizes"
        self.p4.connect()

        self.width = 0
    
    def update_width(self, new_width):
        self.width = max(self.width, new_width)
    
class Directory:
    def __init__(self, context, path, totalDepth, myDepth = 0):
        self.context = context
        self.path = path
        self.totalDepth = totalDepth
        self.myDepth = myDepth

        self.path_indent = "{indent}{path}".format(indent = " ... " * self.myDepth, path = self.path)
        self.context.update_width(len(self.path_indent))
        
        self.dirs = []
        if totalDepth > 0:
            self.dirs = self.find_directories()
        
        self.size = 0
        if self.dirs:
            self.size = self.run_sizes("*")
            for subdir in self.dirs:
                self.size += subdir.size
        else:
            self.size = self.run_sizes("...")
             
    def find_directories(self):
        dirs = []
        for d in self.context.p4.run_dirs(self.path + "/*"):
            dirs.append( Directory(self.context, d['dir'], self.totalDepth - 1, self.myDepth + 1) )

        return dirs

    def run_sizes(self, wildcard):
        cmd = "{dir}/{wild}{range}".format(dir=self.path, wild=wildcard, range=self.context.revisions)
        return int(self.context.p4.run_sizes('-a', self.context.summary, cmd)[0]['fileSize'])
        
    def human(self):
        units = [" B", " KB", " MB", " GB", " TB"]
        factor = 1024
        current = self.size
        for u in units:
            if current < factor:
                return str(current) + u
            else:
                current = round(current / factor, 2)
        return str(current) + " PB"

    def print_size(self):
        print("{p:{width}} : {size:16} ({human})".\
              format(p = self.path_indent, width = self.context.width, size = self.size, human = self.human() ) )
        for d in self.dirs:
            d.print_size()
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory sizes")
    parser.add_argument("-d","--depth", default=1, type=int)
    parser.add_argument("-p","--path", required=True, help="Provide path without wildcard, for example //depot")
    parser.add_argument("-r","--range", default="", help="Perforce style revision range, start with @ or #")
    parser.add_argument("-z","--omit-lazy", action='store_const', default="-s", const="-z", help="Omit lazy copies")
    
    args = parser.parse_args()

    start_dir = args.path
    if args.path.endswith("/"):
        start_dir = args.path[:-1]
    
    root = Directory(Context(args.range, args.omit_lazy), start_dir, args.depth)
    root.print_size()
