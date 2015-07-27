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

import sqlite3
import P4
import argparse
from pprint import pprint

DATABASE_NAME = "hash.db"

class CreateHashDatabase:
    def __init__(self, name, path):
        self.path = path
        self.conn = sqlite3.connect(name)
        self.conn.execute("Create Table IF NOT EXISTS digest(hash TEXT PRIMARY KEY, filesize INTEGER, depotfile TEXT, revision INTEGER)")

        self.p4 = P4.P4()
        self.p4.prog = "CreateHashDatabase"
        self.p4.connect()

        self.insert_hashes()

        self.p4.disconnect()
        self.conn.close()

    def insert_hashes(self):
        class Handler(P4.OutputHandler):
            def __init__(self, conn):
                self.conn = conn

            def outputStat(self, stat):
                depotFile = stat['depotFile']
                values = []

                for (n, rev) in enumerate(stat['rev']):
                    digest = stat['digest'][n]
                    fileSize = stat['fileSize'][n]
                    # check if this revision is a lazy copy 
                    if 'how' in stat:
                        for how in stat['how']:
                            if how in ("branch from", "copy from"):
                                continue 
                    values.append( (digest, fileSize, depotFile, rev) )

                try:
                    with self.conn:
                        self.conn.executemany("INSERT INTO digest VALUES (?, ?, ?, ?)", values )
                except sqlite3.IntegrityError:
                    print("Duplicate HASH key for ", depotFile)

#                        cursor = self.conn.cursor()
#                        cursor.execute("SELECT depotfile, revision FROM digest WHERE hash = ?", (digest, ))
#                        result = cursor.fetchone()
#                        if result:
#                            print("Previously stored : {file}#{rev}".format(file=result[0], rev=result[1]))

                return P4.OutputHandler.HANDLED

        self.p4.run_filelog(self.path, handler=Handler(self.conn))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Hash checker")
    parser.add_argument("-d", "--database", default=DATABASE_NAME)
    parser.add_argument("-p", "--path", required=True)

    args = parser.parse_args()

    prog = CreateHashDatabase(args.database, args.path)

