#coding:utf8
'''
Created on 2014年2月22日

@author:  lan (www.9miao.com)
'''
import gevent.monkey
gevent.monkey.patch_all()
import sys
from gtwisted.core import reactor
from gtwisted.core.rpc import PBServerProtocl,PBServerFactory
from gtwisted.utils import log
import time
import httplib

import gc  
import objgraph

from gevent.event import AsyncResult

import memcache
mc = memcache.Client(["127.0.0.1:11211"])
mc.set("a",1)

def url_open(url):
    """
    """
    t1 = time.time()
    conn = httplib.HTTPConnection("github.com")
    conn.request(method="GET", url="/")
    ss = conn.getresponse()#urllib2.urlopen(url).read()
    t2 = time.time()
    print "time_delta",t2-t1
    return ss

def async_call(func,*args,**kw):
    """
    """
    a = AsyncResult()
    def _call(*args,**kw):
        """
        """
        a.set(func(*args,**kw))
    gevent.spawn(_call,*args,**kw)
    return a.get()

class MyPBServerProtocl(PBServerProtocl):
    
    def remote_getResult(self,a,b):
        print a,b
        print mc.get("a")
        dd = self.getRootObject()
        ss = async_call(dd.callRemoteForResult,"getResult",a,b)
        print "webcontent ready"
        print "11111111111"
        return ss
        
class MyPBServerFactory(PBServerFactory):
    
    protocol = MyPBServerProtocl
    
def printok():
    print "ok",time.time()
    print "##########################################"
    gc.collect()
    objgraph.show_most_common_types(limit=5)
    print "##########################################"
    reactor.callLater(1, printok)
    
# reactor.callLater(1, printok)
reactor.listenTCP(1000, MyPBServerFactory())
log.startLogging(sys.stdout)
reactor.run()


