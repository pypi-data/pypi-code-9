# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


An Pymongoer 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Numscipyer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import os
#</ImportSpecificModules>

#<DefineFunctions>
def getPrintManagerItemTuple(_ManagerItemTuple):

	#Debug
	'''
	print('Pymongoer l 31')
	print('_ManagerItemTuple is ')
	print(_ManagerItemTuple)
	print('')
	'''
	
	#filter
	PrintCollectionList=filter(
		lambda __PymongoviewDict:
		len(__PymongoviewDict)>0,
		SYS.filterNone(
				map(
					lambda __NoderItemTuple:
					__NoderItemTuple[1].pymongoview()
					if hasattr(
							__NoderItemTuple[1],
							'pymongoview'
						) 
					else None,
					_ManagerItemTuple[1].ManagementDict.items()
				)
			)
	)


	#Debug
	'''
	print('PrintCollectionList is ')
	print(PrintCollectionList)
	print('')
	'''

	#Check
	if len(PrintCollectionList)>0:
		return (
			_ManagerItemTuple[0],
			PrintCollectionList
		)
	else:
		return None

def getPrintDatabaseDict(_Database):

	#map
	PrintDatabaseOrderedDictDict=collections.OrderedDict(
		SYS.filterNone
		(
			map(
				lambda __CollectionStr:
				(
					__CollectionStr,
					list(_Database[__CollectionStr].find())
				)
				if __CollectionStr not in ['system.indexes']
				else None,
				_Database.collection_names()
			)
		)
	)

	#Debug
	'''
	print('_Database is ')
	print(_Database)
	print('id(_Database) is')
	print(id(_Database))
	print("'ParentDerivePymongoer' in _Database.__dict__")
	print('ParentDerivePymongoer' in _Database.__dict__)
	print('')
	'''
	
	#Get the childs database dicts
	if 'ParentDerivePymongoer' in _Database.__dict__:

		#Debug
		'''
		print('_Database.ParentDerivePymongoer is '+SYS._str(_Database.__dict__[
			'ParentDerivePymongoer']))
		print('')
		'''

		#update
		PrintDatabaseOrderedDictDict.update(
			collections.OrderedDict(
				filter(
					lambda __ItemTuple:
					len(__ItemTuple[1])>0,
					SYS.filterNone(	
						map(
							lambda __ManagerItemTuple:
							getPrintManagerItemTuple(__ManagerItemTuple),
							_Database.__dict__[
								'ParentDerivePymongoer'
							].TeamDict.items()
						)
					)
				)
			)
		)

	#return 
	return {_Database._Database__name:PrintDatabaseOrderedDictDict}


#</DefineFunctions>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['pymongo']
})
class PymongoerClass(BaseClass):
	
	def default_init(self,		
			_PymongoingUrlStr='mongodb://localhost:27017/',
			_PymongoingDatabaseStr="",
			_PymongoingKillBool=True,
			_PymongoneFolderPathStr="",
			_PymongoneClientVariable=None,
			_PymongoneDatabaseVariable=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_pymongo(self):

		#debug
		'''
		self.debug(('self.',self,[
							'PymongoingUrlStr'
								]))
		'''

		#folder
		self.folder()

		#import
		'''
		self.debug('import pymongo')
		'''

		#kill all a possible old mongod process
		if self.PymongoingKillBool:

			#status
			PymongoneIdStr=SYS.status(
							'mongod'
						)

			#debug
			'''
			self.debug('PymongoneIdStr is '+PymongoneIdStr)
			'''

			#Check
			if PymongoneIdStr!="":
	
				#kill
				os.popen(
					'kill '+PymongoneIdStr
				)

		#connect
		try:

			#import
			'''
			self.debug('import pymongo')
			'''

			#import
			from pymongo import MongoClient

			#debug
			'''
			self.debug('try to connect to MongoClient')
			'''

			#init
			self.PymongoneClientVariable=MongoClient(self.PymongoingUrlStr)
			
		except:

			#debug
			'''
			self.debug('No connection maybe to pymongo')
			'''

			#set
			self.PymongoneFolderPathStr=self.FolderingPathVariable+'data/db/'

			#Check
			if os.path.isdir(self.PymongoneFolderPathStr)==False:
				os.popen('mkdir '+self.FolderingPathVariable+'data')
				os.popen('mkdir '+self.FolderingPathVariable+'data/db')

			#popen
			self.process(
					'/usr/local/bin/mongod --dbpath '+self.PymongoneFolderPathStr,
					True
				)
	
			#debug
			'''
			self.debug(
				('self.',self,['ProcessedPopenVariable'])
			)
			'''

			#wait for connect
			import time
			PymongoneConnectBool=False
			PymongoneCountInt=0
			while PymongoneConnectBool==False and PymongoneCountInt<5:

				try:

					#connect
					self.PymongoneClientVariable=MongoClient(self.PymongoingUrlStr)

					#Check
					if self.PymongoneClientVariable!=None:
						PymongoneConnectBool=True

				except:

					#debug
					'''
					self.debug(
						[
							'Connection to MongoClient failed at the PymongoneCountInt='+str(
								PymongoneCountInt),
							('self.',self,['PymongoneClientVariable'])
						]
					)
					'''

					#say that it is not setted
					PymongoneConnectBool=False
					PymongoneCountInt+=1
					time.sleep(0.2)


			#debug
			'''
			self.debug(
				[
					'after connection',
					('self.',self,['PymongoneClientVariable'])
				]
			)
			'''
			
	def pymongoview(self,_DatabaseKeyStr=""):

		#debug
		'''
		self.debug(
			[
				('self.',self,[
								'PymongoneClientVariable',
								'PymongoingDatabaseKeyStr'
							]),
				'self.PymongoneClientVariable.database_names is \n',
				self.PymongoneClientVariable.database_names()
			]
		)
		'''

		#debug
		'''
		self.debug('_DatabaseKeyStr is '+_DatabaseKeyStr)
		'''

		#init
		Database=None

		#Check
		if _DatabaseKeyStr!='':

			#_DatabaseKeyStr=self.getDatabaseKeyStr()
			Database=self.PymongoneClientVariable[
							_DatabaseKeyStr
						]
		else:

			#Check
			if hasattr(self,'Database'):
				#get the local one
				Database=self.Database

		#Check
		if Database!=None:

			#debug
			'''
			self.debug(
				[
					'_DatabaseKeyStr is '+_DatabaseKeyStr,
					"_DatabaseKeyStr in self.PymongoneClientVariable.database_names()",
					_DatabaseKeyStr in self.PymongoneClientVariable.database_names(),
					'self.PymongoneClientVariable.__dict__.keys() is ',
					str(self.PymongoneClientVariable.__dict__.keys())
				]
			)
			'''

			#return
			return getPrintDatabaseDict(
							Database
						)

		else:

			#return empty
			return {}
		
#</DefineClass>

#</DefinePrint>
PymongoerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PymongoingUrlStr',
		'PymongoingDatabaseStr',
		'PymongoingKillBool',
		'PymongoneFolderPathStr',
		'PymongoneClientVariable',
		'PymongoneDatabaseVariable'
	]
)
#<DefinePrint>