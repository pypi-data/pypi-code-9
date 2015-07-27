#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2011 Sven Erik Knop, Perforce Software Ltd
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1.  Redistributions of source code must retain the above copyright
#	  notice, this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright
#	  notice, this list of conditions and the following disclaimer in the
#	  documentation and/or other materials provided with the
#	  distribution.
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
# User contributed content on the Perforce Public Depot is not supported by Perforce,
# although it may be supported by its author. This applies to all contributions
# even those submitted by Perforce employees.
#
# PerforceTransfer.py
#
# This python script will provide the means to update a server
# with the data of another server. This is useful for transferring
# changes between independent servers when no remote depots are possible.
#
#
# The script requires a config file, normally called transfer.cfg,
# that provides the Perforce connection information for both servers.
# The script also needs a directory in which
# it can place the mapped files. This directory has to be the root
# of both servers' workspaces (this will be verified).
#
# The config file has three sections: [general], [source] and [target].
#
# [source] and [target] take the following parameters, respectively:
#	P4PORT
#	P4CLIENT
#	P4USER
#	COUNTER
#	P4PASSWD (optional)
#
# The general section currently has the following options
#	LOGGER (optional)	logger config file
#
# The counter represents the last transferred change number and must
# be initialized with a base change.
#
# usage:
#
# python PerforceTransfer.py [options]
#
#	options:
#			  -c configfile
#			  --config configfile
#							  specifies the configfile to use (default offline.cfg)
#
#			  -n
#							  do not replicate, only show what would happen
#
#			  -i
#			  --ignore		  replace integrations by adds and edits
#
#			  -v
#			  --verbose
#							  verbose mode
#
# (more too follow, undoubtedly)
#
# $Id: //guest/lester_cheung/p4util/p4util/script/PerforceTransfer.py#1 $

from __future__ import print_function

import sys
from P4 import P4, P4Exception, Resolver, Map

if sys.version_info[0] >= 3:
	from configparser import ConfigParser
else:
	from ConfigParser import ConfigParser

import argparse
import os.path
from datetime import datetime
import logging

CONFIG='transfer.cfg'
GENERAL_SECTION = 'general'
SOURCE_SECTION = 'source'
TARGET_SECTION = 'target'

LOGGER_NAME = "transfer"

class ChangeRevision:

	def __init__( self, r, a, t, d ):
		self.rev = r
		self.action = a
		self.type = t
		self.depotFile = d
		self.localFile = None

	def setIntegrationInfo(self, integ):
		self.integration = integ

	def setLocalFile(self, localFile):
		self.localFile = localFile
		
		localFile = localFile.replace("%40","@")
		localFile = localFile.replace("%23","#")
		localFile = localFile.replace("%2A","*")
		localFile = localFile.replace("%25","%")
		
		self.fixedLocalFile = localFile

	def __repr__(self):
		return 'rev = {rev} action = {action} type = {type} depotFile = {depotfile}' .format(
			rev = self.rev, 
			action = self.action, 
			type = self.type, 
			depotfile = self.depotFile,
		)


