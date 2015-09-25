#!/usr/bin/env python
#Author: Boumediene Kaddour
#Program: IPChecker.py
#Country: Algeria
#City: Maghnia/Tlemcen
#Purpose: Check if IP is Private, Public or Invalid

from re import findall

class IPChecker(object):
    def __init__(self, IP):
        self.IP = IP

    def isValid(self):
        if findall( "(?i)^(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$" ,self.IP):
            return True
        else:
            return False
        
    def isPrivate(self):
        if findall( "(?i)^(192).(168).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$", self.IP ):
            return True
        if findall( '(?i)^(127).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$',self.IP):
            return True
        if findall( '(?i)^(10).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$', self.IP):
            return True
        if findall( '(?i)^(172).(1[6-9]|2[0-5]|3[0-1]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$', self.IP):
            return True
        return False
    
    def isMCast(self):
        if findall( "(?i)^(2[2-3][4-9]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$", self.IP ):
            return True
        else:
            return False

    # is public
    def isPublic(self):
        if self.isValid() and not self.isPrivate() and not self.isMCast():
            return True
        else:
            return False
        
