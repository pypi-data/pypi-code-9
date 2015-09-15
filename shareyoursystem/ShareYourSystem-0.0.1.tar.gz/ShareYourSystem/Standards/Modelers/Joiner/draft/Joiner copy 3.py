#<ImportSpecificModules>
import collections
import copy
import numpy
import tables
import os
import ShareYourSystem as SYS
import sys
#</ImportSpecificModules>

#<DefineLocals>
JoinStr='__'
JoinDeepStr='/'
#</DefineLocals>

#<DefineClass>
class JoinerClass(SYS.FeaturerClass):
	
	#<DefineHookMethods>
	def modelAfter(self,**_ModelingVariablesDict):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug(
					[
						"self.ModeledDict['ModelStr'] is "+str(self.ModeledDict['ModelStr']),
						"We are going to join..."
					]
				)

		#Definition the JoinedOrderedDict
		JoinedOrderedDict=collections.OrderedDict()

		#set in ModeledDict
		self.ModeledDict['JoinedOrderedDict']=JoinedOrderedDict

		#Call the join method
		self.join()

		#debug
		self.debug(
					[
						"Ok joined was done",
						"self.ModeledDict['ModelStr'] is "+str(self.ModeledDict['ModelStr'])
					]
				)

		#Model if there is a JoinedModeledDict
		if self.ModeledDict['JoinedModeledDict']!={}:

			#set an alias for the ModeledDescriptionClass
			ModeledDescriptionClass=self.ModeledDict['ModeledDescriptionClass']

			#Alias
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedRetrievingIndexesListKeyStr']

			#set the columns
			ModeledDescriptionClass.columns[JoinedRetrievingIndexesListKeyStr]=tables.Int64Col(shape=2)
			
			#Alias
			JoinedNodifiedNodeStr=self.ModeledDict['JoinedNodifiedNodeStr']

			#Nodify with the JoinedNodifiedNodeStr
			if JoinedNodifiedNodeStr!="":

				#debug
				self.debug('In the ModeledDescriptionClass we add the joined columns')

				#Alias
				JoinedNodifiedNodedStr=self.ModeledDict['JoinedNodifiedNodedStr']
				JoinedModeledStr=self.ModeledDict['JoinedModeledStr']

				#set the JoinedNodifiedRetrievingIndexesListKeyStrsList
				JoinedNodifiedRetrievingIndexesListKeyStrsList=map(
					lambda __NodifiedKeyStrKeyStr:
					JoinedNodifiedNodedStr+__NodifiedKeyStrKeyStr+JoinedRetrievingIndexesListKeyStr,
					self.ModeledDict['JoinedNodifiedKeyStrsList']
				)

				#set the Cols for the joined children 
				map(
					lambda __JoinedNodifiedRetrievingIndexesListKeyStr:
					ModeledDescriptionClass.columns.__setitem__(
						JoinedNodifiedRetrievingIndexesListKeyStrsList,
						tables.Int64Col(shape=2)
					),
					JoinedNodifiedRetrievingIndexesListKeyStrsList
				)

		#Put them in the ModeledDict
		LocalVars=vars()
		map(
				lambda __GettingStr:
				self.ModeledDict.__setitem__(__GettingStr,LocalVars[__GettingStr]),
				[
					'JoinedOrderedDict'
				]
			)

		#debug
		self.debug('End of the method')

	def rowAfter(self,**_RowingVariablesList):

		#debug
		self.debug('Start of the method')

		#debug
		DebuggingStr="self.ModeledDict['ModelStr'] is "+str(self.ModeledDict['ModelStr'])
		DebuggingStr+='\nWe are going to check if this model is already inserted...'
		self.debug(DebuggingStr)

		#Alias
		JoinedModeledDict=self.ModeledDict['JoinedModeledDict']

		#Check
		if JoinedModeledDict!={}:

			#set JoinedRetrievingIndexesListKeyStr
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedRetrievingIndexesListKeyStr']

			#Definition the GettingStrsList and the GettedVariablesList
			if 'ColumningTuplesList' in JoinedModeledDict:

				#debug
				self.debug('Check that this row is a new row in the table or not')

				#Get the GettingStrsList and GettedVariablesList
				GettingStrsList=SYS.unzip(JoinedModeledDict['ColumningTuplesList'],[0])
				GettedVariablesList=self.pick(GettingStrsList)

				#Check if it was already rowed
				IsRowedBoolsList=map(
						lambda __Row:
						all(
							map(
									lambda __GettingStr,__GettedVariable:
									SYS.getIsEqualBool(__Row[__GettingStr],__GettedVariable),
									GettingStrsList,
									GettedVariablesList
								)
						),
						JoinedModeledDict['TabularedTable'].iterrows()
					)					

				#debug
				if hasattr(self,'StructuredKeyStr'):
					self.debug('self.StructuredKeyStr is '+str(self.StructuredKeyStr))
				self.debug('IsRowedBoolsList is '+str(IsRowedBoolsList))

				#If it is rowed then set the JoinedRetrievingIndexesList
				try:
					RowInt=IsRowedBoolsList.index(True)
				except ValueError:
					RowInt=-1

				#debug
				self.debug('So the corresponding RowInt is '+str(RowInt))

				#set the RowInt
				self.ModeledDict['JoinedOrderedDict'][JoinedRetrievingIndexesListKeyStr][1]=RowInt


			#Alias
			JoinedOrderedDict=self.ModeledDict['JoinedOrderedDict']
			JoinedRetrievingIndexesList=self.ModeledDict['JoinedOrderedDict'][JoinedRetrievingIndexesListKeyStr]
			JoinedNodifiedNodeStr=self.ModeledDict['JoinedNodifiedNodeStr']

			#Give the JoinedRetrievingIndexesList to itself
			JoinedOrderedDict.__setitem__(
				JoinedRetrievingIndexesListKeyStr,
				JoinedRetrievingIndexesList
			)

			#debug
			self.debug(
						[
							'JoinedOrderedDict is now',
							SYS.represent(JoinedOrderedDict)
						]
					)

			#Give to the parent
			if JoinedNodifiedNodeStr!="":
				ParentPointer=getattr(
										self,
										JoinedNodifiedNodedStr+'ParentPointer'
							)
				if ParentPointer!=None:
					ParentPointer['App_Model_'+ModelingStr+'Dict']['JoinedOrderedDict'][
							getattr(
									self,
									JoinedNodifiedNodedStr+'KeyStr'
									)+JoinedRetrievingIndexesListKeyStr
							]=JoinedRetrievingIndexesList

			#Update the self.RowedIdentifiedOrderedDic
			self.ModeledDict['RowedIdentifiedOrderedDict'].update(JoinedOrderedDict)

		#debug
		self.debug('End of the method')

	def insertBefore(self,**_InsertingVariablesList):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug(	
					[
						"self.ModeledDict['ModelStr'] is "+str(self.ModeledDict['ModelStr']),
						'self.StructuredKeyStr is '+str(self.StructuredKeyStr) if hasattr(self,"StructuredKeyStr") else ''
					]
				)

		#Definition the NotRowedTuplesList
		NotRowedTuplesList=filter(
				lambda __JoiningTuple:
				__JoiningTuple[1][0]<0 or __JoiningTuple[1][1]<0,
				self.ModeledDict['JoinedOrderedDict'].items()
			)

		#debug
		self.debug('NotRowedTuplesList is '+str(NotRowedTuplesList))

		#Alias
		ModelStr=self.ModeledDict['ModelStr']

		#IsNodingInsertingBool
		if 'IsNodingInsertingBool' not in _InsertingVariablesList or _InsertingVariablesList['IsNodingInsertingBool']:

			#debug
			self.debug(
						[
							'We are going to make insert all the noded children with the Model',
							'ModelStr is '+str(ModelStr)
						]
					)

			#Insert each noded children
			map(
					lambda __Variable:
					__Variable.insert(ModelStr),
					self.ModeledDict['JoinedNodifiedOrderedDict'].values()
				)

			#debug
			self.debug(
						[
							'The noded children have inserted',
							'Now look at the joined model',
							('self.ModeledDict',self.ModeledDict,['JoinedModelStr'])
						]
					)

		#insert the joined model
		if self.ModeledDict['JoinedModelStr']!="":

			#debug
			self.debug(
						[
							'Insert self with the joined model',
							'But without making the noded children inserting'
						]
					)

			#Copy the ModeledDict
			CopiedModeledDict=copy.copy(self.ModeledDict)

			#Insert
			self.insert(self.ModeledDict['JoinedModelStr'],**{'IsNodingInsertingBool':False})

			#debug
			self.debug('Insert self with the joined model was done')
		
			#Reset the self.ModeledDict
			self.ModeledDict=CopiedModeledDict

			#set the JoinedRetrievingIndexesListKeyStr
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedModeledDict']['ModeledStr']+'RetrievingIndexesList'

			#Alias
			JoinedOrderedDict=self.ModeledDict['JoinedOrderedDict']

			#It is going to be inserted so update the self.JoinedRetrievingIndexesList to the last row index
			if JoinedOrderedDict[JoinedRetrievingIndexesListKeyStr][1]==-1:

				#debug
				self.debug(
							[
								'This is a new row so we just set the RowInt of the <JoinedModeledStr>RetrievingIndexesList',
								'To the size of the table',
								'JoinedOrderedDict[JoinedRetrievingIndexesListKeyStr] is '+str(
									JoinedOrderedDict[JoinedRetrievingIndexesListKeyStr])
							]
						)

				#Update the corresponding RetrievingIndexesList
				JoinedOrderedDict[JoinedRetrievingIndexesListKeyStr][1]=self.ModeledDict['JoinedModeledDict']['TabularedTable'].nrows-1

				#debug
				self.debug('Now JoinedOrderedDict[JoinedRetrievingIndexesListKeyStr] is '+str(
					JoinedOrderedDict[JoinedRetrievingIndexesListKeyStr]))

			#Get the JoinedRetrievingIndexesList
			JoinedRetrievingIndexesListsList=map(
								lambda __InsertingVariable:
								__InsertingVariable.ModeledDict['JoinedRetrievingIndexesList'],
								self.ModeledDict['JoinedNodifiedOrderedDict'].values()
							)

		else:

			#set by default an empty list
			JoinedRetrievingIndexesListsList=[]

		#debug
		self.debug(
					[
						'self.StructuredKeyStr is '+str(self.StructuredKeyStr) if hasattr(self,'StructuredKeyStr') else '',
						"self.ModeledDict['ModelStr'] is "+str(self.ModeledDict['ModelStr']),
						'We add in the RowedIdentifiedOrderedDict the Joined JoinedRetrievingIndexesLists',
						"self.ModeledDict['RowedIdentifiedOrderedDict'] is "+str(
								self.ModeledDict['RowedIdentifiedOrderedDict']),
						"NotRowedTuplesList is "+str(NotRowedTuplesList),
						"JoinedRetrievingIndexesListsList is "+str(JoinedRetrievingIndexesListsList)
					]
		)

		#Alias
		RowedIdentifiedOrderedDict=self.ModeledDict['RowedIdentifiedOrderedDict']

		#Just change the __RowInt
		map(
				lambda __NotRowedTuple:
				RowedIdentifiedOrderedDict.__setitem__(__NotRowedTuple[0],__NotRowedTuple[1]),
				NotRowedTuplesList
			)

		#debug
		self.debug('Now the RowedIdentifiedOrderedDict is '+str(RowedIdentifiedOrderedDict))

		#debug
		self.debug('End of the method')

	def retrieveAfter(self,**_RetrievingVariablesDict):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug("self.ModeledDict['RetrievingIndexesList'] is "+str(self.ModeledDict['RetrievingIndexesList']))

		#Alias
		RetrievedTuplesList=self.ModeledDict['RetrievedTuplesList']

		#debug	
		DebuggedStr='RetrievedTuplesList is '+str(RetrievedTuplesList)
		self.debug(DebuggedStr)

		#Definition the RetrievingIndexesListIndexInt
		if len(RetrievedTuplesList)>0:

			#Get the Index 
			RetrievingIndexesListIndexInt=SYS.unzip(RetrievedTuplesList,[0]).index(
				self.ModeledDict['JoinedRetrievingIndexesListKeyStr'])

			#set and retrieve for the joined model
			self.ModeledDict['RetrievingIndexesList']=RetrievedTuplesList[RetrievingIndexesListIndexInt][1]
			self.retrieve(self.ModeledDict['JoinedModeledDict']['ModelStr'])

		#debug
		self.debug('End of the method')

	def findBefore(self,**_FindingVariablesDict):

		#debug
		self.debug('Find the joined model')

		#Alias
		JoinedModelStr=self.ModeledDict['JoinedModelStr']

		#Check that JoinedModelStr is good
		if JoinedModelStr!="":

			#Copy the ModeledDict
			CopiedModeledDict=copy.copy(self.ModeledDict)

			#debug
			self.debug(
						[
							'First we are going to find in the joined model',
							'JoinedModelStr is '+str(JoinedModelStr)
						]
					)

			#Find
			self.ModeledDict=self.ModeledDict['JoinedModeledDict']
			self.find()
			JoinedModeledDict=self.ModeledDict
			self.ModeledDict=CopiedModeledDict

			#debug
			self.debug(
						[
							'Find in the joined model is done',
							'JoinedModelStr is '+str(JoinedModelStr)
						]
					)

			#debug
			self.debug('Ok we have found the joined model')

			#Copy the FoundFilteredRowedDictsList
			JoinedFoundFilteredRowedDictsList=JoinedModeledDict['FoundFilteredRowedDictsList']

			#debug
			self.debug(
						[
							'JoinedFoundFilteredRowedDictsList is ',
							SYS.represent(JoinedFoundFilteredRowedDictsList)
						]
			)

			#Alias
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedRetrievingIndexesListKeyStr']

			#Make the TabularedInt and the RowInt as a <JoinedModelStr>RetrievingIndexesList
			map(
					lambda __JoinedFoundFilteredRowedDict:
					__JoinedFoundFilteredRowedDict.__setitem__(
						JoinedRetrievingIndexesListKeyStr,
						[
							__JoinedFoundFilteredRowedDict['TabularedInt'],
							__JoinedFoundFilteredRowedDict['RowInt'],
						]
					),
					JoinedFoundFilteredRowedDictsList
				)

			#set the JoinedFindingTuplesList
			JoinedFindingTuplesList=[
						(
							JoinedRetrievingIndexesListKeyStr,
							(
								SYS.getIsInListBool,
								map(
										lambda __JoinedFoundFilteredRowedDict:
										[
											__JoinedFoundFilteredRowedDict['TabularedInt'],
											__JoinedFoundFilteredRowedDict['RowInt'],
										],
										JoinedFoundFilteredRowedDictsList
									)
							)
					)
				]

			#debug
			self.debug(
						[
							'JoinedFindingTuplesList is',
							SYS.represent(JoinedFindingTuplesList)
						]
					)

		else:

			#set an default empty
			JoinedFindingTuplesList=[]

		#debug
		self.debug(
					[
						'Joiner findbefore is over',
						('self.ModeledDict',self.ModeledDict,['ModelStr','FoundRowDictsList'])
					]
				)

		#Put them in the ModeledDict
		LocalVars=vars()
		map(
				lambda __GettingStr:
				self.ModeledDict.__setitem__(__GettingStr,LocalVars[__GettingStr]),
				[
					'JoinedFindingTuplesList',
				]
			)

		#debug
		self.debug('End of the method')

	def findAfter(self,**_FindingVariablesDict):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug(
					[
						('Are we going to do a where with the FoundFilteredRowedDictsList and the '),
						('filtering JoinedFindingTuplesList?'),
						('self.ModeledDict ',self.ModeledDict,[
																'ModelStr',
																'FoundFilteredRowedDictsList'
																]),
						("'JoinedFindingTuplesList' in self.ModeledDict is "+str(
							'JoinedFindingTuplesList' in self.ModeledDict))
					]
			)

		if 'JoinedFindingTuplesList' in self.ModeledDict:

			#debug
			self.debug(
						[
							'Ok we are going to do the where',
							"self.ModeledDict['JoinedFindingTuplesList'] is "+str(
								self.ModeledDict['JoinedFindingTuplesList'])
						]
					)

			#Where
			self.ModeledDict['FoundFilteredRowedDictsList']=SYS.filterNone(SYS.where(
							self.ModeledDict['FoundFilteredRowedDictsList'],
							self.ModeledDict['JoinedFindingTuplesList']
							)
			)

			#debug
			self.debug('Ok the where is done.')

		#debug
		self.debug(
					[
						'After intersection',
						('self.ModeledDict ',self.ModeledDict,[
															'ModelStr',
															'FoundFilteredRowedDictsList'
															]
														)
					]
				)

		#debug
		self.debug('End of the method')

	def recoverBefore(self,**_LocalRecoveringVariablesDict):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug(
					[
						('self.ModeledDict ',self.ModeledDict,[
															'ModelStr',
															'FoundFilteredRowedDictsList'
															]
														)
					]
				)

		#Alias
		FoundFilteredRowedDictsList=self.ModeledDict['FoundFilteredRowedDictsList']

		#debug
		self.debug(
					[
						'Look if we have found only one FilteredRowedDict',
						'len(FoundFilteredRowedDictsList) is '+str(len(FoundFilteredRowedDictsList))
					]
				)

		if len(FoundFilteredRowedDictsList)==1:
				
			#debug
			self.debug('It is good, there is one solution !')

			#Definition a JoinedRecoveredDict
			JoinedRecoveredDict=FoundFilteredRowedDictsList[0]

			#Alias
			JoinedNodifiedOrderedDict=self.ModeledDict['JoinedNodifiedOrderedDict']
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedRetrievingIndexesListKeyStr']
			
			#debug
			self.debug(
						[
							'But first look if we have to recover the children first',
							"len(JoinedNodifiedOrderedDict) is "+str(
								len(JoinedNodifiedOrderedDict))
						]
					)

			#Maybe we have to recover the children before
			if len(JoinedNodifiedOrderedDict)>0:

				self.debug(
							[
								'Yes, we are going to make recover each children before'
							]
						)

				#set each Children and recover each
				JoinedNodifiedKeyStr=self.JoinedNodifiedNodedStr+'KeyStr'

				#Alias
				ModelStr=self.ModeledDict['ModelStr']
				ModelingStr=self.ModeledDict['ModelingStr']
				JoinedNodifiedNodedStr=self.ModeledDict['JoinedNodifiedNodedStr']

				#Map a Recover
				map(
						lambda __JoinedJoiner:
						__JoinedJoiner.__setitem__(
								'/App_Model_'+ModelingStr+'Dict/FindingTuplesList',
								[
									(
										JoinStr+JoinedRetrievingIndexesListKeyStr,
										(
											SYS.getIsEqualBool,
											JoinedRecoveredDict[
											JoinedNodifiedNodedStr+getattr(
													__JoinedJoiner,
													JoinedNodifiedNodedStr
													)+JoinedRetrievingIndexesListKeyStr
											]
										)
									)
								]
						).recover(ModelStr),
						JoinedNodifiedOrderedDict.values()
					)

				#debug
				self.debug('Ok the children are recovered')

			#debug
			self.debug(
						[
							'Maybe update first the joined model by retrieving',
							"JoinedRecoveredDict[JoinedRetrievingIndexesListKeyStr] is "+str(
								JoinedRecoveredDict[JoinedRetrievingIndexesListKeyStr]
								)
						]
					)

			#set RetrievingIndexesList in the model and retrieve
			self['App_Model_'+self.ModeledDict['JoinedModelingStr']+'Dict']['RetrievingIndexesList']=JoinedRecoveredDict[
						JoinedRetrievingIndexesListKeyStr
						]
			self.retrieve(JoinedModelStr)

			#debug
			self.debug('Ok the joined model was retrieved')


			"""
			print('self.JoinedFilteredMergedRowedDictsListTuplesList is')
			SYS._print(self.JoinedFilteredMergedRowedDictsListTuplesList)
			print('AppendingGettingStrsList is ',AppendingGettingStrsList)

			#Next we have maybe to update with the joined model	
			if '/' in AppendingGettingStrsList:	

				#Definition the IndexInt of the joined model
				IndexInt=AppendingGettingStrsList.index('/')

				#Definition the JoinedFilteredMergedRowedDictsList
				JoinedFilteredMergedRowedDictsList=self.JoinedFilteredMergedRowedDictsListTuplesList[
						IndexInt][1] 

				#Definition the JoinedRetrievingIndexesList
				JoinedRetrievingIndexesList=JoinedRecoveredDict[self.JoinedRetrievingIndexesListKeyStr]

				#debug
				print('JoinedFilteredMergedRowedDictsList is ')
				SYS._print(JoinedFilteredMergedRowedDictsList)
				print('JoinedRetrievingIndexesList is ',JoinedRetrievingIndexesList)
				if hasattr(self,'StructuredKeyStr'):
					print("self['StructuredKeyStr'] is ",self.StructuredKeyStr)
				print('')

				#Take the first element of self.JoinedFilteredMergedRowedDictsTuplesList which corresponds to the Joined Model at this level	
				JoinedRowedDict=next(
						RowedDict for RowedDict in JoinedFilteredMergedRowedDictsList
						if SYS.getIsEqualBool(
							RowedDict[self.JoinedRetrievingIndexesListKeyStr],
							JoinedRetrievingIndexesList
						)
					)

				#debug
				'''
				print('JoinedRowedDict is ',JoinedRowedDict)
				print('')
				'''

				#Update
				self.update(JoinedRowedDict.items())
			"""
			
		else:

			#debug
			'''
			print('Joiner There are multiple retrieved states')
			if hasattr(self,'StructuredKeyStr'):
				print("self['StructuredKeyStr'] is ",self.StructuredKeyStr)
			print("self.ModeledDict['FoundFilteredRowedDictsList'] is ")
			SYS._print(self.ModeledDict['FoundFilteredRowedDictsList'])
			print('')
			'''

			#Stop the recover
			self.IsRecoveringBool=False

		#debug
		self.debug('End of the method')

	#</DefineHookMethods>
	def join(	
				self,
				_ModelStr="",
				**_JoiningVariablesDict
			):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug(
					[
						'_ModelStr is '+str(_ModelStr),
						'self.StructuredKeyStr is '+str(self.StructuredKeyStr) if hasattr(self,"StructuredKeyStr") else ''
					]
				)

		#Check
		if 'JoiningTuple' not in self.ModeledDict:
			self.ModeledDict['JoiningTuple']=("","")

		#set JoinedNodifiedNodeStr and JoinedModelStr
		JoinedNodifiedNodeStr=self.ModeledDict['JoiningTuple'][0]
		JoinedModelStr=self.ModeledDict['JoiningTuple'][1]

		#Put them in the ModeledDict
		LocalVars=vars()
		map(
				lambda __GettingStr:
				self.ModeledDict.__setitem__(__GettingStr,LocalVars[__GettingStr]),
				[
					'JoinedNodifiedNodeStr',
					'JoinedModelStr'
				]
			)

		#set the JoiningTuple
		if 'JoiningTuple' not in _JoiningVariablesDict:

			#set to the _JoiningVariablesDict
			_JoiningVariablesDict['JoiningTuple']=self.ModeledDict['JoiningTuple']

			#Maybe we have to structure
			if self.IsGroupedBool==False:

				#debug
				self.debug(
							[
								'Join We have to structure first',
								'self.StructuredKeyStr is '+str(self.StructuredKeyStr) if hasattr(self,"StructuredKeyStr") else ''
							]
					)
				
				#Structure
				self.structure(JoinedNodifiedNodeStr)

		#Nodify if there is the nodified objects
		if JoinedNodifiedNodeStr!="":

			#debug
			self.debug('Joiner we are going to nodify the '+str(JoinedNodifiedNodeStr))

			#Nodify
			self.nodify(JoinedNodifiedNodeStr)

			#set 
			JoinedNodifiedOrderedDict=copy.copy(self.NodifiedOrderedDict)
			JoinedNodifiedNodedStr=self.NodifiedNodedStr
			JoinedNodifiedNodingStr=self.NodifiedNodingStr

			#debug
			self.debug('self.JoinedNodifiedOrderedDict is '+str(JoinedNodifiedOrderedDict))

		else:

			#set an empty dict
			JoinedNodifiedOrderedDict=collections.OrderedDict()
			JoinedNodifiedNodedStr=""
			JoinedNodifiedNodingStr=""

		#Put them in the ModeledDict
		LocalVars=vars()
		map(
				lambda __GettingStr:
				self.ModeledDict.__setitem__(__GettingStr,LocalVars[__GettingStr]),
				[
					'JoinedNodifiedOrderedDict',
					'JoinedNodifiedNodedStr',
					'JoinedNodifiedNodingStr'
				]
			)

		#debug
		self.debug('We are maybe tabling the joined model ?')

		#Table maybe the joined model
		if JoinedModelStr!="":

			#set a copy of it
			LastModeledDict=copy.copy(self.ModeledDict)

			#debug
			self.debug(
						[
							'We are going to table the joinedModel',
							'JoinedModelStr is '+str(JoinedModelStr)
						]
					)

			#table to configure the joined model
			self.table(JoinedModelStr)

			#debug
			self.debug(
						[
							'The joined model is tabled ok',
							'JoinedModelStr is '+str(JoinedModelStr)
						]
					)

			#Copy the ModeledDict
			JoinedModeledDict=copy.copy(self.ModeledDict)

			#Reset the ModeledDict to the original
			self.ModeledDict=LastModeledDict

		else:

			#debug
			self.debug('We dont need to table because this model has not a joined model')

			#Init an empty dict
			JoinedModeledDict={}

		#set a link
		self.ModeledDict['JoinedModeledDict']=JoinedModeledDict

		#Check
		if JoinedModeledDict!={}:

			#debug
			self.debug('We are building the JoinedRetrievingIndexesList and give him the TabularedInt')

			#set the JoinedRetrievingIndexesListKeyStr
			JoinedRetrievingIndexesListKeyStr=JoinedModeledDict['ModeledStr']+'RetrievingIndexesList'
			self.ModeledDict['JoinedRetrievingIndexesListKeyStr']=JoinedRetrievingIndexesListKeyStr

			#set in the ModeledDict
			self.ModeledDict['JoinedOrderedDict'][JoinedRetrievingIndexesListKeyStr]=[JoinedModeledDict['TabularedInt'],-1]

			#debug
			self.debug("OK self.ModeledDict['JoinedOrderedDict' is so "+str(
				self.ModeledDict['JoinedOrderedDict']))
			
		#debug
		self.debug('End of the method')

		#Return self
		return self