class P4Config:

	section = None
	P4PORT = None
	P4CLIENT = None
	P4USER = None
	P4PASSWD = None
	COUNTER = None
	counter = 0

	def __init__(self, section, options):
		self.section = section
		self.myOptions = options
		self.logger = logging.getLogger(LOGGER_NAME)

	def __str__(self):
		return '[section = {} P4PORT = {} P4CLIENT = {} P4USER = {} P4PASSWD = {} COUNTER = {}]'.format( \
			self.section,
			self.P4PORT,
			self.P4CLIENT,
			self.P4USER,
			self.P4PASSWD,
			self.COUNTER,
			)

	def connect(self, progname):
		self.p4 = P4()

		self.p4.port = self.P4PORT
		self.p4.client = self.P4CLIENT
		self.p4.user = self.P4USER
		self.p4.prog = progname
		self.p4.exception_level = P4.RAISE_ERROR

		self.p4.connect()
		if not self.P4PASSWD == None:
			self.p4.password = self.P4PASSWD
			self.p4.run_login()

		clientspec = self.p4.fetch_client(self.p4.client)
		self.root = clientspec._root
		self.p4.cwd = self.root
		self.clientmap = Map(clientspec._view)
		
		ctr = Map('//"'+clientspec._client+'/..."   "' + clientspec._root + '/..."')
		self.localmap = Map.join(self.clientmap, ctr)
		self.depotmap = self.localmap.reverse()
		

	def disconnect(self):
		self.p4.disconnect()

	def verifyCounter(self):
		change = self.p4.run_changes('-m1', '...')
		self.changeNumber = (int(change[0]['change']) if change else 0)
		return self.counter < self.changeNumber

	def missingChanges(self):
		changes = self.p4.run_changes('-l', '...@{rev},#head'.format(rev = self.counter + 1))
		changes.reverse()
		if self.myOptions.maximum:
			changes = changes[:self.myOptions.maximum]
		return changes

	def resetWorkspace(self):
		self.p4.run_sync('...#none')

	def getChange(self, change):
		"""Expects change number as a string"""

		self.p4.run_sync('-f', '...@{},{}'.format(change, change))
		change = self.p4.run_describe(change)[0]
		files = []
		for (n, rev) in enumerate(change['rev']):

			localFile = self.localmap.translate(change['depotFile'][n])
			if len(localFile) > 0:
				chRev = ChangeRevision(rev, change['action'][n], change['type'][n], change['depotFile'][n])
				files.append(chRev)

				chRev.setLocalFile(localFile)

				if chRev.action in ('branch', 'integrate', 'add', 'delete'):
					depotFile = self.p4.run_filelog('-m1', '{}#{}'.format(chRev.depotFile, chRev.rev))[0]
					revision = depotFile.revisions[0]
					if len(revision.integrations) > 0:
						for integ in revision.integrations:
							
							if 'from' in integ.how or integ.how == "ignored": 
								chRev.setIntegrationInfo(integ)

								integ.localFile = self.localmap.translate(integ.file)
								break

				if chRev.action == 'move/add':
					depotFile = self.p4.run_filelog('-m1', '{}#{}'.format(chRev.depotFile, chRev.rev))[0]
					revision = depotFile.revisions[0]
					integration = revision.integrations[0]
					chRev.setIntegrationInfo(integration)

					integration.localFile = self.localmap.translate(integration.file)

		return files

	def checkWarnings(self, where):
		if self.p4.warnings:
			self.logger.warning('warning in {} : {}'.format(where, str(self.p4.warnings)))

	def replicateChange(self, files, change, sourcePort	):
		"""This is the heart of it all. Replicate all changes according to their description"""

		for f in files:
			self.logger.debug( f )

			if not self.myOptions.preview:
				if f.action == 'edit':
					self.p4.run_sync('-k', f.localFile)
					self.p4.run_edit('-t', f.type, f.localFile)
					self.checkWarnings('edit')
				elif f.action == 'add':

					if 'integration' in f.__dict__:
						self.replicateBranch(f, True)  # dirty branch
					else:
						self.p4.run_add('-ft', f.type, f.fixedLocalFile)
						self.checkWarnings('add')
				elif f.action == 'delete':

					if 'integration' in f.__dict__:
						self.replicateIntegration(f)
						self.checkWarnings('integrate (delete)')
					else:
						self.p4.run_delete('-v', f.localFile)
						self.checkWarnings('delete')
				elif f.action == 'purge':

					# special case. Type of file is +S, and source.sync removed the file
					# create a temporary file, it will be overwritten again later

					dummy = open(f.localFile, 'w')
					dummy.write('purged file')
					dummy.close()
					self.p4.run_sync('-k', f.localFile)
					self.p4.run_edit('-t', f.type, f.localFile)
					if self.p4.warnings:
						self.p4.run_add('-tf', f.type, f.fixedLocalFile)
						self.checkWarnings('purge -add')
				elif f.action == 'branch':

					self.replicateBranch(f, False)
					self.checkWarnings('branch')
				elif f.action == 'integrate':

					self.replicateIntegration(f)
					self.checkWarnings('integrate')
				elif f.action == 'move/add':

					self.move(f)

		newChangeId = None

		opened = self.p4.run_opened()
		if len(opened) > 0:
			description = change['desc'] \
				+ '''

Transferred from p4://%s@%s''' % (sourcePort,
					change['change'])
			result = self.p4.run_submit('-d', description)

			self.logger.debug(str(result))
	  		# the submit information can be followed by resfreshFile lines
	  	 	# need to go backwards to find submittedChange

			a = -1
			while 'submittedChange' not in result[a]:
				a -= 1
			newChangeId = result[a]['submittedChange']

			self.updateChange(change, newChangeId)
			self.reverifyRevisions(result)
			
		self.logger.info("source = {} : target = {}".format(change['change'],newChangeId))
		
		return newChangeId

	def updateChange(self, change, newChangeId):
		# need to update the user and time stamp 
		newChange = self.p4.fetch_change(newChangeId)

		newChange._user = change['user']
		# date in change is in epoch time, we need it in canonical form
		newDate = datetime.utcfromtimestamp(int(change['time'])).strftime("%Y/%m/%d %H:%M:%S")
		newChange._date = newDate
		
		self.p4.save_change(newChange, '-f')
		
	def reverifyRevisions(self, result):
		revisionsToVerify = [ "{file}#{rev},{rev}".format(file=x['refreshFile'],rev=x['refreshRev']) 
								for x in result
								if 'refreshFile' in x
							]
		if revisionsToVerify:
			self.p4.run_verify('-qv', revisionsToVerify)
		
	def replicateBranch(self, file, dirty):
		if self.myOptions.ignore == False \
			and file.integration.localFile:
			if file.integration.how == 'add from':

		# determine the filelog of the file in the target database
		# this is not so easy since filelog will return nothing for a deleted file
		# so we need to find the depotFile for the localFile first

				df = self.depotmap.translate(file.localFile)
				f = self.p4.run_filelog(df)
				if len(f) > 0 and len(f[0].revisions) >= 2:

		  # in 2011.1 we can ignore into deleted files, so we need to make sure
		  # we catch a real version

					i = 0
					while f[0].revisions[i].action == 'delete':
						i += 1
					rev = f[0].revisions[i]	 # this is the revision just before the delete
					self.p4.run_sync('-f', '%s#%d' % (rev.depotFile, rev.rev))
					self.p4.run_add("-f", file.fixedLocalFile)
				else:

			  # something fishy going on. Just add the file

					self.p4.run_add('-ft', file.type, file.fixedLocalFile)
			else:
				self.p4.run_integrate('-v', file.integration.localFile, file.localFile)
				if dirty:
					self.p4.run_edit(file.localFile)
		else:
			self.p4.run_add('-ft', file.type, file.fixedLocalFile)

	def replicateIntegration(self, file):
		if self.myOptions.ignore == False \
			and file.integration.localFile:
			if file.integration.how == 'edit from':
				with open(file.localFile) as f:
					content = f.read()
				self.p4.run_sync('-f', file.localFile)	# to avoid tamper checking
				self.p4.run_integrate(file.integration.localFile,
						file.localFile)


				class MyResolver(Resolver):

					def __init__(self, content):
						self.content = content

					def resolve(self, mergeData):
						with open(mergeData.result_path, 'w') as f:
							f.write(self.content)
						return 'ae'


				self.p4.run_resolve(resolver=MyResolver(content))
			else:

				self.p4.run_sync('-f', file.localFile)	# to avoid tamper checking
				self.p4.run_integrate(file.integration.localFile,
						file.localFile)
				if file.integration.how == 'copy from':
					self.p4.run_resolve('-at')
				elif file.integration.how == 'ignored':
					self.p4.run_resolve('-ay')
				elif file.integration.how in ('delete', 'delete from'):
					self.p4.run_resolve('-at')
				elif file.integration.how == 'merge from':

		  			# self.p4.run_edit(file.localFile) # to overcome tamper check

					self.p4.run_resolve('-am')
				else:
					self.logger.error ('Cannot deal with {}'.format( file.integration ))
		else:
			if file.integration.how in ('delete', 'delete from'):
				self.p4.run_delete('-v', file.localFile)
			else:
				self.p4.run_sync('-k', file.localFile)
				self.p4.run_edit(file.localFile)

	def move(self, file):
		source = file.integration.localFile
		self.p4.run_sync('-f', source)
		self.p4.run_edit(source)
		self.p4.run_move('-k', source, file.localFile)


