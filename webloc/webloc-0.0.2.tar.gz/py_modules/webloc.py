#!/usr/bin/env python
import os
from plistlib import *
# me
from public import *

@public
def get_webloc(path):
    plist = readPlist(path)
    return plist.URL # UPPERCASE

@public
def set_webloc(path,url):
    rootObject = dict(URL=str(url)) # UPPERCASE
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    writePlist(rootObject,path)

if __name__=="__main__":
	import os
	path=__file__+".plist"
	url="http://www.google.com"
	set_webloc(path,url)
	print(get_webloc(path))
	os.unlink(path)


