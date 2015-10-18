#!/usr/bin/env python
__all__=["isstdin"]
from os import *
import sys
from sys import *
from public import *

isstdin = fstat(sys.stdin.fileno()).st_size > 0 # True if stdin

@public
def stdin(linebreak=True):
	if isstdin:
		stdindata = sys.stdin.read()
		if not linebreak:
			stdindata = stdindata.rstrip("\n")
		return stdindata

if __name__=="__main__":
	print(isstdin) # False
	print(stdin())
