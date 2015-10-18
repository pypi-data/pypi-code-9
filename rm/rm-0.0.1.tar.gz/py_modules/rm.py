#!/usr/bin/env python
from os import *
from os.path import *
import shutil
# me
from fullpath import *
from public import *

@public
def rm(path):
    """os.unlink and shutil.rmtree replacement"""
    if not path: return
    if isinstance(path,list):
        map(rm,path)
        return
    path = fullpath(path)
    if not exists(path): return
    if isfile(path) or islink(path):
        unlink(path)
        return
    if isdir(path):
        shutil.rmtree(path)


if __name__=="__main__":
    import tempfile
    file=tempfile.mkstemp()[1]
    rm(file) # file
    dir=tempfile.mkdtemp()
    rm(dir) # dir
    from touch import *
    touch("~/testtest")
    rm("~/testtest") # fullpath

    rm(None) # nothing
    rm("not-existing") # nothing

