#!/usr/bin/python
#
# 

"""A P4Python script that splits the verify process over the root directories of each depot

$Id: //depot/python/SplitVerify.py#1 $

#*******************************************************************************
# Copyright (c) 2009, Perforce Software, Inc.  All rights reserved.
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

"""

from __future__ import with_statement

import P4
import sys

p4 = P4.P4()
p4.prog = "SplitVerify.py"
p4.api_level = 63

# assumes that the P4 enviroment is set correctly via environment variables or P4CONFIG
# otherwise, set the P4 environment here
# p4.port = "server:1666"
# p4.user = "super user"

def main( file ):
	try:
		p4.connect()

		dirs = p4.run_dirs("//*/*")
		result = []
		for d in dirs:
			pattern = d['dir'] + "/..."
			print("Verifying %s" % pattern)
			result += ( p4.run_verify("-q",  pattern))
		
		if len(result) > 0:
			file.write("Verify reported errors:\n")
			for r in result:
				file.write(r+"\n")

		p4.disconnect()
		
	except P4Exception as err:
		file.write(err+"\n")

if __name__ == "__main__":
	if len( sys.argv ) > 1:
		with open(sys.argv[1], "w") as filename:
			main(filename)
	else:
		main(sys.stdout)


