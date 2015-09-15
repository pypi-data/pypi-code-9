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
BasingLocalTypeStr="Shaper"
BaseClass=getattr(SYS,SYS.getClassStrWithTypeStr(BasingLocalTypeStr))
#</DefineLocals>

#<DefineClass>
class JoinerClass(BaseClass):
	
	@SYS.HookerClass(**{'AfterTuplesList':[(BaseClass,"init")]})
	def init(self):

		#<DefineSpecificDo>
		self.JoinedOrderedDict=collections.OrderedDict()		#<NotRepresented>
		self.JoinedDatabasePointer=None							#<NotRepresented>
		#</DefineSpecificDo>

	@SYS.HookerClass(**{'BeforeTuplesList':[("<TypeStr>","join")],'AfterTuplesList':[("Featurer","model")]})
	def model(self,**_KwargVariablesDict):

		#debug
		self.debug('Start of the method')

		#Model if there is a JoinedDatabasePointer
		if self.JoinedDatabasePointer!=None:

			#set the columns
			self.ModeledDescriptionClass.columns[self.JoinedRetrievingIndexesListKeyStr]=tables.Int64Col(shape=2)
			
		#debug
		self.debug('End of the method')

	@SYS.HookerClass(**{'AfterTuplesList':[("Featurer","row")]})
	def row(self,**_VariablesList):

		#debug
		self.debug('Start of the method')

		#debug
		self.debug(
					[
						"self.ModelingModelStr is "+str(self.ModelingModelStr),
						"We are going to check if the joined model is already inserted...",
						"First look if self.JoinedModeledDatabase!={} is "+str(len(self.JoinedModeledDatabase)>0)
					]
				)

		#Check
		if self.JoinedDatabasePointer!=None:

			#debug
			self.debug("Ok there is a self.JoinedDatabasePointer")

			#Alias
			JoinedRetrievingIndexesList=self.JoinedRetrievingIndexesList
			JoinedRetrievingIndexesListKeyStr=self.JoinedRetrievingIndexesListKeyStr

			#debug
			self.debug('Check that this joined row is a new row in the table or not')

			#Get the GettingStrsList and GettedVariablesList
			GettingStrsList=SYS.unzip(self.JoinedModeledDatabase.ModelingColumningTuplesList,[0])
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
					self.JoinedDatabasePointer.TabledTable.iterrows()
				)					

			#debug
			self.debug(
						[
							'self.StructuredKeyStr is '+str(
								self.StructuredKeyStr) if hasattr(self,'StructuredKeyStr') else "",
							'IsRowedBoolsList is '+str(IsRowedBoolsList)
						]
					)

			#If it is rowed then set the JoinedRetrievingIndexesList
			try:
				RowInt=IsRowedBoolsList.index(True)
			except ValueError:
				RowInt=-1

			#debug
			self.debug('So the corresponding RowInt is '+str(RowInt))

			#set the RowInt
			JoinedRetrievingIndexesList[1]=RowInt
			#self.ModeledDict['JoinedOrderedDict'][JoinedRetrievingIndexesListKeyStr][1]=RowInt


			#Alias
			'''
			JoinedOrderedDict=self.ModeledDict['JoinedOrderedDict']
			JoinedRetrievingIndexesList=self.ModeledDict['JoinedOrderedDict'][JoinedRetrievingIndexesListKeyStr]

			#Give the JoinedRetrievingIndexesList to itself
			JoinedOrderedDict.__setitem__(
				JoinedRetrievingIndexesListKeyStr,
				JoinedRetrievingIndexesList
			)
			'''

			'''
			#debug
			self.debug(
						[
							'JoinedOrderedDict is now',
							SYS.represent(JoinedOrderedDict)
						]
					)
			'''

			#debug
			#self.debug('So we set the JoinedRetrievingIndexesList in the RowedIdentifiedOrderedDict')

			#Update the self.RowedIdentifiedOrderedDic
			#self.ModeledDict['RowedIdentifiedOrderedDict'].update(JoinedOrderedDict)
			#self.ModeledDict['RowedIdentifiedOrderedDict'].__setitem__(
			#			JoinedRetrievingIndexesListKeyStr,
			#			JoinedRetrievingIndexesList
			#		)

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
		#NotRowedTuplesList=filter(
		#		lambda __JoiningTuple:
		#		__JoiningTuple[1][0]<0 or __JoiningTuple[1][1]<0,
		#		self.ModeledDict['JoinedOrderedDict'].items()
		#	)

		#Alias
		ModelStr=self.ModeledDict['ModelStr']

		#insert the joined model
		if self.ModeledDict['JoiningModelStr']!="":

			#debug
			self.debug(
						[
							'Insert self with the joined model'
						]
					)

			#Copy the ModeledDict
			CopiedModeledDict=copy.copy(self.ModeledDict)

			#Insert
			self.insert(self.ModeledDict['JoiningModelStr'])

			#debug
			self.debug('Insert self with the joined model was done')
		
			#Reset the self.ModeledDict
			self.ModeledDict=CopiedModeledDict

			#set the JoinedRetrievingIndexesListKeyStr
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedModeledDict']['ModeledStr']+'RetrievingIndexesList'

			#Alias
			JoinedRetrievingIndexesList=self.ModeledDict['JoinedRetrievingIndexesList']

			#It is going to be inserted so update the JoinedRetrievingIndexesList to the last row index
			if JoinedRetrievingIndexesList==-1:

				#debug
				self.debug(
							[
								'This is a new row so we just set the RowInt of the <JoinedModeledStr>RetrievingIndexesList',
								'To the size of the table',
								'JoinedRetrievingIndexesList is '+str(
									JoinedRetrievingIndexesList)
							]
						)

				#Update the corresponding RetrievingIndexesList
				JoinedRetrievingIndexesList[1]=self.ModeledDict['JoinedModeledDict']['TabledTable'].nrows-1

				#debug
				self.debug('Now JoinedRetrievingIndexesList is '+str(
					JoinedRetrievingIndexesList))

		#debug
		self.debug(
					[
						'self.StructuredKeyStr is '+str(self.StructuredKeyStr) if hasattr(self,'StructuredKeyStr') else '',
						"self.ModeledDict['ModelStr'] is "+str(self.ModeledDict['ModelStr']),
						'We add in the RowedIdentifiedOrderedDict the Joined JoinedRetrievingIndexesLists',
						"self.ModeledDict['RowedIdentifiedOrderedDict'] is "+str(
								self.ModeledDict['RowedIdentifiedOrderedDict']),
						"NotRowedTuplesList is "+str(NotRowedTuplesList)
					]
		)

		#debug
		self.debug('We set the JoinedRetrievingIndexesList in the RowedIdentifiedOrderedDict')

		#Update the self.RowedIdentifiedOrderedDic
		#self.ModeledDict['RowedIdentifiedOrderedDict'].update(JoinedOrderedDict)
		self.ModeledDict['RowedIdentifiedOrderedDict'].__setitem__(
					JoinedRetrievingIndexesListKeyStr,
					JoinedRetrievingIndexesList
				)

		#Alias
		#RowedIdentifiedOrderedDict=self.ModeledDict['RowedIdentifiedOrderedDict']

		#Just change the __RowInt
		#map(
		#		lambda __NotRowedTuple:
		#		RowedIdentifiedOrderedDict.__setitem__(__NotRowedTuple[0],__NotRowedTuple[1]),
		#		NotRowedTuplesList
		#	)

		#debug
		#self.debug('Now the RowedIdentifiedOrderedDict is '+str(RowedIdentifiedOrderedDict))

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
		self.debug('Start of the method')

		#Alias
		JoiningModelStr=self.ModeledDict['JoiningModelStr']

		#debug
		self.debug(
					[
						'Find maybe first in the joined model',
						'JoiningModelStr is '+JoiningModelStr
					]
				)

		#Check that JoiningModelStr is good
		if JoiningModelStr!="":

			#Copy the ModeledDict
			CopiedModeledDict=copy.copy(self.ModeledDict)

			#debug
			self.debug(
						[
							'First we are going to find in the joined model',
							'JoiningModelStr is '+str(JoiningModelStr)
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
							'JoiningModelStr is '+str(JoiningModelStr)
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

			#Make the TabledInt and the RowInt as a <JoiningModelStr>RetrievingIndexesList
			map(
					lambda __JoinedFoundFilteredRowedDict:
					__JoinedFoundFilteredRowedDict.__setitem__(
						JoinedRetrievingIndexesListKeyStr,
						[
							__JoinedFoundFilteredRowedDict['TabledInt'],
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
											__JoinedFoundFilteredRowedDict['TabledInt'],
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

			#set a default empty
			JoinedFindingTuplesList=[]

		#debug
		self.debug(
					[
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
			JoinedRetrievingIndexesListKeyStr=self.ModeledDict['JoinedRetrievingIndexesListKeyStr']
				
		else:

			#debug
			self.debug('There are multiple found states')

			#Stop the recover
			self.IsRecoveringBool=False

		#debug
		self.debug('End of the method')

	def joinBefore(	
				self,
				**_JoiningVariablesDict
			):

		#debug
		self.debug('Start of the method')

		#Alias
		JoiningModelStr=self.ModeledDict['JoiningModelStr']

		#Table maybe the joined model
		if JoiningModelStr!="":

			#debug
			self.debug('We are tabling the joined model ?')

			#set a copy of it
			LastModeledDict=copy.copy(self.ModeledDict)

			#Get the joined ModeledDict
			self.ModeledDict=self['App_Model_'+SYS.getDoingStrWithDoStr(JoiningModelStr)+'Dict']

			#debug
			self.debug(
						[
							'Check if we have to table',
							"self.ModeledDict!=None and ('IsTabledBool' not in self.ModeledDict or self.ModeledDict['IsTabledBool']==False) is "+str(
								self.ModeledDict!=None and (
									'IsTabledBool' not in self.ModeledDict or self.ModeledDict['IsTabledBool']==False)),
						]
					)
			
			#Check that we have to table
			if self.ModeledDict!=None and (
				'IsTabledBool' not in self.ModeledDict or self.ModeledDict['IsTabledBool']==False):
				
				#debug
				self.debug(
							[
								'We are going to table',
								"'IsTabledBool' not in self.ModeledDict' is "+str(
								'IsTabledBool' not in self.ModeledDict)
							]
						)

				#Table
				self.table(JoiningModelStr)

				#debug
				self.debug('Ok this is tabled')

			#debug
			self.debug(
						[
							'The joined model is tabled ok',
							'JoiningModelStr is '+str(JoiningModelStr)
						]
					)

			#Copy the ModeledDict
			JoinedModeledDict=copy.copy(self.ModeledDict)

			#Reset the ModeledDict to the original
			self.ModeledDict=LastModeledDict

			#set a link
			self.ModeledDict['JoinedModeledDict']=JoinedModeledDict

			#Check
			if JoinedModeledDict!={}:

				#debug
				self.debug('We are building the JoinedRetrievingIndexesList and give him the TabledInt')

				#set the JoinedRetrievingIndexesListKeyStr
				JoinedRetrievingIndexesListKeyStr=JoinedModeledDict['ModeledStr']+'RetrievingIndexesList'
				self.ModeledDict['JoinedRetrievingIndexesListKeyStr']=JoinedRetrievingIndexesListKeyStr

				#set in the ModeledDict
				self.ModeledDict['JoinedOrderedDict'][JoinedRetrievingIndexesListKeyStr]=[JoinedModeledDict['TabledInt'],-1]

				#debug
				self.debug("OK self.ModeledDict['JoinedOrderedDict' is so "+str(
					self.ModeledDict['JoinedOrderedDict']))
				
		#debug
		self.debug('End of the method')

		#Return self
		return self
	#</DefineHookMethods>

	#<DefineMethod>
	def join(self,**_JoiningVariablesDict):
		"""Call the Output<HookStr> methods and return self.OutputedPointer (self by default)"""

		#debug
		self.debug('Start of the method')

		#Check
		if self.IsTabledBool==False:

			#debug
			self.debug('We have to table first')

			#Table
			self.table()

			#debug
			self.debug('Ok this is tabled')

		#Refresh some attributes
		LocalOutputedPointer=self
		LocalJoiningVariablesDict=_JoiningVariablesDict
		self.IsJoiningBool=True

		#Hook
		if self.IsJoinedBool==False:

			#Hook methods
			for OrderStr in ["Before","After"]:
			
				#Definition the HookMethodStr
				HookingMethodStr='join'+OrderStr

				#Check that there is HookingMethods for it
				if HookingMethodStr in self.__class__.HookingMethodStrToMethodsListDict:

					#Call the specific Appended methods 
					for HookingMethod in self.__class__.HookingMethodStrToMethodsListDict[HookingMethodStr]:

						#Call the HookMethod
						OutputVariable=HookingMethod(self,**LocalJoiningVariablesDict)

						if type(OutputVariable)==dict:
							if 'LocalJoiningVariablesDict' in OutputVariable:
								LocalJoiningVariablesDict=OutputVariable['LocalJoiningVariablesDict']
							if 'LocalOutputedPointer' in OutputVariable:
								LocalOutputedPointer=OutputVariable['LocalOutputedPointer']

						#Check Bool
						if self.IsJoiningBool==False:
							self.IsJoinedBool=True
							return LocalOutputedPointer

			#set
			self.IsJoinedBool=True

		#debug
		self.debug('End of the method')

		#Return the OutputVariable
		return LocalOutputedPointer
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
