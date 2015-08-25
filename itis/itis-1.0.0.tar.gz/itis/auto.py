#!/usr/bin/env python
#!/bin/bash
# -*- coding: UTF-8 -*

import os, sys, stat
import requests
import urllib
from colorama import Fore, Back, Style


def main():
	if len(sys.argv)== 1:
		print "Invalid domain"
	else:
		try: 
			urllib.urlopen('http://' + sys.argv[1] ) 
			print(Fore.GREEN + u"\u2713" +" Up")
		except:
			print(Fore.RED + u"\u2718" +" Down")


