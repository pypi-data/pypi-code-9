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
# The config file has two sections: [server1] and [server2].
# Each section takes the following parameters:
#	 P4PORT
#	 P4CLIENT
#	 P4USER
#	 COUNTER
#	 P4PASSWD (optional)
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
# $Id: //guest/lester_cheung/p4util/p4util/script/PerforceExchange.py#1 $

from __future__ import print_function

import sys
from P4 import P4, P4Exception, Resolver, Map

if sys.version_info[0] >= 3:
	from configparser import ConfigParser
else:
	from ConfigParser import ConfigParser

import argparse
import os.path

CONFIG='transfer.cfg'

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

	def __repr__(self):
		return 'rev = %s action = %s type = %s depotFile = %s' \
			% (self.rev, self.action, self.type, self.depotFile)


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

	def __str__(self):
		return '[section = %s P4PORT = %s P4CLIENT = %s P4USER = %s P4PASSWD = %s COUNTER = %s]' \
			% (
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
		changes = self.p4.run_changes('-l', '...@%d,#head'
				% (self.counter + 1))
		changes.reverse()
		return changes

	def resetWorkspace(self):
		self.p4.run_sync('...#none')

	def getChange(self, change):
		"""Expects change number as a string"""

		self.p4.run_sync('-f', '...@%s,%s' % (change, change))
		change = self.p4.run_describe(change)[0]
		files = []
		for (n, rev) in enumerate(change['rev']):

	  # 'p4 where' tests if the file is mapped to this workspace

			localFile = self.localmap.translate(change['depotFile'][n])
			if localFile > 0:
				chRev = ChangeRevision(rev, change['action'][n],
						change['type'][n], change['depotFile'][n])
				files.append(chRev)

				chRev.setLocalFile(localFile)

				if chRev.action in ('branch', 'integrate', 'add', 'delete'):
					depotFile = self.p4.run_filelog('-m1', '%s#%s' % (chRev.depotFile, chRev.rev))[0]
					revision = depotFile.revisions[0]
					if len(revision.integrations) > 0:
						for integ in revision.integrations:
							
							if 'from' in integ.how or integ.how == "ignored": 
								chRev.setIntegrationInfo(integ)

								integ.localFile = self.localmap.translate(integ.file)
								break

				if chRev.action == 'move/add':
					depotFile = self.p4.run_filelog('-m1', '%s#%s'
							% (chRev.depotFile, chRev.rev))[0]
					revision = depotFile.revisions[0]
					integration = revision.integrations[0]
					chRev.setIntegrationInfo(integration)

					integration.localFile = self.localmap.translate(integration.file)

		return files

	def checkWarnings(self, where):
		if self.p4.warnings:
			print ('warning in ', where, ' : ', self.p4.warnings)

	def replicateChange(self, files, change, sourcePort	):
		"""This is the heart of it all. Replicate all changes according to their description"""

		for f in files:
			print( f )

			if not self.myOptions.preview:
				if f.action == 'edit':
					self.p4.run_sync('-k', f.localFile)
					self.p4.run_edit('-t', f.type, f.localFile)
					self.checkWarnings('edit')
				elif f.action == 'add':

					if 'integration' in f.__dict__:
						self.replicateBranch(f, True)  # dirty branch
					else:
						self.p4.run_add('-t', f.type, f.localFile)
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
						self.p4.run_add('-t', f.type, f.localFile)
						self.checkWarnings('purge -add')
				elif f.action == 'branch':

					self.replicateBranch(f, False)
					self.checkWarnings('branch')
				elif f.action == 'integrate':

					self.replicateIntegration(f)
					self.checkWarnings('integrate')
				elif f.action == 'move/add':

					self.move(f)

		opened = self.p4.run_opened()
		if len(opened) > 0:
			description = change['desc'] \
				+ '''

Transferred from p4://%s@%s''' % (sourcePort,
					change['change'])
			result = self.p4.run_submit('-d', description)

	  # the submit information can be followed by resfreshFile lines
	  # need to go backwards to find submittedChange

			a = -1
			while 'submittedChange' not in result[a]:
				a -= 1
			return result[a]['submittedChange']
		else:
			return None

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
					self.p4.run_sync('-f', '%s#%d' % (rev.depotFile,
							rev.rev))
					self.p4.run_add(file.localFile)
				else:

			  # something fishy going on. Just add the file

					self.p4.run_add('-t', file.type, file.localFile)
			else:
				self.p4.run_integrate('-v', file.integration.localFile,
						file.localFile)
				if dirty:
					self.p4.run_edit(file.localFile)
		else:
			self.p4.run_add('-t', file.type, file.localFile)

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
					print ('Cannot deal with ', file.integration)
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


class P4Exchange:

	def __init__(self, *argv):
		parser = argparse.ArgumentParser(
			description="PerforceTransfer",
			epilog="Copyright (C) 2011,2012 Sven Erik Knop, Perforce Software Ltd"
		)
		
		parser.add_argument('-n', '--preview', action='store_true', help="Preview only, no transfer")
		parser.add_argument('-c', '--config', default=CONFIG, help="Default is " + CONFIG)
		parser.add_argument('-v', '--verbose', 
						nargs='?', 
						const="INFO", 
						default="WARNING",
						choices=('DEBUG', 'WARNING', 'INFO', 'ERROR', 'FATAL') ,
						help="Various levels of debug output")
		parser.add_argument('-i', '--ignore', action='store_true')
		
		self.myOptions = parser.parse_args()

	def readConfig(self):
		self.parser = ConfigParser()
		self.myOptions.parser = self.parser	 # for later use
		try:
			self.parser.readfp(open(self.myOptions.config))
		except:
			print( 'Could not read %s' % self.myOptions.config )
			sys.exit(2)

		self.server1 = P4Config('server1', self.myOptions)
		self.server2 = P4Config('server2', self.myOptions)

		self.readSection(self.server1)
		self.readSection(self.server2)

		print( 'server1 = %s' % self.server1 )
		print( 'server2 = %s' % self.server2 )

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
		self.readOption('COUNTER', p4config)
		self.readOption('P4PASSWD', p4config, optional=True)

	def readOption(
		self,
		option,
		p4config,
		optional=False,
		):
		if self.parser.has_option(p4config.section, option):
			p4config.__dict__[option] = \
				self.parser.get(p4config.section, option)
		elif not optional:
			print( 'Required option %s not found in section %s' \
				% (option, p4config.section) )
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

		print( 'Configfile = %s' % self.myOptions.config )
		self.readConfig()

		self.server1.connect('server1 replicate')
		self.server2.connect('server2 replicate')

		print( 'server1 = %s' % self.server1.p4 )
		print( 'server2 = %s' % self.server2.p4 )

	# determine which version is newer

		self.server1.counter = int(self.server1.COUNTER)
		self.server2.counter = int(self.server2.COUNTER)

		mv = self.server1.verifyCounter()
		lv = self.server2.verifyCounter()

		source = None
		target = None

		if mv and not lv:
			print( 'Replicate from server1 to server2.' )
			source = self.server1
			target = self.server2
		elif lv and not mv:
			print( 'Replicate from server2 to server1.' )
			source = self.server2
			target = self.server1
		elif lv and mv:
			print( 'Both sides out of sync. Giving up.' )
			sys.exit(4)
		else:
			print( 'Nothing to do.' )
			sys.exit(0)

		if not source.root == target.root:
			print( 'server1 and server2 workspace root directories must be the same' )
			sys.exit(5)

		source.resetWorkspace()

		for change in source.missingChanges():
			print ('Processing : ', change['change'], change['desc'])
			files = source.getChange(change['change'])
			resultedChange = target.replicateChange(files, change,
					source.p4.port)
			if resultedChange:
				self.setCounter(source.section, change['change'])
				self.setCounter(target.section, resultedChange)
				self.writeConfig()

		source.disconnect()
		target.disconnect()


if __name__ == '__main__':
	prog = P4Exchange(*sys.argv[1:])
	prog.replicate()
