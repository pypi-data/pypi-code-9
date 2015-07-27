#!/usr/bin/env python
# 
# Script to generate P4CONFIG files
#
# Input:
# 	Workspace root
#	P4PORT
#	P4CLIENT
#	P4USER

from __future__ import print_function

import sys
import os, os.path
from subprocess import Popen, PIPE
import re

P4="p4"

class ConfigGenerator:
	def __init__(self, root, port, client, user):
		self.root = root
		self.port = port
		self.client = client
		self.user = user
		self.dict = {}
		self.comments = []
		self.updated = False
		
	def create(self):
		if not os.path.isdir(self.root):
			os.makedirs(self.root)
		os.chdir(self.root)
		
		print("Creating P4CONFIG at %s with \n\tPort\t= %s\n\tClient\t= %s\n\tUser\t= %s" % (self.root, self.port, self.client, self.user))
		
		configFile, configPath = self.findConfig()
		if not configPath or configPath == "noconfig": # config file does not exist yet 
			configPath = os.path.join(self.root, configFile)
		else:
			print("Found %s" % configPath)
		
		if os.path.exists(configPath):
			with open(configPath) as f:
				for line in f:
					if line.startswith('#'):
						self.comments.append(line)
					elif "=" in line:
						key,value = line.split('=')
						self.dict[key]=value.rstrip()
		
		self.set("P4PORT", self.port)
		self.set("P4CLIENT", self.client)
		self.set("P4USER", self.user)
		
		if self.updated:
			with open(configPath, 'w') as f:
				for comment in self.comments:
					f.write(comment)
				for key, value in self.dict.iteritems():
					f.write(key+'='+value + "\n")
			print("Created or updated %s" % configPath)
		
	def set(self, key, value):
		if not key in self.dict or self.dict[key] != value:
			self.dict[key] = value
			self.updated = True
		
	def findConfig(self):
		with Popen([P4, "-d", self.root, "set", "P4CONFIG"], stdout = PIPE).stdout as s:
			output = s.read()
		
		# match either
		#   P4CONFIG=configfile\n
		# or
		#   P4CONFIG=configfile (config 'configpath')\n
		
		r = re.compile("P4CONFIG=([\w.]+)(\s*\(\w+\)\s*)?( \(config '(.*)'\))?%s" % os.linesep)
		m = r.match(output)
		if m:
			config = m.group(1)
			path = m.group(4)
			return config, path
		else:
			print("Cannot extract config file from >%s<" % output)
			sys.exit(1)
		
if __name__ == '__main__':
	if len(sys.argv) < 4:
		print("Usage: ConfigGenerator ws_root P4PORT P4CLIENT P4USER")
		print("Got parameters: ", sys.argv)
		sys.exit(1)
	
	root = sys.argv[1]
	port = sys.argv[2]
	client = sys.argv[3]
	user = sys.argv[4]
	
	c = ConfigGenerator(root, port, client, user)
	c.create()
