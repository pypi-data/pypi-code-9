# -*- encoding: UTF8 -*-

from __future__ import print_function

import sys
import time
import P4
import unittest, os, types, shutil, stat
from subprocess import Popen, PIPE

if sys.version_info[0] >= 3:
	from configparser import ConfigParser
else:
	from ConfigParser import ConfigParser

P4D="p4d"
P4USER="testuser"
P4CLIENT="test_ws"
TRANSFER_CLIENT="transfer"
TRANSFER_CONFIG="transfer.cfg"
PYTHON="python"
PERFORCE_TRANSFER="PerforceExchange.py"
INTEG_ENGINE=3

def onRmTreeError( function, path, exc_info ):
	os.chmod( path, stat.S_IWRITE)
	os.remove( path )

def ensureDirectory(directory):
	if not os.path.isdir(directory):
		os.mkdir(directory)

class P4Server:
	def __init__(self, root):
		self.root = root
		self.server_root = os.path.join(root, "server")
		self.client_root = os.path.join(root, "client")

		ensureDirectory(self.root)
		ensureDirectory(self.server_root)
		ensureDirectory(self.client_root)

		self.p4d = P4D
		self.port = "rsh:%s -r \"%s\" -L log -i" % ( self.p4d, self.server_root )
		self.p4 = P4.P4()
		self.p4.port = self.port
		self.p4.user = P4USER
		self.p4.client = P4CLIENT
		self.p4.connect()
		
		self.p4.run_depots() # triggers creation of the user
		self.p4.run_configure('set', 'dm.integ.engine=%d' % INTEG_ENGINE)
		
		self.p4.disconnect() # required to pick up the configure changes
		self.p4.connect()
		
		self.client_name = P4CLIENT
		client = self.p4.fetch_client(self.client_name)
		client._root = self.client_root
		self.p4.save_client(client)
		
	def shutDown(self):
		if self.p4.connected():
			self.p4.disconnect()
	
	def createTransferClient(self, name, root):
		pass
	
	def enableUnicode(self):
		cmd = [self.p4d, "-r", self.server_root, "-L", "log", "-vserver=3", "-xi"]
		f = Popen(cmd, stdout=PIPE).stdout
		for s in f.readlines():
		  pass
		f.close()
	
