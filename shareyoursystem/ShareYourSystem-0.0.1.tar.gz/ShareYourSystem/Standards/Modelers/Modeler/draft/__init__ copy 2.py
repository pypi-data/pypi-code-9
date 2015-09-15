# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Modeler defines the model to be stored in a database like Django or PyTable.
Here are defined the relations between attributes of an instance and their corresponding
types in the databased structures.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Parenter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import copy
from ShareYourSystem.Standards.Classors import Doer
#</ImportSpecificModules>

#<DefineLocals>
AnalyzingColStrsList=[
						'Int',
						'Float',
						'Str'
					]
ModelingJoinStr='__'
ModelingLinkStr='_'
ModelingOrderStr='xx'
#</DefineLocals>

#<DefineFunctions>
def getModeledColWithGetKeyStr(_GetKeyStr):

	#import
	import tables

	#Definition
	global AnalyzingColStrsList

	#Definition
	ModeledColStr=SYS._filter(
		lambda __AnalyzingColStr:
			_GetKeyStr.endswith(__AnalyzingColStr),
			AnalyzingColStrsList
		)[0]

	#Debug
	'''
	print('l 55 getModeledColWithGetKeyStr')
	print('ModeledColStr is ')
	print(ModeledColStr)
	print('')
	'''

	#Get the Col Class
	if ModeledColStr=='Str':
		ModeledColClass=getattr(
							tables,
							'StringCol'
						)
	else:
		ModeledColClass=getattr(
							tables,
							ModeledColStr+'Col'
						)

	#Return
	if ModeledColStr=='Str':
		return ModeledColClass(100)
	else:
		return ModeledColClass() 

def getModelingColumnTupleWithGetKeyStr(_GetKeyStr):
	return (
			_GetKeyStr,
			_GetKeyStr,
			getModeledColWithGetKeyStr(_GetKeyStr)
	)

