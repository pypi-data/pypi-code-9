# -*- coding: utf-8 -*-
"""

<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>

Joiner instances helps to insert in joined databases, get the corresponding
RetrieveIndexIntsLists if it was already inserted, and then insert locally
depending if it is a new row compared to all JoinedRetrieveIndexIntsListsList

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Findoer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Joiner','Join','Joining','Joined')
#</DefineAugmentation>

#<ImportSpecificModules>
Featurer=BaseModule
import collections
from ShareYourSystem.Standards.Modelers import Modeler
from ShareYourSystem.Standards.Controllers import Controller
#</ImportSpecificModules>

#<DefineLocals>
JoinStr='__'
JoinDeepStr='/'
JoinTeamPrefixStr='Jonct'
JoinColumnPrefixStr='_j_'
JoinColumnSuffixStr='List'
#JoinColumnSuffixStr="RetrieveIndexIntsList"
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':[
		'model',
		'row',
		'join',
		'insert'
	]
})
class JoinerClass(BaseClass):
	
	def default_init(self,
						_JoiningRowBool=False,
						_JoinedOutDeriveConnectersList=None,
						_JoinedOutDeriveJoinersList=None,
						_JoinedRetrieveIndexIntsListGetStrsList=None,
						_JoinedModelMongoIndexIntsList=None,
						_JoinedModelHdfIndexIntsList=None,
						_JoinedRowMongoIndexIntsList=None,
						_JoinedRowHdfIndexIntsList=None,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
		
	def do_join(	
				self
			):


		#debug
		'''
		self.debug(
				[
					'We join here',
					'Check if there are joined tables'
				]
			)
		'''
		
		#Check
		if JoinTeamPrefixStr+'ions' in self.TeamDict:

			#/################/#
			# Get the post derive pointing parenters and make them point
			#	

			#set
			self.JoinedOutDeriveConnectersList=self.TeamDict[
				JoinTeamPrefixStr+'ions'
			].ManagementDict.values()

			#debug
			'''
			self.debug(
					[
						'We have getted the post derive parenters',
						('self.',self,['JoinedOutDeriveConnectersList'])
					]
				)
			'''

			#/################/#
			# get the JoinedRetrieveIndexIntsListGetStrs, and the ModeledIndexInts
			#

			self.JoinedRetrieveIndexIntsListGetStrsList=map(
					lambda __JoinedPostDerivePointer:
					JoinColumnPrefixStr+''.join(
						[
							__JoinedPostDerivePointer.ManagementTagStr.replace('/','_'),
						]
					)+JoinColumnSuffixStr,
					self.JoinedOutDeriveConnectersList
				)

			#debug
			'''
			self.debug(
					[
						'We have setted the JoinedRetrieveIndexIntsListGetStrsList',
						('self.',self,['JoinedRetrieveIndexIntsListGetStrsList']),
						'Now get the model index int',
						('self.',self,[
								'ModelMongoBool',
								'ModelHdfBool'
							])
					]
				)
			'''

			#/################/#
			# get the pointed Joiners 
			#

			#set
			self.JoinedOutDeriveJoinersList=map(
					lambda __JoinedOutDerivePointer:
					__JoinedOutDerivePointer.ConnectedToVariable,
					self.JoinedOutDeriveConnectersList
				)

			#debug
			'''
			self.debug(
					[
						'We have getted the out joiners',
						#'self.TeamDict[JoinTeamTagStr].ManagementDict.keys() is',
						#str(self.TeamDict[JoinTeamTagStr].ManagementDict.keys()),
						('self.',self,['JoinedOutDeriveJoinersList']),
						'Now get the model index int',
						('self.',self,[
								'ModelMongoBool',
								'ModelHdfBool'
							])
					]
				)
			'''

			#Check
			if self.ModelMongoBool:

				#set
				self.JoinedModelMongoIndexIntsList=map(
							lambda __JoinedOutDeriveJoiner:
							__JoinedOutDeriveJoiner.ModeledMongoIndexInt,
							self.JoinedOutDeriveJoinersList
						)

			#Check
			if self.ModelHdfBool:

				#debug
				'''
				self.debug(
						[
							'We get the model hdf',
							('self.',self,['JoinedOutDeriveJoinersList'])
						]
					)
				'''

				#set
				self.JoinedModelHdfIndexIntsList=map(
							lambda __JoinedOutDeriveJoiner:
							__JoinedOutDeriveJoiner.ModeledHdfIndexInt,
							self.JoinedOutDeriveJoinersList
						)

			#debug
			'''
			self.debug(
					[
						'We have getted the JoinedModelMongoOrHdfIndexIntsList',
						('self.',self,[
							'JoinedModelMongoIndexIntsList',
							'JoinedModelHdfIndexIntsList'
						])
					]
				)
			'''

			#/################/#
			# Init them into the controller 
			#

			#debug
			'''
			self.debug(
					[
						'We set this retrieve tuples into the controller',
						('self.',self,[
							'JoinedModelMongoIndexIntsList',
							'JoinedModelHdfIndexIntsList',
							'ModeledParentControllerDeriveModelerVariable'
						])
					]
				)
			'''
			
			#Check
			if self.ModelMongoBool:

				#map
				map(
						lambda __JoinedModelMongoIndexInt,__JoinedRetrieveIndexIntsListGetStr:
						setattr(
							self.ModeledParentControllerDeriveModelerVariable,
							__JoinedRetrieveIndexIntsListGetStr,
							[
								__JoinedModelMongoIndexInt,
								-1
							]
						),
						self.JoinedModelMongoIndexIntsList,
						self.JoinedRetrieveIndexIntsListGetStrsList
					)

			#Check
			if self.ModelHdfBool:

				#map
				map(
						lambda __JoinedModelHdfIndexInt,__JoinedRetrieveIndexIntsListGetStr:
						setattr(
							self.ModeledParentControllerDeriveModelerVariable,
							__JoinedRetrieveIndexIntsListGetStr,
							[
								__JoinedModelHdfIndexInt,
								-1
							]
						),
						self.JoinedModelHdfIndexIntsList,
						self.JoinedRetrieveIndexIntsListGetStrsList
					)
			

			#debug
			'''
			self.debug(
					[
						'Ok we have initiated the retrieve tuples
					]
				)
			'''

	def mimic_model(self):
		
		#/################/#
		# Need to reset first the parent...
		#

		#debug
		'''
		self.debug(
				[
					'We join model here',
					('self.',self,['StructureTopDeriveStructurerRigidVariable'])
				]
			)
		'''

		#set
		if self.ParentDeriveTeamerVariable!=None:
			self.ModeledParentControllerDeriveModelerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
		else:
			self.ModeledParentControllerDeriveModelerVariable=self

		#set
		self.ModeledTopControllerDeriveModelerVariable=self.StructureTopDeriveStructurerRigidVariable

		#debug
		'''
		self.debug(
			[
				('self.',self,[
					#'ModeledParentControllerDeriveModelerVariable',
					#'ModeledTopControllerDeriveModelerVariable'
				]),
				'Recheck for hdf or mongo',
				'self.ModeledParentControllerDeriveModelerVariable.HdformatingFileKeyStr is ',
				self.ModeledParentControllerDeriveModelerVariable.HdformatingFileKeyStr
			]
		)
		'''


		#Check
		if self.ModeledParentControllerDeriveModelerVariable.HdformatingFileKeyStr!="":

			#set
			self.ModelMongoBool=True	
			self.ModelHdfBool=True		

		#/################/#
		# Join first
		#

		#debug
		'''
		self.debug(
				'We join now'
			)
		'''

		#join
		self.join()

		#/################/#
		# Add to the ModelKeyStrs the join attributes
		#

		#debug
		'''
		self.debug(
			[
				'Add in the  ModelKeyStrs',
				('self.',self,['ModelKeyStrsList'])
			]
		)
		'''

		#extend
		self._ModelKeyStrsList=self.JoinedRetrieveIndexIntsListGetStrsList+self._ModelKeyStrsList
		
		#debug
		'''
		self.debug(
			[
				'Now',
				('self.',self,[
					'ModelKeyStrsList',
					'ModelHdfBool'
				])
			]
		)
		'''
		
		#Check
		if self.ModelHdfBool:

			#import 
			import tables

			#debug
			'''
			self.debug(
				[
					'We add  the join items in the description',
					('self.',self,['ModelingDescriptionTuplesList'])
				]
			)
			'''

			#add
			self._ModelingDescriptionTuplesList=map(
				lambda __JoinedRetrieveIndexIntsListGetStr,__JoinedRetrieveIndexIntsListColumnStr:
				(
					__JoinedRetrieveIndexIntsListGetStr,
					__JoinedRetrieveIndexIntsListColumnStr,
					tables.Int64Col(shape=2)
				),
				self.JoinedRetrieveIndexIntsListGetStrsList,
				self.JoinedRetrieveIndexIntsListGetStrsList
			)+self._ModelingDescriptionTuplesList

			#debug
			'''
			self.debug(
						[	
							'Now',
							('self.',self,['ModelingDescriptionTuplesList']),
						]
					)
			'''

		#/################/#
		# Base method
		#

		#debug
		'''
		self.debug(
				[
					'We call the base model method',
					('self.',self,[
							'ModelMongoBool',
							'ModelHdfBool'
						])
				]
			)
		'''

		#call base method
		BaseClass.model(self)

	def mimic_row(self):

		#/###################/#
		# Check if we have to make row first the joined models
		# (in a insert call it is already done)

		#Check
		if self.JoiningRowBool:

			#debug
			'''
			self.debug(
						[
							"We make the children row if it wasn\'t yet",
							'We get their RowedMongoOrHdfIndexInt',
							('self.',self,['JoinedOutDeriveJoinersList'])
						]
					)
			'''

			#set
			self.JoinedRowMongoIndexIntsList=map(
						lambda __JoinedOutDeriveJoiner:
						__JoinedOutDeriveJoiner.row(),
						self.JoinedOutDeriveJoinersList
					)

		#Check
		if self.ModelMongoBool:

			#set
			self.JoinedRowMongoIndexIntsList=map(
						lambda __JoinedOutDeriveJoiner:
						__JoinedOutDeriveJoiner.RowedMongoIndexInt,
						self.JoinedOutDeriveJoinersList
					)

		#Check
		if self.ModelHdfBool:

			#set
			self.JoinedRowHdfIndexIntsList=map(
						lambda __JoinedOutDeriveJoiner:
						__JoinedOutDeriveJoiner.RowedHdfIndexInt,
						self.JoinedOutDeriveJoinersList
					)

		
		#debug
		'''
		self.debug(
			[
				'Ok the out models have rowed',
				('self.',self,[
							'JoinedRowMongoIndexIntsList',
							'JoinedRowHdfIndexIntsList'
						]),
				'Now we set in the Controller this values'
			]
		)
		'''

		#Check
		if self.ModelMongoBool:

			#set the modeled int in the retrieve tuples
			map(
					lambda __JoinedRetrieveIndexIntsListGetStr,__JoinedInsertIndexInt:
					getattr(
						self.ModeledParentControllerDeriveModelerVariable,
						__JoinedRetrieveIndexIntsListGetStr
						).__setitem__(
							1,
							__JoinedInsertIndexInt
					),
					self.JoinedRetrieveIndexIntsListGetStrsList,
					self.JoinedRowMongoIndexIntsList
				)

		if self.ModelHdfBool:

			#set the modeled int in the retrieve tuples
			map(
					lambda __JoinedRetrieveIndexIntsListGetStr,__JoinedInsertIndexInt:
					getattr(
						self.ModeledParentControllerDeriveModelerVariable,
						__JoinedRetrieveIndexIntsListGetStr
						).__setitem__(
							1,
							__JoinedInsertIndexInt
					),
					self.JoinedRetrieveIndexIntsListGetStrsList,
					self.JoinedRowHdfIndexIntsList
				)

		#debug
		'''
		self.debug([
						('Before updating the RowingKeyStrsList'),
						#('self.',self,['NodePointDeriveNoder'])
						('model first to set the ModeledGetStrToColumStr')
					]
				)
		'''

		#Model first to set the ModeledGetStrToColumStr
		#self.model()

		#Add in the RowingKeyStrsList
		#self.RowingKeyStrsList=self.JoinedRetrieveIndexIntsListGetStrsList+self.RowingKeyStrsList

		#debug
		'''
		self.debug('Now row with the BaseClass')
		'''

		#row then
		BaseClass.row(self)

		#debug
		'''
		self.debug('Ok row is over for joining')
		'''

	def mimic_insert(self,**_KwargVariablesDict):

		#/####################/#
		# We make insert the out joins models
		#

		#debug
		self.debug(
					[
						'First make insert the out models',
						('self.',self,['JoinedOutDeriveConnectersList'])
					]
				)
		
		#Insert the post joined databases
		map(
			lambda __JoinedOutDeriveJoiner:
			__JoinedOutDeriveJoiner.insert(**{'JoiningRowBool':False}),
			self.JoinedOutDeriveJoinersList
		)

		#/####################/#
		# We make insert the out joins models
		#

		#debug
		'''
		self.debug(
			[
				'Now we can insert here',
				'we call the base method'
			]
		)
		'''

		#insert then
		BaseClass.insert(self)

		#/####################/#
		# We setSwitch insert the out 
		#

		#debug
		'''
		self.debug(
					[
						'self.getSwitch("row") is ',
						SYS.indent(self.getSwitch("row")),
						'setSwitch insert the out ',
						('self.',self,['JoinedOutDeriveConnectersList'])
					]
				)
		'''

		#Insert the post joined databases
		map(
			lambda __JoinedOutDeriveJoiner:
			__JoinedOutDeriveJoiner.setSwitch('insert'),
			self.JoinedOutDeriveJoinersList
		)

	def mimic_retrieve(self):

		#debug
		'''
		self.debug(('self.',self,['RetrievingIndexesList']))
		'''

		#retrieve first
		BaseClass.retrieve(self)

		#Retrieve in the joined databases
		JoinedInsertIndexIntsList=map(
					lambda __JoinedRetrieveIndexIntsListGetStr,__JoinedPostDeriveJoiner:
					__JoinedPostDeriveJoiner.retrieve(
						getattr(
							self.ModeledParentControllerDeriveModelerVariable,
							__JoinedRetrieveIndexIntsListGetStr
						)
					),
					self.JoinedRetrieveIndexIntsListGetStrsList,
					self.JoinedCatchDeriveJoinersList
				)

		#Check
		if self.JoiningDatabaseStr=='mongo':
			self.JoinedRowMongoIndexIntsList=JoinedInsertIndexIntsList
		elif self.JoiningDatabaseStr=='hdf':
			self.JoinedRowHdfIndexIntsList=JoinedInsertIndexIntsList

	def mimic_find(self):

		#debug
		'''
		self.debug(('self.',self,['FindingWhereTuplesList']))
		'''

		#
		if self.JoiningFindBeforeBool:

			#Find in the joined databases
			JoinedFindFilterRowDictsListsList=map(
					lambda __JoinedPostDeriveJoiner:
					__JoinedPostDeriveJoiner.find(
						).FoundFilterRowDictsList,
					self.JoinedCatchDeriveJoinersList
				)

			#debug
			'''
			self.debug('JoinedFindFilterRowDictsListsList is '+str(JoinedFindFilterRowDictsListsList))
			'''

			#Just keep the retrieve lists
			JoinedFindFilterRetrieveListsList=map(
						lambda __JoinedFindFilterRowDictsList:
						map(
								lambda __JoinedFindFilterRowDict:
								[
									__JoinedFindFilterRowDict['ModeledInt']
									if 'ModeledInt' in __JoinedFindFilterRowDict else 0,
									__JoinedFindFilterRowDict['RowInt']
								],
								__JoinedFindFilterRowDictsList
							),
						JoinedFindFilterRowDictsListsList
			)

			#debug
			'''
			self.debug('JoinedFindFilterRetrieveListsList is '+str(JoinedFindFilterRetrieveListsList))
			'''

			#Map
			JoinedFindingWhereTuplesList=map(
					lambda __JoinedRetrieveIndexIntsListColumnStr,__JoinedFindFilterRetrieveList:
					(
						__JoinedRetrieveIndexIntsListColumnStr,
						(
							SYS.getIsInListBool,
							__JoinedFindFilterRetrieveList
						)
					),
					self.JoinedRetrieveIndexIntsListColumnStrsList,
					JoinedFindFilterRetrieveListsList
				)

			#debug
			'''
			self.debug('JoinedFindingWhereTuplesList is '+str(JoinedFindingWhereTuplesList))
			'''

			#Add to the finding condition tuples
			self.FindingWhereTuplesList+=JoinedFindingWhereTuplesList

			#Call the parent method
			Featurer.FeaturerClass.find(self)

		else:
			
			#Call the parent method
			BaseClass.find(self).FoundFilterRowDictsList
#</DefineClass>

#<DefineLocals>
Modeler.ModelersStructurerClass.ManagingValueClass=JoinerClass
JoinerClass.StructureConnectPrefixStrsList=[JoinTeamPrefixStr]
#<DefineLocals>

#</DefinePrint>
JoinerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'JoiningRowBool',
		'JoinedOutDeriveConnectersList',
		'JoinedOutDeriveJoinersList',
		'JoinedRetrieveIndexIntsListGetStrsList',
		'JoinedModelMongoIndexIntsList',
		'JoinedModelHdfIndexIntsList',
		'JoinedRowMongoIndexIntsList',
		'JoinedRowHdfIndexIntsList'
	]
)
#<DefinePrint>
