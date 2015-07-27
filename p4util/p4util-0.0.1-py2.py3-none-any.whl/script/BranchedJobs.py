#! python
# Copyright (C) 2011 Sven Erik Knop, Perforce Software. All rights reserved.
# This is a demonstration script, not production quality.
# There is no warranty implied or given.

import sys
import P4

def findJobsBetween(branch1, branch2):
	p4 = P4.P4()
	p4.connect() # implies environment is set correctly outside the script

	changes1 = [ x['change'] for x in p4.run_changes('-i', branch1) ]
	changes2 = [ x['change'] for x in p4.run_changes('-i', branch2) ]

	diff = [ x for x in changes2 if x not in changes1 ]
	
	jobs = []
	for c in diff:
		fixes = p4.run_fixes('-c', c)
		for f in fixes:
			jobs.append( f['Job'] )

	for j in jobs:
		print(j)

	p4.disconnect()
 
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("Usage: python pca.py path1 path2")
		sys.exit(1)
	
	findJobsBetween(sys.argv[1], sys.argv[2])
	