#</DefineFunctions>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':["model"]
})
class ModelerClass(BaseClass):
	
	def default_init(
					self,
					_ModelKeyStrsList=None,
					_ModelDeriveControllerVariable=None,
					_ModelTagStr="",
					_ModelingDescriptionTuplesList={
						'DefaultValueType':property,
						'PropertyInitVariable':[],
						'PropertyDocStr':'I described variables for storing them in hdf'
					}, 	
					_ModelingMongoBool=True,
					_ModelingHdfBool=False,	
					_ModeledDescriptionKeyStr="",						
					_ModeledDescriptionClassesOrderedDict=None,																
					_ModeledDescriptionClass=None,
					_ModeledMongoDeriveNoderVariable=None,
					_ModeledHdfGroupVariable=None,
					_ModeledMongoTopClientVariable=None,
					_ModeledMongoLocalDatabaseVariable=None,
					_ModeledHdfTopFileVariable=None,
					_ModeledMongoSuffixStr="",
					_ModeledHdfSuffixStr="",
					_ModeledHdfKeyStrsList=None,
					_ModeledMongoKeyStrsList=None,
					_ModeledMongoCollectionsOrderedDict=None,
					_ModeledHdfTablesOrderedDict=None,
					_ModeledMongoKeyStr="", 	
					_ModeledHdfKeyStr="", 
					_ModeledMongoIndexInt=-1, 	
					_ModeledHdfIndexInt=-1, 			
					_ModeledMongoCollection=None, 	
					_ModeledHdfTable=None,  													
					**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_model(self):
		""" """

		#Debug
		self.debug('model start')
		
		#/###################/#
		# Define the ModeledKeyStr 
		#

		if self.ModeledDescriptionKeyStr=='':
			self.ModeledDescriptionKeyStr=self.ModelTagStr

		#/###################/#
		# Mongo Case
		#

		#Check
		if self.ModelingMongoBool:

			#debug
			'''
			self.debug(
					'We model mongo here'
				)
			'''

			#set
			self.ModeledMongoSuffixStr=self.ModelTagStr+'Collection'

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'PymongoneClientVariable',
							'ModeledMongoSuffixStr'
						]
					)
				]
			)
			'''

			#Check
			if self.ModelDeriveControllerVariable.PymongoneClientVariable==None:

				#debug
				'''
				self.debug('We have to pymongo first...')
				'''

				#pymongo
				self.ModelDeriveControllerVariable.pymongo()

			#Link
			self.ModeledMongoTopClientVariable=self.ModelDeriveControllerVariable.PymongoneClientVariable
			
			#Check
			if self.ModeledMongoTopClientVariable!=None:

				#debug
				'''
				self.debug(
							[	
								'Looking for names of collections here',
								('self.',self,[
									'ModeledMongoTopClientVariable'
									]),
							]
						)
				'''

				#set
				self.ModeledMongoDatabaseKeyStr=self.ModelDeriveControllerVariable.ControlModelStr

				#set
				self.ModelDeriveControllerVariable.PymongoingDatabaseKeyStr=self.ModeledMongoDatabaseKeyStr

				#set
				self.ModeledMongoLocalDatabaseVariable=self.ModeledMongoTopClientVariable[
						self.ModeledMongoDatabaseKeyStr
				]

				#debug
				'''
				self.debug(
						[
							('self.',self,[
								'ModeledMongoDatabaseKeyStr',
								'ModeledMongoLocalDatabaseVariable'
								]),
							"id(self.ModeledMongoLocalDatabaseVariable) is "+str(
								id(self.ModeledMongoLocalDatabaseVariable))
						]
					)
				'''

				#set
				self.ModeledMongoLocalDatabaseVariable.__dict__[
					'ParentDerivePymongoer'
				]=self.ModelDeriveControllerVariable

				#alias
				self.ModelDeriveControllerVariable.Database=self.ModeledMongoLocalDatabaseVariable

				#debug
				'''
				self.debug(
							[	
								('self.',self,[
									'ModeledMongoLocalDatabaseVariable'
									]),
								"'ParentDerivePymongoer' in self.ModeledMongoLocalDatabaseVariable.__dict__",
								'ParentDerivePymongoer' in self.ModeledMongoLocalDatabaseVariable.__dict__
							]
						)
				'''

				#Get and sort
				self.ModeledMongoKeyStrsList=map(
					str,
					sorted(
						filter(
								lambda __KeyStr:
								__KeyStr.endswith(
									self.ModeledMongoSuffixStr
								),
								self.ModeledMongoLocalDatabaseVariable.collection_names()
							)
						)
				)
				
				#debug
				'''
				self.debug(
					[	
						('self.',self,[
							'ModeledMongoKeyStrsList'
							])
					]
				)
				'''
				
				#update
				self.ModeledMongoCollectionsOrderedDict.update(
					map(
							lambda __ModeledKeyStr:
							(
								__ModeledKeyStr,
								self.ModeledMongoLocalDatabaseVariable[
									__ModeledKeyStr
								]
							),
							self.ModeledMongoKeyStrsList
						)
				)

				#debug
				'''
				self.debug(("self.",self,[
											'ModeledMongoSuffixStr',
											'ModeledMongoKeyStrsList'
											]))
				'''

			#debug
			'''
			self.debug(
						[
							'ModeledMongoKeyStrsList',
							'ModeledMongoSuffixStr',
							'ModeledMongoKeyStr'
						]
					)
			'''

			#Get the suffix Strs of all the tables and their index
			ModeledMongoList=SYS.unzip(map(
					lambda __StrsList:
					(
						__StrsList[1],
						ModelingOrderStr.join(__StrsList[2:])
					),
					map(
							lambda __ModeledMongoKeyStr:
							__ModeledMongoKeyStr.split(ModelingOrderStr),
							self.ModeledMongoKeyStrsList
						)
				),[0,1]
			)

			#debug
			'''
			self.debug(('vars ',vars(),['ModeledHdfList']))
			'''
			
			#Unpack if it is possible
			if len(ModeledMongoList)>0:

				#Unpack
				[ModeledMongoIndexIntsTuple,ModeledMongoSuffixStrsList]=ModeledMongoList

				#debug
				'''
				self.debug(
							[
								'There are already some tables',
								'ModeledMongoSuffixStrsList is '+str(ModeledMongoSuffixStrsList),
								"self.ModeledMongoSuffixStr is "+str(
									self.ModeledMongoSuffixStr)
							]
						)
				'''

				if self.ModeledMongoSuffixStr not in ModeledMongoSuffixStrsList:

					#Increment the IndexStr
					ModeledMongoIndexInt=max(map(int,ModeledMongoIndexIntsTuple))+1

					#Strify
					ModeledMongoIndexStr=str(ModeledMongoIndexInt)

					#debug
					'''
					self.debug('IndexStr of this new table is '+str(IndexStr))
					'''
					
				else:

					#Get the already setted one
					ModeledMongoIndexStr=self.ModeledMongoKeyStrsList[
							ModeledMongoSuffixStrsList.index(self.ModeledMongoSuffixStr)
						].split(ModelingOrderStr)[1]

					#Intify
					ModeledMongoIndexInt=(int)(ModeledMongoIndexStr)

					#debug
					'''
					self.debug('IndexStr of this not new table is '+str(IndexStr))
					'''

			else:

				#debug
				'''
				self.debug('There are no tables here')
				'''

				#set to empty lists 
				[ModeledMongoIndexIntsTuple,ModeledMongoSuffixStrsList]=[[],[]]

				#Init the list
				ModeledMongoIndexInt=0

				#Strify
				ModeledMongoIndexStr="0"

			#Bind with ModeledHdfKeyStr setting
			self.ModeledMongoKeyStr=ModelingOrderStr+ModeledMongoIndexStr+ModelingOrderStr+self.ModeledMongoSuffixStr

			#set the ModeledInt
			self.ModeledMongoIndexInt=ModeledMongoIndexInt

			#debug
			'''
			self.debug("self.ModeledMongoKeyStr is "+str(self.ModeledMongoKeyStr))
			'''
			
			#debug
			'''
			self.debug(
						[
							'Here we create the collection or get it depending if it is new or not',
							'self.ModeledMongoKeyStr is '+self.ModeledMongoKeyStr,
							'self.ModeledTopFileVariable!=None is '+str(self.ModeledTopFileVariable!=None)
						]
					)
			'''

			#Check
			if self.ModeledMongoKeyStr!="" and self.ModeledMongoLocalDatabaseVariable!=None:

				#debug
				'''
				self.debug(
							[
								('self.',self,[
									'ModeledMongoKeyStr',
									'ModeledMongoKeyStrsList'
									]
								),
								'self.ModeledMongoLocalDatabaseVariable.collection_names() is ',
								str(self.ModeledMongoLocalDatabaseVariable.collection_names())
							]
						)
				'''
				
				#Create the collection if not already
				if self.ModeledMongoKeyStr not in self.ModeledMongoKeyStrsList:

					#debug
					'''
					self.debug(
								[
									'The collection not exists',
								]
							)
					'''

					#Create the collections
					self.ModeledMongoCollection=self.ModeledMongoLocalDatabaseVariable.create_collection(
						self.ModeledMongoKeyStr
					)

					#Append
					self.ModeledMongoKeyStrsList.append(self.ModeledMongoKeyStr)

				else:

					#debug
					'''
					self.debug(
						[
							'The collection exists',
						]
					)
					'''

					#Else just get it 
					self.ModeledMongoCollection=self.ModeledMongoLocalDatabaseVariable[
						self.ModeledMongoKeyStr
					]
					
				#set the in the ModeledMongoCollectionsOrderedDict
				self.ModeledMongoCollectionsOrderedDict[
					self.ModeledMongoKeyStr
				]=self.ModeledMongoCollection

				#debug
				'''
				self.debug("self.ModeledMongoCollectionsOrderedDict is "+str(self.ModeledMongoCollectionsOrderedDict))
				'''
				
			#debug
			'''
			self.debug(
						[
							'Table is done here for mongo...',
							('self.',self,[
								'ModeledMongoCollection',
								'ModeledMongoTopDatabaseVariable'
								]
							)
						]
					)
			'''

		#/###################/#
		# Hdf Case
		#

		#Check
		if self.ModelingHdfBool:

			#/###################/#
			# Define the Description
			#

			#import 
			import tables

			#Definition the DescriptionClass
			class DescriptionClass(tables.IsDescription):

				#Add (just like a unique KEY in mysql...) 
				RowInt=tables.Int64Col()

			#debug
			self.debug(
				[
					'We add descriptions in the description Class',
					('self.',self,['ModelingDescriptionTuplesList'])
				]
			)
			
			#set the cols in the ModelClass
			map(
					lambda __ModelingColumnTuple:
					DescriptionClass.columns.__setitem__(
						__ModelingColumnTuple[1],
						__ModelingColumnTuple[2]
						),
					self.ModelingDescriptionTuplesList
				)

			#Give a name
			DescriptionClass.__name__=SYS.getClassStrWithNameStr(self.ModelTagStr)

			#set the ModelClass
			if self.ModeledDescriptionClassesOrderedDict==None:
				self.ModeledDescriptionClassesOrderedDict=collections.OrderedDict()
			self.ModeledDescriptionClassesOrderedDict[self.ModelTagStr]=DescriptionClass

			#set the ModeledDescriptionClass
			self.ModeledDescriptionClass=DescriptionClass

			#debug
			'''
			self.debug('We tabular for hdf here...')
			'''
			
			#set
			self.ModeledHdfSuffixStr=self.ModelTagStr+'Table'

			#Check
			if self.ModelDeriveControllerVariable.HdformatedFileVariable==None:

				#Check
				if self.ModelDeriveControllerVariable.HdformatingFileKeyStr=='':

					#set
					self.ModelDeriveControllerVariable.HdformatingFileKeyStr=self.ModelDeriveControllerVariable.ControlModelStr+'.hdf5'

				#debug
				'''
				self.debug(
					[
						'We have to hdformat first...',
						'self.ModelDeriveControllerVariable.HdformatingFileKeyStr is ',
						self.ModelDeriveControllerVariable.HdformatingFileKeyStr
					]
				)
				'''

				#Hdformat
				self.ModelDeriveControllerVariable.hdformat()
				
			#Set
			self.ModelDeriveControllerVariable.HdfGroupPathStr=self.ModelDeriveControllerVariable.ControlModelStr

			#Link
			self.ModeledHdfTopFileVariable=self.ModelDeriveControllerVariable.HdformatedFileVariable
			
			#debug
			'''
			self.debug(('self.',self,[
										'ModeledHdfTopFileVariable'
									]))
			'''
			
			#/#################/#
			# Check for all the tables alreday defined here
			#

			#Check
			if self.ModeledHdfTopFileVariable!=None:

				#debug
				'''
				self.debug(
							[	
								'Looking for names of tables here',
								('self.',self,['HdfGroupPathStr'])
							]
						)
				'''

				#Definition Modeled attributes
				self.ModeledHdfGroupVariable=self.ModeledHdfTopFileVariable.getNode(
					self.ModelDeriveControllerVariable.HdfGroupPathStr
				)

				#debug
				'''
				self.debug(
							[
								('looking for tables with the same suffix Str as : '),
								('self.',self,['ModeledHdfSuffixStr'])
							]
						)
				'''

				#Get and sort
				self.ModeledHdfKeyStrsList=sorted(
					filter(
							lambda __KeyStr:
							__KeyStr.endswith(self.ModeledHdfSuffixStr),
							self.ModeledHdfGroupVariable._v_leaves.keys()
						)
				)
				
				self.ModeledHdfTablesOrderedDict.update(
					map(
							lambda __ModeledKeyStr:
							(
								__ModeledKeyStr,
								self.ModeledHdfGroupVariable._f_getChild(
									__ModeledKeyStr
								)
							),
							self.ModeledHdfKeyStrsList
						)
				)

				#debug
				'''
				self.debug(("self.",self,[
											'ModeledHdfSuffixStr',
											'ModeledHdfKeyStrsList'
											]))
				'''	

			#/################/#
			# Refind all the names of the tables
			#

			#debug
			'''
			self.debug(
						('self.',self,[
							'ModeledHdfKeyStrsList',
							'ModeledHdfSuffixStr',
							'ModeledHdfKeyStr'
						])
					)
			'''

			#Get the suffix Strs of all the tables and their index
			ModeledHdfList=SYS.unzip(map(
					lambda __StrsList:
					(
						__StrsList[1],
						ModelingOrderStr.join(__StrsList[2:])
					),
					map(
							lambda __ModeledHdfKeyStr:
							__ModeledHdfKeyStr.split(ModelingOrderStr),
							self.ModeledHdfKeyStrsList
						)
				),[0,1]
			)

			#debug
			self.debug(('vars ',vars(),['ModeledHdfList']))
			
			#/##################/#
			# Find if there are already some tables here and deduce the index of the table
			#

			#Unpack if it is possible
			if len(ModeledHdfList)>0:

				#Unpack
				[ModeledHdfIndexIntsTuple,ModeledHdfSuffixStrsList]=ModeledHdfList

				#debug
				'''
				self.debug(
							[
								'There are already some tables',
								'ModeledHdfSuffixStrsList is '+str(ModeledHdfSuffixStrsList),
								"self.ModeledHdfSuffixStr is "+str(
									self.ModeledHdfSuffixStr)
							]
						)
				'''

				if self.ModeledHdfSuffixStr not in ModeledHdfSuffixStrsList:

					#Increment the IndexStr
					ModeledHdfIndexInt=max(map(int,ModeledHdfIndexIntsTuple))+1

					#Strify
					ModeledHdfIndexStr=str(ModeledHdfIndexInt)

					#debug
					'''
					self.debug('IndexStr of this new table is '+str(IndexStr))
					'''
					
				else:

					#Get the already setted one
					ModeledHdfIndexStr=self.ModeledHdfKeyStrsList[
							ModeledHdfSuffixStrsList.index(self.ModeledHdfSuffixStr)
						].split(ModelingOrderStr)[1]

					#Intify
					ModeledHdfIndexInt=(int)(ModeledHdfIndexStr)

					#debug
					'''
					self.debug('IndexStr of this not new table is '+str(IndexStr))
					'''

			else:

				#debug
				'''
				self.debug('There are no tables here')
				'''

				#set to empty lists 
				[ModeledHdfIndexIntsTuple,ModeledHdfSuffixStrsList]=[[],[]]

				#Init the list
				ModeledHdfIndexInt=0

				#Strify
				ModeledHdfIndexStr="0"

			#/##################/#
			# set the table key str
			#

			#debug
			self.debug(
					[
						'We set the table key str',
						('self.',self,['ModeledHdfKeyStr'])
					]
				)

			#Bind with ModeledHdfKeyStr setting
			self.ModeledHdfKeyStr=ModelingOrderStr+ModeledHdfIndexStr+ModelingOrderStr+self.ModeledHdfSuffixStr

			#set the ModeledInt
			self.ModeledHdfIndexInt=ModeledHdfIndexInt

			#debug
			'''
			self.debug("self.ModeledHdfKeyStr is "+str(self.ModeledHdfKeyStr))
			'''
			
			#debug
			'''
			self.debug(
						[
							'Here we create the table or get it depending if it is new or not',
							('self.',self,[
								'ModeledHdfKeyStr',
								'ModeledHdfTopFileVariable'
								])
						]
					)
			'''
			
			#Check
			if self.ModeledHdfKeyStr!="" and self.ModeledHdfTopFileVariable!=None:

				#debug
				'''
				self.debug(
							[
								('self.',self,[
									'ModeledHdfKeyStr',
									'ModeledHdfKeyStrsList'
								])
							]
						)
				'''
				
				#Create the Table if not already
				if self.ModeledHdfKeyStr not in self.ModeledHdfKeyStrsList:

					#debug
					'''
					self.debug(
								[
									'The table not exists',
								]
							)
					'''

					#Create the Table in the hdf5
					self.ModeledHdfTable=self.ModeledHdfTopFileVariable.create_table(
						self.ModeledHdfGroupVariable,
						self.ModeledHdfKeyStr,
						self.ModeledDescriptionClass,
						self.ModeledDescriptionClass.__doc__ 
						if self.ModeledDescriptionClass.__doc__!=None 
						else "This is the "+self.ModeledDescriptionClass.__name__
					)

					#Append
					self.ModeledHdfKeyStrsList.append(
						self.ModeledHdfKeyStr
					)

				else:

					#debug
					'''
					self.debug(
									[
										'The table exists',
										"self.ModeledGroupVariable is "+str(self.ModeledGroupVariable)
									]
								)
					'''

					#Else just get it 
					self.ModeledHdfTable=self.ModeledHdfGroupVariable._f_getChild(
						self.ModeledHdfKeyStr
					)

				#set the in the TablesOrderedDict
				self.ModeledHdfTablesOrderedDict[
					self.ModeledHdfKeyStr
				]=self.ModeledHdfTable

				#debug
				'''
				self.debug("self.ModeledHdfTablesOrderedDict is "+str(
					self.ModeledHdfTablesOrderedDict))
				'''
				
			#debug
			'''
			self.debug(
						[
							'Table is done here for hdf...',
							('self.',self,[
								'ModeledHdfTable',
								'ModeledHdfTopFileVariable'
								]
							)
						]
					)
			'''


	def propertize_setParentKeyStr(self,_SettingValueVariable):

		#call the parent base
		BaseClass.propertize_setParentKeyStr(self,_SettingValueVariable)

		#debug
		'''
		self.debug(
			[
				'We know the ParentKeyStr',
				'We model here',
			]
		)
		'''

		#/#################/#
		# Give some things from the controller
		#

		#get the parent-parent Teamer
		if self.ParentDeriveTeamerVariable!=None:
			if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable!=None:
				self.ModelDeriveControllerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#Link set
		self.ModelTagStr=self.ManagementTagStr+'Model'

		#debug
		'''
		self.debug(
				[
					'We have setted the ModelDeriveControllerVariable',
					('self.',self,[
						'ModelDeriveControllerVariable',
						'ModelTagStr'
					])
				]
			)
		'''

		#model
		self.model()


	def propertize_setModelingDescriptionTuplesList(self,_SettingValueVariable):

		#set
		self._ModelingDescriptionTuplesList=_SettingValueVariable

		#check
		if self.ModelKeyStrsList==None:
			self.ModelKeyStrsList=[]

		#extend
		self.ModelKeyStrsList.extend(
			SYS.unzip(
				_SettingValueVariable,
				[0]
			)
		)

		#/###################/#
		# Check if it is a hdf or mongo model
		#

		#debug
		'''
		self.debug(
			[
				('self.',self,['ModelingDescriptionTuplesList'])
			]
		)
		'''

		#Check
		if len(self.ModelingDescriptionTuplesList)>0:
			self.ModelingHdfBool=True
			self.ModelingMongoBool=False
		else:
			self.ModelingHdfBool=False
			self.ModelingMongoBool=True

#</DefineClass>


#</DefinePrint>
ModelerClass.PrintingClassSkipKeyStrsList.extend(
	[
		#'ModelKeyStrsList',	
		'ModelingDescriptionTuplesList', 
		'_ModelingDescriptionTuplesList', 
		'ModelingMongoBool',
		'ModelingHdfBool',							
		'ModeledDescriptionClassesOrderedDict',																
		#'ModeledDescriptionClass', 													
		'ModelDeriveControllerVariable',
		'ModeledMongoDeriveNoderVariable',	
		'ModeledHdfGroupVariable', 
		'ModeledHdfTopFileVariable',
		'ModeledMongoTopClientVariable',
		'ModeledMongoLocalDatabaseVariable',									
		'ModeledMongoSuffixStr',
		'ModeledHdfSuffixStr',																
		'ModeledMongoKeyStrsList',
		'ModeledHdfKeyStrsList', 	
		'ModeledMongoCollectionsOrderedDict',												
		'ModeledHdfTablesOrderedDict',
		'ModeledMongoKeyStr', 	
		'ModeledHdfKeyStr', 
		'ModeledMongoIndexInt', 	
		'ModeledHdfIndexInt', 			
		'ModeledMongoCollection', 	
		'ModeledHdfTable' 
	]
)
#<DefinePrint>
