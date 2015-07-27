#!/usr/bin/env python3

'''
Just a simple example to show how you can convert a Perforce Audit LOG to a SQLite database.

$Id: //guest/lester_cheung/p4util/p4util/adm/audit2db.py#1 $
$Author: lester_cheung $

'''
import sqlite3
import sys

if len(sys.argv) != 3:
    print('''Usage: {} <AUDIT_LOG> <SQLiteDB>''')
    sys.exit(0)
    
db = sqlite3.connect(sys.argv[2])
db.execute('''CREATE TABLE audit (date,time,user,client,ip,cmd,dpath,rev)''')
with open(sys.argv[1]) as fd:
    for line in fd:
        da, ti, user_client,  ip, cmd, dpath_with_rev = line.split(' ', 5)
        user, client = user_client.split('@')
        dpath_chunks = dpath_with_rev.split('#')
        dpath = '#'.join(dpath_chunks[:-1])
        rev = dpath_chunks[-1]
        db.execute('INSERT INTO AUDIT (date,time,user,client,ip,cmd,dpath,rev) VALUES (?,?,?,?,?,?,?,?)',
                   (da, ti, user, client, ip, cmd, dpath, rev))
db.commit()
