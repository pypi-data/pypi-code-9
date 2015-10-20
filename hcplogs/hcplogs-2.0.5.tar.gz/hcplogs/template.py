# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

__t = ['[target hcp72]',
       'fqdn = admin.hcp72.archivas.com',
       'user = logmon',
       'password = logmon01',
       'folder = hcp72',
       'last collected =',
       '',
       '[target hcp73]',
       'fqdn = admin.hcp73.archivas.com',
       'user = logmon',
       'password = logmon01',
       'folder = hcp73',
       'last collected = ',
       '',
       '[access logs]',
       'access = yes',
       'admin = yes',
       'mapi = yes',
       '# do not transfer empty logfiles',
       'omit empty = yes',
       '',
       '[local archive store]',
       'enable = yes',
       '# path should to be an absolute path',
       'path = /tmp/hcplogs',
       '',
       '[compliant archive store]',
       'enable = yes',
       '# path needs to be a full qualified Namespace and folder',
       'path = https://n1.m.hcp72.archivas.com/rest/accesslogs',
       '# a user having write permission to the namespace',
       'user = n',
       'password = n01',
       '# retention needs to be a valid HCP retention string',
       'retention = 0',
       '',
       '[logging]',
       'log to stdout = yes',
       'log to file = yes',
       'logfile = /tmp/hcplogs/_hcplogs.log',
       'rotateMB = 10',
       'backups = 9',
       'status query = 10',
       'debug = no',
       '',
       '[temporary store]',
       '# used for download/de-compression and handling the logs',
       '# will be cleaned up when the tool has finished its work',
       'tempdir = .',
       ]

template = '\n'.join(__t)
