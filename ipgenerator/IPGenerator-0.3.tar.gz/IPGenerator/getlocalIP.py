#!/usr/bin/env python
from socket import socket, AF_INET, SOCK_STREAM, inet_ntoa
from IPGenerator import IPGen, Netinfo

def Bits(Bytes):
	if not isinstance(Bytes, list):
		exit()
	bits = 0
	mask = 0

	for Byte in Bytes:
		for i in range(8):
			mask += 1 << (7 - i) % 8
			if  Byte == mask:
				bits += 1
			else:
				if mask > Byte:
					pass
				else:
					bits+=1
		mask = 0
	return bits

def localIP():
	try:
		GW = Netinfo().GATEWAY()
		MASK = Netinfo().MASK()
		cidr = Bits(MASK.split("."))
		
	except:
		print   "[-] No default route found"
	ip = IPGen()
	ip.net = GW+"/"+str(cidr)
	listofIPs = ip.IPGen()
	s = socket(AF_INET, SOCK_STREAM)
	for IP in listofIPs:
		try:
			s.connect(( IP, 80))
			break
		except:
			pass
	s.close()

	last = None
	f = open("/proc/net/tcp", "r")
	for line in f.readlines():
		last = line
	l = inet_ntoa(last.split()[1].split(":")[0].decode("hex")).split(".")
	l.reverse()
	f.close()
	del(listofIPs)
	return  ".".join(l)
	
		
localIP()
