#!/usr/bin/env python3
#
# $Id: //guest/lester_cheung/p4util/p4util/script/P4PyReview.py#1 $
#
# Copyright (c) 2012 Sven Erik Knop, Perforce Software Ltd
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are 
# met:
# 
# 1.  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the 
#     distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PERFORCE 
# SOFTWARE, INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Perforce review daemon (P4Python version)
#
# This script emails descriptions of new changelists and/or new or modified
# jobs to users who have expressed an interest in them.  In addition, the script
# creates a log file and adds entries to the log file if the debug variable
# is set to 1 or an error is encountered by the script.  Users express
# interest in reviewing changes and/or jobs by setting the "Reviews:" field
# on their user form (see "p4 help user").  Users are notified of changes
# if they review any file involved in that change. Users are notified of
# job updates if they review "//depot/jobs". (This value is configurable
# - see the <jobpath> configuration variable in the configuration file).
#
# If run directly with the <repeat> configuration variable = 1, the script
# will sleep for "sleeptime" seconds and then run again.  On UNIX you can
# run the script from cron by setting <repeat> = 0 and adding the following
# line to the cron table with "crontab -e:"
#
#        * * * * * /path/to/p4review.py
#
# This will run the script every minute.  Note that if you use cron you
# should be sure that the script will complete within the time allotted.
#
# P4PyReview requires 
# 	Python 3.2+
#	P4Python 2011.1+

from configparser import ConfigParser as ConfigParser
from P4 import P4, P4Exception
import logging.config
import smtplib
import argparse
import sys
import time
import os.path

CONFIG_FILE = 'p4review.cfg'

class P4Review:
	def __init__(self, options):
		self.options = options
		
		self.parser = ConfigParser()
		try:
			with open(self.options.config) as f:
				self.parser.read_file(f)
		except IOError as e:
			print("Cannot open configfile \"%s\"" % self.options.config	, file=sys.stderr)
			sys.exit(1)
			
		self.perforce = self.parser['Perforce']
		self.mail = self.parser['Mail']
		self.logging = self.parser['Logging']
		self.review = self.parser['Review'] 
		
		self.repeat = int(self.review['repeat'])
		self.notify_changes = int(self.review['notify_changes'])
		self.notify_jobs = int(self.review['notify_jobs'])
		self.sleeptime = int(self.review['sleeptime'])
		
		self.setupLogging()
	
	def setupLogging(self):
		if 'logger' in self.logging:
			if os.path.exists(self.logging['logger']):
				logging.config.fileConfig(self.logging['logger'])
				self.logger = logging.getLogger("review.file") # for debug
			else:
				print("Logger config file %s does not exist" % self.logging['logger'], file=sys.stderr)
				sys.exit(1)
		else:
			print("No 'logger' config file specified", file=sys.stderr)
			sys.exit(1)
		
		# The following is a hack:
		# list all the handlers for the logger
		# if there is a StreamHandler, set the logging level according
		# to the command line option
		
		handlers = self.logger.parent.handlers
		for h in handlers:
			if isinstance(h, logging.StreamHandler):
				if self.options.verbose:
					h.setLevel(self.options.verbose)
	
		self.logger.info("P4PyReview started")
	
	def notifyChanges(self):
		pass
	
	def notifyJobs(self):
		pass

	def notify(self):
		"""
		Run one iteration of notifications.
		"""
		
		# check whether we can talk to 
		try:
			if self.notify_changes:
				self.notifyChanges()
			if self.notify_jobs:
				self.notifyJobs()
		except P4Exception as e:
			if e.errors and "please login again" in e.errors[0]:
				if self.login():
					# successful logged in again, try again
					pass
				else:
					self.logger.exception("Session expired, and not able to login again.")
					raise e
			else:
				self.logger.exception("Encountered unhandled Perforce exception")
				raise e

		
	def login(self):
		"""
		Logs the user in in case the password is provided in the configuration file,
		otherwise does nothing.
		Returns True if successfully logged in
		Returns False if not attempt has been made
		Might exit the application if an incorrect password has been provided
		"""
		
		if 'P4PASSWD' in self.perforce:
			self.p4.password = self.perforce['P4PASSWD']
			try:
				self.logger.debug('Logging in user')
				self.p4.run_login()
				self.logger.debug('User logged in')
				return True
			except P4Exception as e:
				self.logger.critical("Login failed: " + e)
				self.exit(2)
		else:
			return False
	
	def run(self):
		self.p4 = P4()
		self.p4.port = self.perforce['P4PORT']
		self.p4.user = self.perforce['P4USER']
		with self.p4.connect():
			self.login() # ignores missing Password, assumes that ticket exists
			
			self.logger.debug("Entering main loop")
			
			while self.repeat:
				self.notify()
				self.logger.debug('Sleeping for %d seconds' % self.sleeptime)
				time.sleep(self.sleeptime)
			else:
				self.notify()
			
		self.logger.debug("Done.")
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="P4PyReview",
		epilog="Copyright (C) 2012 Perforce Software Ltd"
	)
	parser.add_argument('-c', '--config', default=CONFIG_FILE, help="Default is " + CONFIG_FILE)
	parser.add_argument('-v', '--verbose',
				nargs='?', 
				const="INFO",
				choices=('DEBUG', 'WARNING', 'INFO', 'ERROR', 'CRITICAL') ,
				help="Various levels of debug output")

	options = parser.parse_args()
	
	reviewer = P4Review(options)
	
	reviewer.run()
