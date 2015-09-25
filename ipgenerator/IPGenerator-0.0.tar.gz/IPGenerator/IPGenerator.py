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

class IPGenerator:
	def __init__(self, net):
		self.net = net
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
	def IPGen(self):
		if not self.isNetOK():
			print "[-] %s: Invalid given Network"%self.net
			return
		addrs =IPCalc(self.net)
		try:
			fst, last = addrs[3], addrs[4]
		except:
			exit()
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
							for octet in lst1:
								for octet2 in lst2:
									for octet3 in range(int(i), int(j)+1):
										print ".".join( [ str(p) for p in fst[0:genindx ] ] )+".%s.%s.%s"%(octet, octet2, octet3)
							del lst1
						elif genindx == 2:
							for octet in lst2:
								for octet2 in range(int(i), int(j)+1):
									print ".".join( [ str(p) for p in fst[0:genindx] ] )+".%s.%s"%(octet, octet2)
							del lst2
						else:
							for octet in range(int(i), int(j)+1):
								print ".".join( [ str(p) for p in fst[0:genindx ] ] )+".%s"%octet
					else:	
						pass
			print "[+] Done"
		except KeyboardInterrupt:
			print "User hit CTRL+C"
			exit(1)