class P4Transfer:

	def __init__(self, *argv):
		parser = argparse.ArgumentParser(
			description="PerforceTransfer",
			epilog="Copyright (C) 2013 Sven Erik Knop, Perforce Software Ltd"
		)
		
		parser.add_argument('-n', '--preview', action='store_true', help="Preview only, no transfer")
		parser.add_argument('-c', '--config', default=CONFIG, help="Default is " + CONFIG)
		parser.add_argument('-m', '--maximum', default=None, type=int, help="maximum number of changes to transfer")
		parser.add_argument('-p', '--preflight', action='store_true', help="Run a sanity check first to ensure target is empty")
		parser.add_argument('-v', '--verbose', 
						nargs='?', 
						const="INFO", 
						default="WARNING",
						choices=('DEBUG', 'WARNING', 'INFO', 'ERROR', 'FATAL') ,
						help="Various levels of debug output")
		parser.add_argument('-i', '--ignore', action='store_true')
		
		self.myOptions = parser.parse_args()

		self.logger = logging.getLogger(LOGGER_NAME)
		self.logger.setLevel(self.myOptions.verbose)

	def readConfig(self):
		self.parser = ConfigParser()
		self.myOptions.parser = self.parser	 # for later use
		try:
			self.parser.readfp(open(self.myOptions.config))
		except:
			print( 'Could not read %s' % self.myOptions.config )
			sys.exit(2)   


		if self.parser.has_section(GENERAL_SECTION):
			if self.parser.has_option(GENERAL_SECTION, "LOGFILE"):
				logfile = self.parser.get(GENERAL_SECTION, "LOGFILE")
				
				fh = logging.FileHandler(logfile)
				fh.setLevel(self.myOptions.verbose)
				
				formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
				fh.setFormatter(formatter)
				
				self.logger.addHandler(fh)
		else:
			print( 'No general section in config file, bailing out')
			sys.exit(3)
		
		self.source = P4Config(SOURCE_SECTION, self.myOptions)
		self.target = P4Config(TARGET_SECTION, self.myOptions)

		self.readSection(self.source)
		self.readSection(self.target)

	def writeConfig(self):
		with open(self.myOptions.config, 'w') as f:
			self.parser.write(f)

	def readSection(self, p4config):
		if self.parser.has_section(p4config.section):
			self.readOptions(p4config)
		else:
			print( 'Config file needs section %s' % p4config.section )
			sys.exit(3)

	def readOptions(self, p4config):
		self.readOption('P4CLIENT', p4config)
		self.readOption('P4USER', p4config)
		self.readOption('P4PORT', p4config)
		self.readOption('COUNTER', p4config, optional=True)
		self.readOption('P4PASSWD', p4config, optional=True)
		
	def readOption( self, option, p4config,	optional=False ):
		if self.parser.has_option(p4config.section, option):
			p4config.__dict__[option] = self.parser.get(p4config.section, option)
		elif not optional:
			print( 'Required option %s not found in section %s' % (option, p4config.section) )
			sys.exit(1)

	def setCounter(self, section, value):
		"""Sets the counter to value. Value must be a string"""

		self.parser.set(section, 'COUNTER', value)

  #
  # This is the central method
  # It provides the replication process
  # Algorithm:
  #	  Read the config file
  #	  Connect to server1 and server
  #	  Determine if counter is there

	def replicate(self):
		"""Central method that performs the replication between server1 and server2"""

		self.readConfig()

		self.source.connect('source replicate')
		self.target.connect('target replicate')

		if not self.source.root == self.target.root:
			print( 'server1 and server2 workspace root directories must be the same' )
			sys.exit(5)

		self.source.counter = int(self.source.COUNTER)
		if not self.source.verifyCounter():
			print("Nothing to do. Good bye")
			sys.exit(0)

		self.source.resetWorkspace()

		if self.myOptions.preflight:
			print("Running pre-flight check first ...")
			targetFiles = self.target.p4.run_fstat('-T clientFile', '...')
			sourceFiles = self.source.p4.run_fstat('-T clientFile', '...')
			
			for f in targetFiles:
				if f in sourceFiles:
					depotFile = self.target.p4.run_fstat(f['clientFile'])[0]
					print("Failed pre-flight check, file '{}' in source and target".format(depotFile['depotFile']), file=sys.stderr)
					sys.exit(1)
			print("Finished pre-flight check ...")
		
		try:
			for change in self.source.missingChanges():
				self.logger.debug('Processing : {} "{}"'.format(change['change'], change['desc']))
				files = self.source.getChange(change['change'])
				resultedChange = self.target.replicateChange(files, change,	self.source.p4.port)
				if resultedChange:
					self.setCounter(self.source.section, change['change'])
					self.setCounter(self.target.section, resultedChange)
					self.writeConfig()
		except P4Exception as e:
			self.logger.error(e)
		
		self.source.disconnect()
		self.target.disconnect()


if __name__ == '__main__':
	prog = P4Transfer(*sys.argv[1:])
	prog.replicate()
