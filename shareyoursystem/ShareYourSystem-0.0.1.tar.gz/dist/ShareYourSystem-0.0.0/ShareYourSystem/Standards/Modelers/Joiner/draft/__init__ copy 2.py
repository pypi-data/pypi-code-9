# -*- coding: utf-8 -*-
"""

<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>

Joiner instances helps to insert in joined databases, get the corresponding
RetrieveIndexesLists if it was already inserted, and then insert locally
depending if it is a new row compared to all JoinedRetrieveIndexesListsList

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Findoer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
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
						_JoiningCollectionStr="",
						_JoiningCatchStr="",
						_JoiningAttentionStr="",
						_JoiningFindBeforeBool=True,
						_JoiningDatabaseStr='mongo',
						_JoinedAttentionCollectionOrderedDict=None,
						_JoinedCatchCollectionOrderedDict=None,
						_JoinedCatchDeriveJoinersList=None,
						_JoinedRetrieveIndexesListGetStrsList=None,
						_JoinedRetrieveIndexesListColumnStrsList=None,
						_JoinedMongoInsertIndexIntsList=None,
						_JoinedHdfInsertIndexIntsList=None,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
		
	def do_join(	
				self
			):

		#/################/#
		# Build the join items
		#

		#debug
		self.debug(
				[
					'We join here'
				]
			)

		#Check
		if self.JoiningCollectionStr=="":
			self.JoiningCollectionStr=self.NetworkCollectionStr
		if self.JoiningCatchStr=="":
			self.JoiningCatchStr=self.NetworkCatchStr
		if self.JoiningAttentionStr=="":
			self.JoiningAttentionStr=self.NetworkAttentionStr

		#debug
		'''
		self.debug(
					('self.',self,[
									'JoiningCollectionStr',
									'JoiningCatchStr',
									'JoiningAttentionStr'
								])
				)
		'''
		#set
		JoinedAttentionCollectionOrderedSetTagStr=self.JoiningAttentionStr+self.JoiningCollectionStr+"CollectionOrderedDict"

		#check
		if hasattr(
			self,
			JoinedAttentionCollectionOrderedSetTagStr
		):

			#get
			self.JoinedAttentionCollectionOrderedDict=getattr(
				self,
				JoinedAttentionCollectionOrderedSetTagStr
			)

		#set
		JoinedCatchCollectionOrderedSetTagStr=self.JoiningCatchStr+self.JoiningCollectionStr+"CollectionOrderedDict"

		#check
		if hasattr(self,JoinedCatchCollectionOrderedSetTagStr):

			#get
			self.JoinedCatchCollectionOrderedDict=getattr(
				self,
				JoinedCatchCollectionOrderedSetTagStr
			)

			#model and link all the catched joiners
			self.JoinedCatchDeriveJoinersList=map(
					lambda __JoinedCatchDeriveJoiner:
					#__JoinedCatchDeriveJoiner.__setitem__(
					#	'InsertIsBool',
					#	False
					#).CatchToPointVariable.model(
					#),
					__JoinedCatchDeriveJoiner.CatchToPointVariable.model(),
					self.JoinedCatchCollectionOrderedDict.values()
				)

			#debug
			'''
			self.debug(('self.',self,['JoinedCatchCollectionOrderedDict']))
			'''

			#set
			self.JoinedRetrieveIndexesListColumnStrsList=map(
					lambda __JoinedCatchDeriveJoiner:
					"Join"+''.join(
						[
							__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr
							if __JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr!="" 
							else 'Top'+__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.__class__.NameStr,
							__JoinedCatchDeriveJoiner.ModeledSuffixStr
						]
					)+"RetrieveIndexesList",
					self.JoinedCatchDeriveJoinersList,
				)

			#debug
			'''
			self.debug(('self.',self,['JoinedRetrieveIndexesListColumnStrsList']))
			'''

			#set
			self.JoinedRetrieveIndexesListGetStrsList=map(
					lambda __JoinedCatchDeriveJoiner:
					"Joined"+''.join(
						[
							self.ModelDeriveControllerVariable.NodeKeyStr
							if self.ModelDeriveControllerVariable.NodeKeyStr!="" 
							else 'Top'+self.ModelDeriveControllerVariable.__class__.NameStr,
							self.ModeledSuffixStr,
							'To',
							__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr
							if __JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.NodeKeyStr!="" 
							else 'Top'+__JoinedCatchDeriveJoiner.ModelDeriveControllerVariable.__class__.NameStr,
							__JoinedCatchDeriveJoiner.ModeledSuffixStr
						]
					)+"RetrieveIndexesList",
					self.JoinedCatchDeriveJoinersList,
				)
			
			#debug
			'''
			self.debug(
						[
							('self.',self,['JoinedRetrieveIndexesListGetStrsList']),
							'Table the joined databases'
						]
					)
			'''

			#Check
			if len(self.ModelingDescriptionTuplesList)>0:
				self.ModelingHdfBool=True
				self.JoiningDatabaseStr="hdf"
				JoinedModelIndexIntKeyStr='ModeledHdfIndexInt'
			else:
				self.JoiningDatabaseStr="mongo"
				JoinedModelIndexIntKeyStr='ModeledMongoIndexInt'


			#Table all the joined databasers and init the corresponding JoinedRetrieveIndexesList in the NodePointDeriveNoder
			self.ModelDeriveControllerVariable.update(
				zip(
						self.JoinedRetrieveIndexesListGetStrsList,
						map(
							lambda __JoinedCatchDeriveJoiner:
							[
								__JoinedCatchDeriveJoiner.table(
									)[
										JoinedModelIndexIntKeyStr
									],
								-1
							],
							self.JoinedCatchDeriveJoinersList
						)
					)
			)

			#debug
			'''
			self.debug(
						('self.',self,[
										'JoinedRetrieveIndexesListColumnStrsList',
										'JoinedRetrieveIndexesListGetStrsList'
									])
			)
			'''

	def mimic_model(self):
		
		#debug
		self.debug(
				'We join model here'
			)

		#/################/#
		# Join first
		#

		#join
		self.join()


		"""
		#/################/#
		# Add to the description the join attributes
		#

		#debug
		'''
		self.debug('Add in the ModelingDescriptionTuplesList')
		'''
		
		#set
		if len(self.JoinedRetrieveIndexesListColumnStrsList)>0:

			#Check
			if self.ModelingHdfBool:

				#import 
				import tables

				#add
				self.ModeledDescriptionTuplesList=map(
					lambda __JoinedRetrieveIndexesListGetStr,__JoinedRetrieveIndexesListColumnStr:
					(
						__JoinedRetrieveIndexesListGetStr,
						__JoinedRetrieveIndexesListColumnStr,
						tables.Int64Col(shape=2)
					),
					self.JoinedRetrieveIndexesListGetStrsList,
					self.JoinedRetrieveIndexesListColumnStrsList
				)+self.ModeledDescriptionTuplesList

		#debug
		'''
		self.debug(
					[	
						('self.',self,['ModelingDescriptionTuplesList']),
						'Now call the parent model method'
					]
				)
		'''

		#/################/#
		# Base method
		#

		#call parent base method
		BaseClass.model(self)
		"""

	def mimic_row(self):

		#debug
		'''
		self.debug('Maybe we have to join first')
		'''

		#table and join first
		self.table()
		self.join()

		#debug
		self.debug(
					[
						"We are going to check if is already inserted in the joined databases...",
						"So we make the children row",
						#('self.',self,['JoinedCatchDeriveJoinersList'])
					]
				)

		#set
		self.JoinedMongoInsertIndexIntsList=map(
					lambda __JoinedCatchDeriveJoiner:
					__JoinedCatchDeriveJoiner.row().RowedMongoIndexInt,
					self.JoinedCatchDeriveJoinersList
				)

		#set
		self.JoinedHdfInsertIndexIntsList=map(
					lambda __JoinedCatchDeriveJoiner:
					__JoinedCatchDeriveJoiner.RowedHdfIndexInt,
					self.JoinedCatchDeriveJoinersList
				)

		

		#debug
		self.debug(
				'Ok the catched databases have rowed',
				('self.',self,[
									'JoinedMongoInsertIndexIntsList',
									'JoinedHdfInsertIndexIntsList'
								])
			)

		#Check
		if len(self.ModelingDescriptionTuplesList)>0:
			self.JoiningDatabaseStr='hdf'

		#Check
		if self.JoiningDatabaseStr=='mongo':

			#set the modeled int in the retrieve tuples
			map(
					lambda __JoinedRetrieveIndexesListGetStr,__JoinedInsertIndexInt:
					getattr(
						self.ModelDeriveControllerVariable,
						__JoinedRetrieveIndexesListGetStr
						).__setitem__(
							1,
							__JoinedInsertIndexInt
					),
					self.JoinedRetrieveIndexesListGetStrsList,
					self.JoinedMongoInsertIndexIntsList
				)

		elif self.JoiningDatabaseStr=='hdf':

			#set the modeled int in the retrieve tuples
			map(
					lambda __JoinedRetrieveIndexesListGetStr,__JoinedInsertIndexInt:
					getattr(
						self.ModelDeriveControllerVariable,
						__JoinedRetrieveIndexesListGetStr
						).__setitem__(
							1,
							__JoinedInsertIndexInt
					),
					self.JoinedRetrieveIndexesListGetStrsList,
					self.JoinedHdfInsertIndexIntsList
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
		self.RowingKeyStrsList=self.JoinedRetrieveIndexesListGetStrsList+self.RowingKeyStrsList

		#debug
		self.debug('Now row with the BaseClass')

		#row then
		BaseClass.row(self)

		#debug
		'''
		self.debug('Ok row is over for joining')
		'''

	def mimic_insert(self,**_KwargVariablesDict):

		#debug
		self.debug('First we row')

		#row first
		self.row()

		#debug
		self.debug(
					[
						'First setSwitch and make insert the catched databases',
						('self.',self,[
											'JoiningCatchStr',
											'JoiningCollectionStr'
									])
					]
				)
		
		#Insert the post joined databases
		self.JoinedCatchDeriveJoinersList=map(
			lambda __JoinedCatchDeriveJoinerPointer:
			__JoinedCatchDeriveJoinerPointer.CatchToPointVariable.insert(),
			self.JoinedCatchCollectionOrderedDict.values(),
		)

		#debug
		self.debug('We transmit now')

		#switch first
		self.transmit(
			[
				(
					'setSwitch',
					SYS.ApplyDictClass(
						{
							'LiargVariablesList':[],
							'KwargVariablesDict':
							{
								'_ClassVariable':"Joiner",
								'_DoStrsList':['Insert']
							}
						}
					)
				)
			],
			[self.JoiningCatchStr+self.JoiningCollectionStr]
		)

		#debug
		self.debug('Now we can insert here')

		#insert then
		BaseClass.insert(self)
		
	def mimic_retrieve(self):

		#debug
		'''
		self.debug(('self.',self,['RetrievingIndexesList']))
		'''

		#retrieve first
		BaseClass.retrieve(self)

		#Retrieve in the joined databases
		JoinedInsertIndexIntsList=map(
					lambda __JoinedRetrieveIndexesListGetStr,__JoinedCatchDeriveJoiner:
					__JoinedCatchDeriveJoiner.retrieve(
						getattr(
							self.ModelDeriveControllerVariable,
							__JoinedRetrieveIndexesListGetStr
						)
					),
					self.JoinedRetrieveIndexesListGetStrsList,
					self.JoinedCatchDeriveJoinersList
				)

		#Check
		if self.JoiningDatabaseStr=='mongo':
			self.JoinedMongoInsertIndexIntsList=JoinedInsertIndexIntsList
		elif self.JoiningDatabaseStr=='hdf':
			self.JoinedHdfInsertIndexIntsList=JoinedInsertIndexIntsList

	def mimic_find(self):

		#table first
		self.table()

		#debug
		'''
		self.debug(('self.',self,['FindingWhereTuplesList']))
		'''

		#
		if self.JoiningFindBeforeBool:

			#Find in the joined databases
			JoinedFindFilterRowDictsListsList=map(
					lambda __JoinedCatchDeriveJoiner:
					__JoinedCatchDeriveJoiner.find(
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
					lambda __JoinedRetrieveIndexesListColumnStr,__JoinedFindFilterRetrieveList:
					(
						__JoinedRetrieveIndexesListColumnStr,
						(
							SYS.getIsInListBool,
							__JoinedFindFilterRetrieveList
						)
					),
					self.JoinedRetrieveIndexesListColumnStrsList,
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
Controller.ModelsParenterClass.ManagingValueClass=JoinerClass
#<DefineLocals>

#</DefinePrint>
JoinerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'JoiningCollectionStr',
		'JoiningCatchStr',
		'JoiningAttentionStr',
		'JoiningFindBeforeBool',
		'JoiningDatabaseStr',
		'JoinedCatchCollectionOrderedDict',
		'JoinedCatchDeriveJoinersList',
		'JoinedRetrieveIndexesListGetStrsList',
		'JoinedRetrieveIndexesListColumnStrsList',
		'JoinedMongoInsertIndexIntsList',
		'JoinedHdfInsertIndexIntsList'
	]
)
#<DefinePrint>
