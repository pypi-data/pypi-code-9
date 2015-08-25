#!/usr/bin/env python
# -*- coding: UTF-8 -*

import urllib

class colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'

def main():
	try: 
		urllib.urlopen('https://google.com') 
		print colors.OKGREEN + u"\u2713" + " Online"
	except:
		print colors.FAIL + u"\u2718" + " Offline" 



