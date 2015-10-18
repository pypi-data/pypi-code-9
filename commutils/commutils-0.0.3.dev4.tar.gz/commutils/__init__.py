#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

'''

import commutils
commutils.use_dev_commutils()
reload(commutils)

use this code for useing the live develop version of commutils located in /Users/lhr/_action/python/projects/commutils/

'''


import os,sys
import time

def time_count(function, *args, **kwargs):
    tStart = time.time()#計時開始

    function(*args,**kwargs)

    tEnd = time.time()#計時結束
    #列印結果
    print "[ %s ] cost %f sec" % (function.__name__,tEnd - tStart)#會自動做近位
    # print tEnd - tStart#原型長這樣

def print_time(fun):
    start = time.clock()
    fun()
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)

def import_path(path):
    if not path in sys.path:
        sys.path.append(path)

def use_dev_commutils():
    home=os.environ['HOME']
    mypub=os.path.join(home,'_action/python/projects/commutils/')
    if not mypub in sys.path:
        sys.path.insert(0,mypub)



if __name__ == '__main__':
    pass