#</DefineClass>

#<DefineAttestingFunctions>
def attest_join():

	#Build Hdf groups
	Joiner=SYS.JoinerClass().hdformat().update(
								[
									(
										'App_Structure_ChildJoiner1',
										SYS.JoinerClass().update(
										[
											('App_Model_ParameterizingDict',
														{
															'ColumningTuplesList':
															[
																('MyIntsList',tables.Int64Col(shape=2))
															]
														}
											),
											('MyIntsList',[2,4]),
											('App_Model_ResultingDict',
														{
															'ColumningTuplesList':
															[
																('MyInt',tables.Int64Col())
															]
														}
											),
											('MyInt',1)
										])
									),
									('App_Model_ParameterizingDict',
														{
															'ColumningTuplesList':
															[
																('MyStr',tables.StrCol(10)),
															]
														}
									),
									('MyStr',"hello")
								]	
							).walk(
										[
											'StructuredOrderedDict.items()'
										],
										**{
												'BeforeUpdateList':
												[
													('parentize',{'ArgsVariable':"Structure"}),
													('group',{'ArgsVariable':""}),
													('model',{'ArgsVariable':"Parameter"}),
													('table',{'ArgsVariable':""}),
													('row',{'ArgsVariable':""}),
													('insert',{'ArgsVariable':""})
												]
											}
									).update(
										[
											
											('App_Model_ResultingDict',
												{
													'ColumningTuplesList':
													[
														('MyFloat',tables.Float32Col()),
														('MyFloatsList',tables.Float32Col(shape=3))
													],
													'JoiningTuple':("Structure","Parameter")
												}
											),
											('MyFloat',0.1),
											('MyFloatsList',[2.3,4.5,1.1])
										]
									).model("Result"		
									).table(
									).row(
									).insert("Result"
									).hdfclose()

	#Return the object itself
	return "Objects is : \n"+SYS.represent(
		Joiner
		)+'\n\n\n'+SYS.represent(os.popen('/usr/local/bin/h5ls -dlr '+Joiner.HdformatingPathStr
		).read())
#</DefineAttestingFunctions>
