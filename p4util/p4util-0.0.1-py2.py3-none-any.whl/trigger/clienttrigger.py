#!/usr/bin/python
#
# clienttrigger.py
#
# Copyright (c) 2008, Perforce Software, Inc.  All rights reserved.
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
# $Id: //guest/lester_cheung/p4util/p4util/trigger/clienttrigger.py#1 $
# 
# This trigger updates a new client spec with some defaults.
# It is meant as a template to create your own client default triggers.
# 
# This script requires P4Python 2007.3 or later from the Perforce website.
# 
# Called with formname, formfile and serverport and user
# Link this up as a trigger with a trigger line like this:
#
# default-client form-out client "/home/triggers/clienttrigger.py %formname% %formfile% %serverport% %user%

import P4
import sys

clientname = sys.argv[1]
clientfilename = sys.argv[2]
serverport = sys.argv[3]
user = sys.argv[4]

p4 = P4.P4()
p4.port = serverport
p4.user = user
p4.client = clientname
p4.connect()

# verify that the client does not exists already

info = p4.run_info()[0]


if info['clientName'] != "*unknown*":
  sys.exit(0)

# read the formfile

with open( clientfilename, "r" ) as f:
	clientAsString = f.read()

# parse the formfile

client = p4.parse_client(clientAsString)

# change the client content

client['Options'] = client['Options'].replace('normdir', 'rmdir')

# create the string again
# and modify the formfile

clientAsString = p4.format_client(client)

with open ( clientfilename, "w" ) as f:
	f.write(clientAsString)

# and exit successfully

p4.disconnect()
sys.exit(0)