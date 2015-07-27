#coding:utf8
'''
Created on 2014年2月22日

@author:  lan (www.9miao.com)
'''
import gevent.monkey
from gevent.event import AsyncResult
gevent.monkey.patch_thread()
from gtwisted.core import reactor
from gtwisted.core.rpc import PBClientProtocl,PBClientFactory
from gtwisted.utils import log
import sys
import time

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


class MyPBClientProtocl(PBClientProtocl):
    
    def remote_getResult(self,a,b):
        print "call client remote_getResult"
        return a+b
    
    def remote_printok(self):
        print "Hello World!"
        
class MyPBClientFactory(PBClientFactory):
    
    protocol = MyPBClientProtocl
    
client = MyPBClientFactory()

def printok():
    print "ok",time.time()
    reactor.callLater(1, printok)
    
def callRemote():
    dd = client.getRootObject()
    result = dd.callRemoteForResult('getResult1',8,9)
    print result
    
def callRemote2():
    dd = client.getRootObject()
    result = async_call(dd.callRemoteForResult,'getResult',8,9)
    print "result is",result
    reactor.callLater(0.5, callRemote2)

reactor.connectTCP('localhost', 1000, client)
reactor.callLater(2, callRemote2)
log.startLogging(sys.stdout)
reactor.run()
