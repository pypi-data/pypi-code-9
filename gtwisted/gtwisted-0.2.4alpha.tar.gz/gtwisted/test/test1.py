#coding:utf8
'''
Created on 2014年2月21日

@author:  lan (www.9miao.com)
'''
from thread import start_new
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 80))
import time
time.sleep(2)
sock.send('1')

def start():
    for i in range(10): 
        sock.sendall('asdfe')
        data = sock.recv(1024)
        print data
        
for i in range(10):
    start_new(start,())
while True:
    pass







