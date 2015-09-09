#coding:utf8
'''
Created on 2011-10-3

@author: lan (www.9miao.com)
'''
import gevent.monkey
import gc
import struct
gevent.monkey.patch_all()
import socket
from gfirefly.dbentrust.memclient import memcached_connect
memcached_connect(["127.0.0.1:11211"])#,"python-ultramemcache"
from gfirefly.dbentrust.memclient import mclient
import sys
from gtwisted.core import reactor
        
from gtwisted.utils import log
from gfirefly.utils import services
from gfirefly.netconnect.protoc import LiberateFactory
from gevent.pool import Pool
p = Pool(2)
ss = set([])
gs = set([])
def getme(sessionno):
    result = mclient.set("a",sessionno)
    mid = id(mclient._get_server('1')[0])
    ss.add(mid)
    print "ss length",len(ss)
    print sessionno,"id(mclient._get_server('1')[0])",mid
#     optval = struct.pack("ii",1,0)
#     mclient._get_server('1')[0].socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, optval )
#     print "socket.socket.getsockopt",socket.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print gevent.getcurrent()
    print "mclient.get('a')",mclient.get("a")
    mclient.disconnect_all()
    return result

# run1 = [p.apply(getme) for _ in xrange(100)]

# reactor = reactor
service = services.CommandService("loginService")

def serviceHandle(target):
    '''服务处理
    @param target: func Object
    '''
    service.mapTarget(target)
    
factory = LiberateFactory()

def doConnectionLost(conn):
    print conn.transport

factory.doConnectionLost = doConnectionLost

def printMem():
    ### 强制进行垃圾回收
    print gc.collect()
    print "###################MEM#####################"
    print gc.garbage  
    print "###########################################"
    reactor.callLater(2, printMem)

def serverstart():
    '''服务配置
    '''
    log.startLogging(sys.stdout)
    factory.addServiceChannel(service)
#     reactor.callLater(10,factory.pushObject,111,'asdfe',[0,1])
#     reactor.callLater(2, printMem)
    reactor.listenTCP(1000,factory)
    reactor.run()
    
@serviceHandle
def echo_1(_conn,data):
    result = getme(_conn.transport.sessionno)
#     print "id(mclient._get_server('1')[0])",id(mclient._get_server('1')[0])
#     print result
    return "0"

if __name__ == "__main__":
    
    serverstart()

