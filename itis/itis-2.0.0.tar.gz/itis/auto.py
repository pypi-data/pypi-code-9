#!/usr/bin/env python
#!/bin/bash
# -*- coding: UTF-8 -*

import os, sys, stat
import urllib

class colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'

def main():
	if len(sys.argv)== 1:
		print "Invalid domain"
	else:
		try: 
			urllib.urlopen('http://' + sys.argv[1] ) 
			print colors.OKGREEN + u"\u2713" + " Up"
		except:
			print colors.FAIL + u"\u2718" + " Down" 
