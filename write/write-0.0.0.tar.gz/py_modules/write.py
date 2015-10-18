#!/usr/bin/env python
from datetime import *
from json import *
import os
# me
from isstring import *
from public import *

@public
def write(path,content):
    """write to file and return fullpath"""
    if content is None: content=""
    if isinstance(content,dict):
        content = dumps(content)
    if not isstring(content):
        content = str(content)
    if str(content.__class__)=="<class 'bytes'>":
        try:
            content = str(content,"utf-8") # python3
        except TypeError: # TypeError: str() takes at most 1 argument (2 given)
            content = str(content) # python2
    #if encoding:
        #content=content.encode(encoding)
    dir = os.path.dirname(path)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    try:
        unicode()
        open(path,"w").write(content.encode("utf-8"))
    except:
        open(path,"w").write(content)
    return path

if __name__=="__main__":
    path=__file__+".tmp"
    write(path,"string")
    write(path,b"bytes")
    write(path,1488)
    write(path,dict())
    write(path,None)
    os.unlink(path)

