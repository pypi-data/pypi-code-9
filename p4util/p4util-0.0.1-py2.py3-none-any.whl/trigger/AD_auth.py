#!/usr/local/bin/python
# Copyright (c) 2011 Perforce Software, Inc.  Provided for use as defined in
# the Perforce Consulting Services Agreement.

from __future__ import print_function

import ldap, sys

# Configuration values
TIMEOUT=10
AD_HOST      = "ldap://ldap:389"
AD_READ_DN   = 'CN=perforce,CN=Users,DC=company,DC=org'
AD_READ_PWD  = 'mypassword'

def verifyPassword(user):
	password = sys.stdin.read().rstrip()  # read password from STDIN
	con = ldap.initialize(AD_HOST)
	con.set_option(ldap.OPT_TIMEOUT, TIMEOUT)
	
	try:
		result = con.bind(AD_READ_DN, AD_READ_PWD)
		answer = con.result(result)
	
		result = con.search('', ldap.SCOPE_BASE , '(objectclass=*)')
		answer = con.result(result)
		base = answer[1][0][1]['rootDomainNamingContext'][0]
	
		result = con.search(base, ldap.SCOPE_SUBTREE, 'sAMAccountname=%s' % user, ['mail'])
		answer = con.result(result)
		users = answer[1]
		for user in users:
			result = con.bind(user[0], password)
			try:
				answer = con.result(result)
				return 0
			except ldap.INVALID_CREDENTIALS as e:
				pass
		return 1
	except Exception as e:
		print( e )
		return 1
		
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print( "Usage: %s username" % sys.argv[0])
		sys.exit(1)
	result = verifyPassword(sys.argv[1])
	if (result):
		print("Authentication Failed.  Access Denied")
		sys.exit(1)
	sys.exit(0)
