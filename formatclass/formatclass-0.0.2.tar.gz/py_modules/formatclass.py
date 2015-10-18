#!/usr/bin/env python
try:
    import __builtin__  as __builtins__ # python 2
except:
    import builtins as __builtins__ # python 3
from inspect import *
#from cyfunction import *
from formatfunction import *
from formatvalue import *
from objectname import *
from public import *
from issharedobject import *

def issystem(cls):
    return hasattr(__builtins__,cls.__name__)

def defargs(object):
    #argspec = getargspec(object)
    argspec = getargspec(object)
    return argspec.args

def formatbases(cls,fullname=True):
    __bases__ = cls.__bases__
    if not __bases__: return ""
    clsnames=[]
    for base in __bases__:
        module = getmodule(base)
        if cls.__module__==module:
            clsnames.append(base.__name__)
        else:
            name = objectname(base,fullname=fullname)
            clsnames.append(name)
    return "(%s)" % ",".join(clsnames)

@public
def formatclass(cls,fullname=True,args=True,formatvalue=formatvalue,space=True):
    """todo"""
    name = cls.__name__+formatbases(cls,fullname=fullname)
    #args = False # by default no
    if not issharedobject(cls) and hasattr(cls,"__init__"):
        #if iscyfunction(cls.__init__):
            #args = False
        #else:
        if ismethoddescriptor(cls.__init__):
            args = False
        else: # python source
            if len(defargs(cls.__init__))==1:
                args = False
    if not args:
        return name
    else:
        return name+formatfunction(cls.__init__,
            name=False,
            formatvalue=formatvalue,
            firstarg=False,
            space=space
        )

if __name__=="__main__":
    class Cls(object): pass
    class Cls2(Cls): 
        def __init__(self,arg,arg2="default"): pass
    print(formatclass(Cls2))
    print("\nfullname")
    print(formatclass(Cls2,fullname=True))
    print(formatclass(Cls2,fullname=False))
    print("\nargs")
    print(formatclass(Cls2,args=True))
    print(formatclass(Cls2,args=False))
    print("\nspace")
    print(formatclass(Cls2,space=True))
    print(formatclass(Cls2,space=False))
