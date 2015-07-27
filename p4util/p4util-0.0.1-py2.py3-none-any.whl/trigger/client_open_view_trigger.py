#!/usr/bin/env python
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


from __future__ import print_function

import P4
import sys, re

def check_client(formfile):
    with open(formfile) as f:
        content = f.read()

    p4 = P4.P4()
    # no need to connect, we are only parsing the form

    client = p4.parse_client(content)

    pattern = re.compile("//[^/]+/\.\.\.\s")

    for v in client._view:
        if pattern.match(v):
            print("Open view '{}' is not allowed. Please change client view".format(v))
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %formfile%", file=sys.stderr)
        sys.exit(1)

    check_client(sys.argv[1])

