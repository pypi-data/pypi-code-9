#!/usr/bin/env python
# WebSite: http://www.pentestingskills.com/
# Author : Boumediene Kaddour
# Name   : IPGenerator.py
# Purpose: Generates IPs for a given network
# Country: Algeria
# Email  : snboumediene@gmail.com
try:
	from IPChecker import IPChecker
except:
	from os import system
	system("pip install IPChecker")
	from IPChecker import IPChecker
from IPCalc import IPCalc
from socket import inet_ntoa

class IPGen:
	def __init__(self, net=None):
		self.net = net
		self.IPList = []

	def isNetOK(self):
		if "/" in self.net:
			addr, cidr = self.net.split("/")
			ip = IPChecker(addr)
			if int(cidr) > 32 or int(cidr) < 0:
				return False
			else:
				if ip.isValid():
					return True
				else:
					return False
		else:
			return False
	
	def __addrs__(self):
		return IPCalc(self.net)
	
	def NETWORK(self):
		return self.__addrs__()[0]

	def MASK(self):
		return self.__addrs__()[1]

	def BCAST(self):
		return self.__addrs__()[2]

	def FIRST(self):
		return ".".join( [ str(octet) for octet in self.__addrs__()[3]])

	def LAST(self):
		return ".".join( [ str(octet) for octet in self.__addrs__()[4]])
	

	def IPGen(self):
		try:
			fst, last = self.__addrs__()[3], self.__addrs__()[4]
		except:
			return None
		lst1 = []
		lst2 = []
		indxBool1 = False
		indxBool2 = False
		indx = 0
		try:
			for i, j in zip(fst, last):
				if i == j:
					indx+=1
				else:
					if indx == 1:
						for octet in range(int(i), int(j)+1):
							indxBool1 = True
							lst1.append(octet)
						indx+=1
					elif indx == 2:
						for octet in range(int(i), int(j)+1):
							indxBool2 = True
							lst2.append(octet)
						indx+=1
					elif indx == 3:
						if indxBool1 is True:
							genindx = 1
						elif indxBool2 is True:
							genindx = 2
						else:
							genindx = indx
						if genindx == 1:
							self.IPList = []
							for octet in lst1:
								for octet2 in lst2:
									for octet3 in range(int(i), int(j)+1):
										self.IPList += [ ".".join( [ str(p) for p in fst[0:genindx ] ] )+".%s.%s.%s"%(octet, octet2, octet3) ]
							del lst1
						elif genindx == 2:
							self.IPList = []
							for octet in lst2:
								for octet2 in range(int(i), int(j)+1):
									self.IPList+=[".".join( [ str(p) for p in fst[0:genindx] ] )+".%s.%s"%(octet, octet2)]
							del lst2
						else:
							self.IPList = []
							for octet in range(int(i), int(j)+1):
								self.IPList+=[".".join( [ str(p) for p in fst[0:genindx ] ] )+".%s"%octet]
					else:	
						pass
			return self.IPList
		except KeyboardInterrupt:
			print "User hit CTRL+C"
			exit(1)





class Netinfo:
	def __init__(self,arpfilename="/proc/net/arp", routefile="/proc/net/route"):
		self.arpfilename = arpfilename
		self.routefile = routefile

	def __Parser__(self):
		counter = 0
		ROUTE = []
		ARP = []
		for filename in [self.routefile, self.arpfilename]:
			f = open(filename, "r")
			for line in f.readlines():
				if counter == 0:
					pass
				elif counter == 1 and filename == self.routefile or counter == 2 and filename == self.routefile:
					ROUTE.append(line.split())
				elif counter > 2 and filename == self.routefile:
					break
				elif filename == self.arpfilename:
					ARP.append(line.split())
				else: 
					break
				counter += 1
			f.close()
			counter = 0
		return ROUTE,ARP

	def IFACE(self):
		try:
			return self.__Parser__()[0][0][0]
		except:
			pass

	def GATEWAY(self):
		try:
			RAW_GW = self.__Parser__()[0][0][2]
			GW_T = inet_ntoa(RAW_GW.decode("hex")).split(".")
			GW_T.reverse()
			GW = ".".join(GW_T)
		except:
			print "We couldn't recognize the GATEWAY, Check it out please"
			exit(1)
		return GW

	def GW_MAC(self):
		GW = self.GATEWAY()
		GW_MAC = ""
		ARP_T = self.__Parser__()[1]
		for entry in ARP_T:
			if GW in entry:
				GW_MAC = entry[3]
			else:
				pass
		return GW_MAC
	
	def MASK(self):
		RAW_Value = self.__Parser__()[0][1][7]
		MASK_T = inet_ntoa(RAW_Value.decode("hex")).split(".")
		MASK_T.reverse()
		MASK = ".".join(MASK_T)
		return MASK

	def localIP(self):
		from getlocalIP import localIP
		return localIP()

		