class TestPerforceTransfer(unittest.TestCase):

	def setUp(self):
		self.setDirectories()
		
	def tearDown(self):
		self.source.shutDown()
		self.target.shutDown()
		time.sleep( 1 )
		self.cleanupTestTree()

	def setDirectories(self):
		self.startdir = os.getcwd()
		self.transfer_root = os.path.join(self.startdir, 'transfer')
		self.cleanupTestTree()

		ensureDirectory(self.transfer_root)

		self.source = P4Server(os.path.join(self.transfer_root, 'source'))
		self.target = P4Server(os.path.join(self.transfer_root, 'target'))
		
		self.transfer_client_root = os.path.join(self.transfer_root, 'transfer_client')
		ensureDirectory(self.transfer_client_root)
	
	def cleanupTestTree(self):
		os.chdir(self.startdir)
		if os.path.isdir(self.transfer_root):
			shutil.rmtree(self.transfer_root, False, onRmTreeError)
	
	def setupTransfer(self):
		"""Creates client workspaces on source and target and a config file"""
		source_client = self.source.p4.fetch_client(TRANSFER_CLIENT)
		source_client._root = self.transfer_client_root
		source_client._view = ['//depot/inside/... //%s/...' % TRANSFER_CLIENT]
		self.source.p4.save_client(source_client)
		
		target_client = self.target.p4.fetch_client('transfer')
		target_client._root = self.transfer_client_root
		target_client._view = ['//depot/import/... //%s/...' % TRANSFER_CLIENT]
		self.target.p4.save_client(target_client)
		
		# create the config file
		
		self.parser = ConfigParser()
		self.parser.add_section('server1')
		self.parser.set('server1', 'p4port', self.source.port)
		self.parser.set('server1', 'p4user', P4USER)
		self.parser.set('server1', 'p4client', TRANSFER_CLIENT)
		self.parser.set('server1', 'counter', '0')
		
		self.parser.add_section('server2')
		self.parser.set('server2', 'p4port', self.target.port)
		self.parser.set('server2', 'p4user', P4USER)
		self.parser.set('server2', 'p4client', TRANSFER_CLIENT)
		self.parser.set('server2', 'counter', '0')
		
		# write the config file
		
		self.transfer_cfg = os.path.join(self.transfer_root, TRANSFER_CONFIG)
		with open(self.transfer_cfg, 'w') as f:
			 self.parser.write(f)
	
	def run_PerforceTransfer(self):
		process = Popen([PYTHON, PERFORCE_TRANSFER, '-c', self.transfer_cfg], stdout=PIPE)
		out = process.stdout
		result = out.readlines()
		out.close()
		
		return result
		
	def assertCounters(self, sourceValue, targetValue):
		with open(self.transfer_cfg) as f:
			try:
				self.parser.read_file(f)
			except AttributeError: 
				self.parser.readfp(f)
		
		self.assertEqual(self.parser.getint("server1", 'counter'), sourceValue, "Source counter is not %d" % sourceValue)
		self.assertEqual(self.parser.getint("server2", 'counter'), targetValue, "Target counter is not %d" % targetValue)
		
	def testAdd(self):
		self.setupTransfer()
		
		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
		file1 = os.path.join(inside, "file1")

		with open(file1, 'w') as f:
			f.write('Test content')
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', 'File1 added')
		
		self.run_PerforceTransfer()
		
		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes), 1, "Target does not have exactly one change")
		self.assertEqual(changes[0]['change'], "1", "Target change is not 1")
		
		files = self.target.p4.run_files('//depot/...')
		self.assertEqual(len(files), 1, "Target does not have exactly one file")
		self.assertEqual(files[0]['depotFile'], '//depot/import/file1', "File not transferred to correct place")
		
		self.assertCounters(1,1)
 	
	def testEditAndDelete(self):
		self.setupTransfer()
		
		# add
 		
		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
		file1 = os.path.join(inside, "file1")
		with open(file1, 'w') as f:
			f.write('Test content')
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', "File1 added")
		
		# edit
		
		self.source.p4.run_edit(file1)
		with open(file1, 'a+') as f:
			f.write('More content')
		self.source.p4.run_submit('-d', "File1 edited")
		
		self.run_PerforceTransfer()
		
		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes), 2, "Target does not have exactly two changes")
		self.assertEqual(changes[0]['change'], "2", "Highest target change is not 2")
		
		self.assertCounters(2,2)
		
		# delete
		
		self.source.p4.run_delete(file1)
		self.source.p4.run_submit('-d', "File1 deleted")
		
		self.run_PerforceTransfer()
		
		self.assertCounters(3,3)

		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes), 3, "Target does not have exactly three changes")
		filelog = self.target.p4.run_filelog('//depot/import/file1')
		self.assertEqual(filelog[0].revisions[0].action, 'delete', "Target has not been deleted")
		
		# re-add
		
		with open(file1, 'w') as f:
			f.write('New content')
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', "Re-added")
		
		self.run_PerforceTransfer()
		
		self.assertCounters(4,4)

		filelog = self.target.p4.run_filelog('//depot/import/file1')
		self.assertEqual(filelog[0].revisions[0].action, 'add', "Target has not been re-added")
		
	def testFileTypes(self):
		self.setupTransfer()
		
		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
 		
		file1 = os.path.join(inside, "file1")
		with open(file1, 'w') as f:
			print("Test content", file=f)
		self.source.p4.run_add('-tbinary', file1)
		self.source.p4.run_submit('-d', "File1 added")
		
		self.run_PerforceTransfer()
		
		self.assertCounters(1,1)
		
		filelog = self.target.p4.run_filelog('//depot/import/file1')
		self.assertEqual(filelog[0].revisions[0].type, 'binary', "File type is not binary, but %s" % filelog[0].revisions[0].type)
		
		# change type to binary+x
		
		self.source.p4.run_edit('-t+x', file1)
		with open(file1, 'a+') as f:
			print("More content", file=f)
		self.source.p4.run_submit('-d', "Type changed")
		
		self.run_PerforceTransfer()
		
		self.assertCounters(2, 2)
		
		filelog = self.target.p4.run_filelog('//depot/import/file1')
		self.assertEqual(filelog[0].revisions[0].type, 'xbinary', "File type is not xbinary, but %s" % filelog[0].revisions[0].type)
		
		# add ktext file
		
		file2 = os.path.join(inside, "file2")
		with open(file2, 'w') as f:
			print("$Id$", file=f)
			print("$DateTime$", file=f)
		self.source.p4.run_add('-t+k', file2)
		self.source.p4.run_submit('-d', "Ktext added")
		
		self.run_PerforceTransfer()
		
		self.assertCounters(3,3)
		
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].type, 'ktext', "File type is not ktext, but %s" % filelog[0].revisions[0].type)
		verifyResult = self.target.p4.run_verify('-q', '//depot/import/file2')
		self.assertEqual(len(verifyResult), 0) # just to see that ktext gets transferred properly
		
		content = self.target.p4.run_print('//depot/import/file2')[1]
		lines = content.split("\n")
		self.assertEqual(lines[0], '$Id: //depot/import/file2#1 $', "Content does not match : %s" % lines[0])
		
	def testSimpleIntegrate(self):
		self.setupTransfer()
		
		# seed the integration
		
		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
		file1 = os.path.join(inside, "file1")

		with open(file1, 'w') as f:
			print("Test content", file=f)
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', 'File1 added')

		file2 = os.path.join(inside, "file2")
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_submit('-d', 'File1 -> File2')
		
		result = self.run_PerforceTransfer()
		
		# test integration
		
		self.assertCounters(2,2)

		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes), 2, "Target does not have exactly two changes")

		# seed edit/copy
		 		
		self.source.p4.run_edit(file1)
		with open(file1, 'a+') as f:
			print("More content", file=f)
		self.source.p4.run_submit('-d', 'File1 edited')
		
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_resolve('-at')
		self.source.p4.run_submit('-d', 'File1 -> File2 (copy)')
		
		result = self.run_PerforceTransfer()
		
		self.assertCounters(4,4)
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(len(filelog[0].revisions), 2, "Not exactly 2 target revisions")
		self.assertEqual(len(filelog[0].revisions[1].integrations), 1, "Not exactly 1 integration into target")
		self.assertEqual(filelog[0].revisions[0].integrations[0].how, "copy from", "'How' is not copy from")
		
	def testComplexIntegrate(self):
		self.setupTransfer()
		
		# seed the integration
		
		content = """
		Line 1
		Line 2
		Line 3
		"""
		
		content1 = """
		Line 1
		Line 2 - changed
		Line 3
		"""
		
		content2 = """
		Line 1
		Line 2
		Line 3 - changed
		"""
		
		content4 = """
		Line 1
		Line 2 - changed
		Line 3 - differs
		"""

		content5 = """
		Line 1
		Line 2 - changed
		Line 3 - edited
		"""
		
		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
		file1 = os.path.join(inside, "file1")

		with open(file1, 'w') as f:
			print(content, file=f)
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', 'File1 added')

		file2 = os.path.join(inside, "file2")
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_submit('-d', 'File1 -> File2')

		# Prepare merge
		
		self.source.p4.run_edit(file1, file2)
		with open(file1, 'w') as f:
			print(content1, file=f)
		with open(file2, 'w') as f:
			print(content2, file=f)
		self.source.p4.run_submit('-d', "Changed both contents")
		
		# Integrate with merge
		
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_resolve('-am')
		self.source.p4.run_submit('-d', "Merged contents")
		
		contentMerged = self.source.p4.run_print(file2)[1] 
		
		sourceCounter = 4
		targetCounter = 4
		
		self.run_PerforceTransfer()
		self.assertCounters(sourceCounter, targetCounter)
		
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].integrations[0].how, 'merge from', "How is not merge from")
		self.assertEqual(self.target.p4.run_print('//depot/import/file2')[1], contentMerged, "Content not the same")
		
		# Prepare integrate with edit
		
		self.source.p4.run_edit(file1, file2)
		with open(file1, 'w') as f:
			print(content1, file=f)
		self.source.p4.run_submit('-d', "Created a conflict")

		# Integrate with edit
		
		self.source.p4.run_integrate(file1, file2)
		
		class EditResolve(P4.Resolver):
			def resolve(self, mergeData):
				with open(mergeData.result_path, 'w') as f:
					f.write(content5)
					return 'ae'

		self.source.p4.run_resolve(resolver=EditResolve())
		self.source.p4.run_submit('-d', "Merge with edit")
		
		sourceCounter += 2
		targetCounter += 2
		
		self.run_PerforceTransfer()
		self.assertCounters(sourceCounter, targetCounter)

		# Prepare ignore
		
		self.source.p4.run_edit(file1)
		with open(file1, 'a+') as f:
			print("For your eyes only", file=f)
		self.source.p4.run_submit('-d', "Edit source again")
		
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_resolve('-ay') # ignore
		self.source.p4.run_submit('-d', "Ignored change in file1")
		
		sourceCounter += 2
		targetCounter += 2
		
		self.run_PerforceTransfer()
		self.assertCounters(sourceCounter, targetCounter)
		
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].integrations[0].how, 'ignored', "How is not ignored")
		content = self.target.p4.run_print('-a', '//depot/import/file2')
		self.assertEqual(content[1], content[3], "Content of #1 not equal to #2")
		
		# Prepare delete
		
		self.source.p4.run_delete(file1)
		self.source.p4.run_submit('-d', "Delete file 1")
		
		self.source.p4.run_merge(file1, file2) # to trigger resolve
		self.source.p4.run_resolve('-at')
		self.source.p4.run_submit('-d', "Propagated delete")

		sourceCounter += 2
		targetCounter += 2

		self.run_PerforceTransfer()
		self.assertCounters(sourceCounter, targetCounter)
		
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(len(filelog[0].revisions[0].integrations), 1, "No integration for delete")
		self.assertEqual(filelog[0].revisions[0].integrations[0].how, 'delete from', "How is not delete from")
		
		# Prepare re-add
		
		with open(file1, 'w') as f:
			print(content1, file=f)
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', 'File1 re-added')
		
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_submit('-d', "File2 re-added")

		sourceCounter += 2
		targetCounter += 2
		
		self.run_PerforceTransfer()
		self.assertCounters(sourceCounter, targetCounter)
		
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].integrations[0].how, 'branch from' , "How is not branch from")
		
	def testMultipleIntegrate(self):
		self.setupTransfer()

		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
		file1 = os.path.join(inside, "file1")

		with open(file1, 'w') as f:
			print("Some content", file=f)
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', 'File1 added')

		file2 = os.path.join(inside, "file2")
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_submit('-d', 'File1 -> File2')

		file3 = os.path.join(inside, "file3")
		self.source.p4.run_integrate(file2, file3)
		self.source.p4.run_submit('-d', 'File2 -> File3')

		self.run_PerforceTransfer()
		self.assertCounters(3, 3)
		
		filelog1 = self.target.p4.run_filelog('//depot/import/file1')
		filelog2 = self.target.p4.run_filelog('//depot/import/file2')
		filelog3 = self.target.p4.run_filelog('//depot/import/file3')
		
		self.assertEqual(len(filelog1[0].revisions), 1, "Not exactly one file1 revision")
		self.assertEqual(len(filelog2[0].revisions), 1, "Not exactly one file2 revision")
		self.assertEqual(len(filelog3[0].revisions), 1, "Not exactly one file3 revision")

		self.assertEqual(len(filelog1[0].revisions[0].integrations), 1, "Not exactly one file1 integ record")
		self.assertEqual(len(filelog2[0].revisions[0].integrations), 2, "Not exactly two file2 integ records")
		self.assertEqual(len(filelog3[0].revisions[0].integrations), 1, "Not exactly one file3 integ record")

	def testInsideOutside(self):
		self.setupTransfer()

		inside = os.path.join(self.source.client_root, "inside")
		ensureDirectory(inside)
		outside = os.path.join(self.source.client_root, "outside")
		ensureDirectory(outside)
	
		# add from outside, integrate in
		
		file1 = os.path.join(outside, 'file1')
		with open(file1,'w') as f:
			print("Some content", file=f)
		self.source.p4.run_add(file1)
		self.source.p4.run_submit('-d', "Outside file1")
		
		file2 = os.path.join(inside, 'file2')
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_submit('-d', "Integrated from outside to inside")
		
		self.run_PerforceTransfer()
		self.assertCounters(2,1)
		
		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes),1, "Not exactly one change on target")
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].action, "add", "File2 action is not add")
		
		# edit from outside, integrated in
		
		self.source.p4.run_edit(file1)
		with open(file1, 'a+') as f:
			print("More content", file=f)
		self.source.p4.run_submit('-d', "Outside file1 edited")
		
		self.run_PerforceTransfer()
		self.assertCounters(2,1) # counters will not move, no change within the client workspace's scope
		
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_resolve('-at')
		self.source.p4.run_submit('-d', "Copied file1 -> file2")
		
		self.run_PerforceTransfer()
		self.assertCounters(4, 2)

		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes),2, "Not exactly two changes on target")
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].action, "edit", "File2 action is not edit")
		
		# delete from outside, integrate in
		
		self.source.p4.run_delete(file1)
		self.source.p4.run_submit('-d', "File1 deleted")
		
		self.source.p4.run_integrate(file1, file2)
		self.source.p4.run_submit('-d', "File2 deleted from file1")
		
		self.run_PerforceTransfer()
		self.assertCounters(6, 3)
		
		changes = self.target.p4.run_changes()
		self.assertEqual(len(changes),3, "Not exactly three changes on target")
		filelog = self.target.p4.run_filelog('//depot/import/file2')
		self.assertEqual(filelog[0].revisions[0].action, "delete", "File2 action is not delete")
		
if __name__ == '__main__':
	unittest.main()
