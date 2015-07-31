#coding:utf8
'''
Created on 2014年2月21日

@author:  lan (www.9miao.com)
'''
# from twisted.core.greactor import GeventReactor
from gtwisted.core import reactor
from gtwisted.core import protocols
from gevent import sleep

reactor = reactor

soc = None

def send(delta):
    """
    """
    if soc:
        soc.sendall("ok!")
    reactor.callLater(delta, send, delta)

class MyProtocol(protocols.BaseProtocol):
    
    def connectionMade(self):
#         pass
        global soc
        soc = self.transport
        print "connectionMade:",self.transport.sessionno
        
    def dataReceived(self, data):
        print "dataReceived:",data
        sleep(3)
        self.transport.sendall("hello")
        
    def connectionLost(self, reason):
#         pass
        soc = None
        print "connectionLost",reason
        
class MyServerFactory(protocols.ServerFactory):
    protocol = MyProtocol
    
from gtwisted.utils import log

ss = MyServerFactory()
import sys
log.startLogging(sys.stdout)
send(0.1)
reactor.listenTCP(80, ss)
reactor.run()

