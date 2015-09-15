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
	def initAfter(self):

		#<DefineSpecificDo>
		self.JoinedNodifiedOrderedDict=collections.OrderedDict()	#<NotRepresented>
		self.JoinedOrderedDict=collections.OrderedDict() 			#<NotRepresented>
		self.JoinedJoinedListKeyStr=""							#<NotRepresented>
		self.JoinedModeledKeyStr=""								#<NotRepresented>
		self.JoinedModeledDict={}									#<NotRepresented>
		self.JoinedTabularedTable=None      						#<NotRepresented>
		self.JoinedJoinedList=[-1,-1]								#<NotRepresented>
		self.JoinedRetrievingIndexesListsList=[]							#<NotRepresented>
		self.JoinedNodifiedNodeStr=""							#<NotRepresented>
		self.JoinedNodifiedNodedStr=""							#<NotRepresented>
		self.JoinedNodifiedNodingStr=""							#<NotRepresented>
		self.JoinedModelStr=""									#<NotRepresented>
		self.JoinedModeledStr=""									#<NotRepresented>
		self.JoinedRowedDictsList=[] 								#<NotRepresented>
		self.JoinedFilteredMergedRowedDictsListTuplesList=[]		#<NotRepresented>
		#</DefineSpecificDo>

		#self.RepresentingKeyVariablesList+=['RowedIdentifiedOrderedDict','RowedNotIdentifiedOrderedDict']

	def modelAfter(self,**_ModelingVariablesDict):

		#debug
		'''
		print('Joiner modelAfter method')
		print('')
		'''

		#Join maybe
		if 'JoiningTuple' in self.ModeledDict:

			#debug
			'''
			print("self.ModeledDict['JoiningTuple'] is ",self.ModeledDict['JoiningTuple'])
			print()
			'''

			#Definition the JoinedModeledStr
			JoinedModeledStr=SYS.getDoneStrWithDoStr(self.ModeledDict['JoiningTuple'][1])

			#Add a JoinedList for the join with the joining table at this level
			self.JoinedJoinedListKeyStr=JoinedModeledStr+'JoinedList'
			self.ModeledDescriptionClass.columns[self.JoinedJoinedListKeyStr]=tables.Int64Col(shape=2)
			
			#Nodify with the JoiningNodifiedStr
			if self.ModeledDict['JoiningTuple'][0]!="":

				#debug
				'''
				print('Joiner we are going to nodify the ',self.ModeledDict['JoiningTuple'][0])
				print('')
				'''
				
				#Nodify
				self.nodify(self.ModeledDict['JoiningTuple'][0])

				#set the JoinedNodifiedKeyStrKeyStrsList
				JoinedNodifiedKeyStrsList=map(
							lambda __JoinedObjects:
							getattr(
									__JoinedObjects,
									self.NodifiedKeyStrKeyStr
									),
							self.NodifiedOrderedDict.values()
						)

				#set the Cols for the joined children 
				map(
					lambda __NodifiedKeyStrKeyStr:
					self.ModeledDescriptionClass.columns.__setitem__(
						self.NodifiedNodedStr+__NodifiedKeyStrKeyStr+JoinedModeledStr+'JoinedList',
						tables.Int64Col(shape=2)
					),
					JoinedNodifiedKeyStrsList
				)

				#Definition the JoinedOrderedDict
				JoinedOrderedSetTagStr=self.NodifiedNodedStr+'JoinedOrderedDict'
				self.__setattr__(JoinedOrderedSetTagStr,collections.OrderedDict())
				JoinedOrderedDict=getattr(self,JoinedOrderedSetTagStr)
				JoinedOrderedDict[self.JoinedJoinedListKeyStr]=[-1,-1]

				#Init the JoinedList for each child
				map(
						lambda __JoinedNodifiedKeyStr:
						JoinedOrderedDict.__setitem__(
							self.NodifiedNodedStr+__JoinedNodifiedKeyStr+self.JoinedJoinedListKeyStr,
							[-1,-1]
							),
						JoinedNodifiedKeyStrsList
					)

	def rowAfter(self,**_LocalRowingVariablesList):

		#Join maybe
		if 'JoiningTuple' in self.ModeledDict:
			
			#Join
			if 'IsJoiningBool' not in _LocalRowingVariablesList or _LocalRowingVariablesList['IsJoiningBool']:
				self.join("")

			#debug
			#print('self.JoinedOrderedDict is ',self.JoinedOrderedDict)

			#Update the self.RowedIdentifiedOrderedDic
			self.RowedIdentifiedOrderedDict.update(self.JoinedOrderedDict)

			#debug
			'''
			print('self.JoinedOrderedDict is ',self.JoinedOrderedDict)
			print('self.RowedIdentifiedOrderedDict is ',self.RowedIdentifiedOrderedDict)
			print()
			'''

	def insertBefore(self,**_LocalInsertingVariablesList):

		#debug
		'''
		print("Joiner insertBefore method")
		if hasattr(self,"StructuredKeyStr"):
			print('self.StructuredKeyStr is ',self.StructuredKeyStr)
		print('_LocalInsertingVariablesList is',_LocalInsertingVariablesList)
		print('')
		'''
		
		#Insert the joined stuff if they are not yet
		if 'JoiningTuple' in self.ModeledDict:

			#We need maybe to join if it was not already rowed
			if 'IsRowedBool' in _LocalInsertingVariablesList and _LocalInsertingVariablesList['IsRowedBool']==False:
				self.join("")

			#Definition the NodifyingStr
			#NodifyingStr=self.ModeledDict['JoiningTuple'][0]
			#NodifiedStr=SYS.getDoneStrWithDoStr(NodifyingStr)
			
			#debug
			'''
			print('Joiner insertAfter method')
			print('self.RowedIdentifiedOrderedDict is',self.RowedIdentifiedOrderedDict)
			print('self.JoinedOrderedDict is ',self.JoinedOrderedDict)
			print('')
			'''

			#Definition the NotRowedTuplesList
			NotRowedTuplesList=filter(
					lambda __JoiningTuple:
					__JoiningTuple[1][0]<0 or __JoiningTuple[1][1]<0,
					self.JoinedOrderedDict.items()
				)

			#debug
			'''
			print('NotRowedTuplesList is ',NotRowedTuplesList)
			print('')
			'''

			#Then get the corresponding NodifiedKeyStrsList
			NodifiedKeyStrsList=map(
										lambda __NodifiedKeyStr:
										self.JoinedNodifiedNodedStr.join(
											__NodifiedKeyStr.split(self.JoinedNodifiedNodedStr)[1:]
											)
										if self.JoinedNodifiedNodedStr in __NodifiedKeyStr and self.JoinedNodifiedNodedStr!=""
										else __NodifiedKeyStr,
										map(
											lambda __NotRowedTuple:
											self.JoinedJoinedListKeyStr.join(__NotRowedTuple[0].split(
														self.JoinedJoinedListKeyStr)[:-1]),
											NotRowedTuplesList
										)
									)

			#debug
			'''
			print('NodifiedKeyStrsList is ',NodifiedKeyStrsList)
			print("self.JoinedNodifiedNodeStr is ",self.JoinedNodifiedNodeStr)
			print('')
			'''

			#Insert first all the children
			InsertingVariablesList=map(
					lambda __NodifiedKeyStr:
					self['App_'+self.JoinedNodifiedNodeStr+'_'+__NodifiedKeyStr
					].insert(_LocalInsertingVariablesList['InsertingStr'])
					if __NodifiedKeyStr!=""
					else
					self.insert(self.JoinedModeledDict['ModelStr']),
					NodifiedKeyStrsList
				)
			
			#It is going to be inserted so update the self.JoinedJoinedList to the last row index
			if self.JoinedJoinedList[1]==-1:
				self.JoinedJoinedList[1]=self.JoinedTabularedTable.nrows-1

			#Get the JoinedJoinedList
			JoinedListsList=map(lambda __InsertingVariable:__InsertingVariable.JoinedJoinedList,InsertingVariablesList)

			#debug
			'''
			print('self.StructuredKeyStr is ',self.StructuredKeyStr)
			print('JoinedListsList is ',JoinedListsList)
			print('')
			'''

			#A row to reset the values plus the modeled and tabulared attributes is need but the join method doesn't need to be called one more time
			self.row(_LocalInsertingVariablesList['InsertingStr'],**{'IsJoiningBool':False})

			#Just change the __RowInt
			map(
					lambda __NotRowedTuple,__JoinedList:
					self.RowedIdentifiedOrderedDict.__setitem__(__NotRowedTuple[0],__JoinedList),
					NotRowedTuplesList,
					JoinedListsList
				)

	def retrieveBefore(self,**_RetrievingVariablesDict):

		#debug
		print('Joiner retrieveBefore method')
		print("self.ModeledDict['RetrievingIndexesListsList'] is ")
		SYS._print(self.ModeledDict['RetrievingIndexesListsList'])
		print('')

		#Check that there is the RetrievingIndexesListsList
		if 'RetrievingIndexesListsList' in self.ModeledDict:	

			#Join before
			self.join()

			'''

			#set the self.JoinedRetrievingIndexesListsList and self.ModeledDict['RetrievingIndexesListsList']
			[
				self.JoinedRetrievingIndexesListsList,
				self.ModeledDict['RetrievingIndexesListsList']
			]=SYS.groupby(
							lambda __Tuple:
							SYS.getCommonPrefixStrWithStrsList(
									[__Tuple[0],JoinStr]
								)==JoinStr,
							self.ModeledDict['RetrievingIndexesListsList']
						)

			#debug
			print('self.JoinedRetrievingIndexesListsList is ')
			SYS._print(self.JoinedRetrievingIndexesListsList)
			print("self.ModeledDict['RetrievingIndexesListsList'] is ")
			SYS._print(self.ModeledDict['RetrievingIndexesListsList'])
			print('')

			JoinedSortedDict=SYS.getSortedDictWithSortedTuplesList(
								map(
										lambda __JoinedTuple:
										(
											__JoinedTuple[0],
											(
												JoinStr.join(__JoinedTuple[1][0].split(JoinStr)[1:])
												if JoinStr in __JoinedTuple[1][0]
												else __JoinedTuple[1][0],
												__JoinedTuple[1][1]
											)
										),
										map(
												lambda __JoinedSplittedRetrievingIndexesList:
												(
													#KeyStr for the ModeledDict getting
													SYS.Node.DeepShortStr.join(
														map(
																lambda __KeyStr:
																SYS.Node.AppendShortStr+self.JoinedNodifiedNodeStr+SYS.Node.NodeStr+JoinStr.join(
																	__KeyStr.split(
																		JoinStr)[1:]
																),
																__JoinedSplittedRetrievingIndexesList[0][:-1]
															)
													)
													if len(__JoinedSplittedRetrievingIndexesList[0])>1
													else '/',
													#Tuple
													(
														#GettingStr
														__JoinedSplittedRetrievingIndexesList[0][-1]
														if len(__JoinedSplittedRetrievingIndexesList[0])>1
														else
														__JoinedSplittedRetrievingIndexesList[0][0],
														#OperatorTuple
														__JoinedSplittedRetrievingIndexesList[1]
													)
												),
												#Split the PathStr with the JoinDeepStr
												map(
														lambda __JoinedRetrievingIndexesList:
														(
																__JoinedRetrievingIndexesList[0].split(
																	JoinDeepStr
																),
																__JoinedRetrievingIndexesList[1]
														),
														self.JoinedRetrievingIndexesListsList
												)
											)
									)
							)

			#debug
			print('JoinedSortedDict is ')
			SYS._print(JoinedSortedDict)
			print('')

			#set the MergedRowedDictsListsList
			self.JoinedJoinedListKeyStr=self.JoinedModeledStr+'JoinedList'
			MergedRowedDictsListsTuplesList=map(
									lambda __AppendingGettingStr,__Joiner:
									(
										__AppendingGettingStr,
										SYS.getJoinedRowedDictsListWithJoinedListKeyStr(
											__Joiner.merge(self.JoinedModelStr).MergedRowedDictsList,
											self.JoinedJoinedListKeyStr
										)
									)
									if __Joiner!=None else (__AppendingGettingStr,[]),
									JoinedSortedDict.keys(),
									self.pick(JoinedSortedDict.keys())
								)
						

			#debug
			print('MergedRowedDictsListsTuplesList is ')
			SYS._print(MergedRowedDictsListsTuplesList)
			print('JoinedSortedDict.values() is ')
			SYS._print(JoinedSortedDict.values())
			print('')

			#set the JoinedFilteredMergedRowedDictsListsList
			self.JoinedFilteredMergedRowedDictsListTuplesList=map(
					lambda __MergedRowedDictsListsTuple,__JoinedRetrievingIndexesListsList:
					(
						__MergedRowedDictsListsTuple[0],
						map(
							lambda __MergedRowedDict:
							__MergedRowedDict,
							SYS.filterNone(
								SYS.where(
									__MergedRowedDictsListsTuple[1],
									__JoinedRetrievingIndexesListsList)
							)
						)
					),
					MergedRowedDictsListsTuplesList,
					JoinedSortedDict.values()
				)

			#debug
			print('self.JoinedFilteredMergedRowedDictsListTuplesList is ')
			SYS._print(self.JoinedFilteredMergedRowedDictsListTuplesList)
			print('JoinedSortedDict.keys() is ',JoinedSortedDict.keys())
			if hasattr(self,'StructuredKeyStr'):
				print('self.StructuredKeyStr is ',self.StructuredKeyStr)
			print('')

			#set the JoinedRetrievingIndexesListsList
			self.JoinedRetrievingIndexesListsList=map(
					lambda __JoinedFilteredMergedRowedDictsListTuple,__JoinedRetrievingKeyStr:
					(
						''.join(
							map(
								lambda __IntAndStrTuple:
								SYS.getDoneStrWithDoStr(__IntAndStrTuple[1])
								if __IntAndStrTuple[0]==0
								else __IntAndStrTuple[1],
								enumerate(
											SYS.Node.AppendShortStr.join(
											__JoinedRetrievingKeyStr.split(
												SYS.Node.AppendShortStr)[1:] 
											).split(SYS.Node.NodeStr)
										)
								)
						)+self.JoinedJoinedListKeyStr,
						(
						SYS.getIsInListBool,
						map(
								lambda __JoinedFilteredMergedRowedDict:
								__JoinedFilteredMergedRowedDict[self.JoinedJoinedListKeyStr],
								__JoinedFilteredMergedRowedDictsListTuple[1]
							)
						)
					),
					self.JoinedFilteredMergedRowedDictsListTuplesList,
					JoinedSortedDict.keys()
				)

			#debug
			print('self.JoinedRetrievingIndexesListsList is ',self.JoinedRetrievingIndexesListsList)
			print('')
			'''
			

		else:

			#debug
			print('WARNING : Joiner, you have to mention a RetrievingIndexesListsList')
			print('')

	def retrieveAfter(self,**_RetrievingVariablesDict):

		#debug
		print('Joiner retrieveAfter method')
		print('self.RetrievedFilteredRowedDictsList is ')
		SYS._print(self.RetrievedFilteredRowedDictsList)
		print('self.JoinedRetrievingIndexesListsList is ')
		SYS._print(self.JoinedRetrievingIndexesListsList)
		print('self.JoinedJoinedListKeyStr is ')
		SYS._print(self.JoinedJoinedListKeyStr)
		print('')

		#Rebound the RetrievedFilteredRowedDictsList
		self.RetrievedFilteredRowedDictsList=filter(
														lambda __Variable:
														__Variable!=None,
														SYS.where(
							self.RetrievedFilteredRowedDictsList,
							self.JoinedRetrievingIndexesListsList
							)
						)

		#debug
		print('self.RetrievedFilteredRowedDictsList is ')
		SYS._print(self.RetrievedFilteredRowedDictsList)
		print('')

	def recoverBefore(self,**_LocalRecoveringVariablesDict):

		#debug
		print('Joiner recoverBefore method')
		print('self.RetrievedFilteredRowedDictsList is ')
		SYS._print(self.RetrievedFilteredRowedDictsList)
		if hasattr(self,'StructuredKeyStr'):
				print("self['StructuredKeyStr'] is ",self.StructuredKeyStr)
		print('')

		if len(self.RetrievedFilteredRowedDictsList)==1:
				
			#debug
			'''
			print('Joiner It is good, there is one solution !')
			print('')
			'''

			#Definition a JoinedRecoveredDict
			JoinedRecoveredDict=self.RetrievedFilteredRowedDictsList[0]

			#debug
			print('Joiner JoinedRecoveredDict is ')
			SYS._print(JoinedRecoveredDict)
			print('self.JoinedNodifiedNodedStr is ',self.JoinedNodifiedNodedStr)
			if hasattr(self,'StructuredKeyStr'):
				print("self['StructuredKeyStr'] is ",self.StructuredKeyStr)
			print('')

			#Maybe we have to recover the children before
			ChildJoinersList=self.JoinedNodifiedOrderedDict.values()
			if len(ChildJoinersList)>0:

				#set each Children and recover each
				JoinedNodifiedKeyStr=self.JoinedNodifiedNodedStr+'KeyStr'
					
				#debug
				print('We are going to make recover each children before')
				if hasattr(self,'StructuredKeyStr'):
					print('self.StructuredKeyStr is ',self.StructuredKeyStr)
				print('')
				print('self.JoinedNodifiedOrderedDict.values() is ',self.JoinedNodifiedOrderedDict.values())
				print('')

				#Map a Recover
				map(
						lambda __JoinedJoiner:
						__JoinedJoiner.__setitem__(
								'/App_Model_'+self.ModeledDict['ModelingStr']+'Dict/RetrievingIndexesListsList',
								[
									(
										JoinStr+self.JoinedJoinedListKeyStr,
										(
											SYS.getIsEqualBool,
											JoinedRecoveredDict[
											self.JoinedNodifiedNodedStr+getattr(
													__JoinedJoiner,
													JoinedNodifiedKeyStr
													)+self.JoinedJoinedListKeyStr
											]
										)
									)
								]
						).recover(self.ModeledKeyStr),
						ChildJoinersList
					)

			#Definition the 
			AppendingGettingStrsList=SYS.unzip(self.JoinedFilteredMergedRowedDictsListTuplesList,[0])

			#debug
			print('Joiner maybe update first the joined model')
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

				#Definition the JoinedJoinedList
				JoinedJoinedList=JoinedRecoveredDict[self.JoinedJoinedListKeyStr]

				#debug
				print('JoinedFilteredMergedRowedDictsList is ')
				SYS._print(JoinedFilteredMergedRowedDictsList)
				print('JoinedJoinedList is ',JoinedJoinedList)
				if hasattr(self,'StructuredKeyStr'):
					print("self['StructuredKeyStr'] is ",self.StructuredKeyStr)
				print('')

				#Take the first element of self.JoinedFilteredMergedRowedDictsTuplesList which corresponds to the Joined Model at this level	
				JoinedRowedDict=next(
						RowedDict for RowedDict in JoinedFilteredMergedRowedDictsList
						if SYS.getIsEqualBool(
							RowedDict[self.JoinedJoinedListKeyStr],
							JoinedJoinedList
						)
					)

				#debug
				'''
				print('JoinedRowedDict is ',JoinedRowedDict)
				print('')
				'''

				#Update
				self.update(JoinedRowedDict.items())
			
		else:

			#debug
			print('Joiner There are multiple retrieved states')
			if hasattr(self,'StructuredKeyStr'):
				print("self['StructuredKeyStr'] is ",self.StructuredKeyStr)
			print('self.RetrievedFilteredRowedDictsList is ')
			SYS._print(self.RetrievedFilteredRowedDictsList)
			print('')

			#Stop the recover
			self.IsRecoveringBool=False


	#</DefineHookMethods>
	def join(	
				self,
				_ModelStr="",
				**_LocalJoiningVariablesDict
			):

		#debug
		print('Joiner join method')
		print('_ModelStr is ',_ModelStr)
		if hasattr(self,"StructuredKeyStr"):
			print('self.StructuredKeyStr is ',self.StructuredKeyStr)
		print('')

		#Maybe we need to refresh some modeled and tabulared attributes
		if _ModelStr!="":

			#debug
			'''
			print('_ModelStr is ',_ModelStr)
			print('')
			'''

			#row
			self.tabular(_ModelStr)

		else:

			#set again the _ModelStr
			_ModelStr=self.ModeledDict['ModelStr']

		#Init maybe the _LocalJoiningVariablesDict
		if 'IsJoiningBool' not in _LocalJoiningVariablesDict:

			#set IsScanningBool to False
			_LocalJoiningVariablesDict['IsJoiningBool']=False

			#Refresh attributes
			self.JoinedJoinedList=[-1,-1]
			self.JoinedOrderedDict=collections.OrderedDict()
			self.JoinedNodifiedOrderedDict=collections.OrderedDict()

		#Init a default False IsCheckingJoiningBool
		if 'IsCheckingJoiningBool' not in _LocalJoiningVariablesDict:
			_LocalJoiningVariablesDict['IsCheckingJoiningBool']=True

		#set the JoiningTuple
		if 'JoiningTuple' not in _LocalJoiningVariablesDict:

			#Case where there are joins
			if 'JoiningTuple' in self.ModeledDict:

				#set to the _LocalJoiningVariablesDict
				_LocalJoiningVariablesDict['JoiningTuple']=self.ModeledDict['JoiningTuple']

				#Maybe we have to structure
				if self.IsGroupedBool==False:

					#debug
					'''
					print('Join We have to structure first')
					if hasattr(self,"StructuredKeyStr"):
						print('self.StructuredKeyStr is ',self.StructuredKeyStr)
					'''
					
					#Structure
					self.structure(self.ModeledDict['JoiningTuple'][0])

			else:

				#set a default
				_LocalJoiningVariablesDict['JoiningTuple']=("","")

		#Nodify if there is the nodified objects
		if _LocalJoiningVariablesDict['IsJoiningBool']==False and _LocalJoiningVariablesDict['JoiningTuple'
		][0]!="":

			#debug
			print('Joiner we are going to nodify the ',_LocalJoiningVariablesDict['JoiningTuple'][0])
			if hasattr(self,'StructuredKeyStr'):
				print('self.StructuredKeyStr is ',self.StructuredKeyStr)
			print('')

			#Nodify
			self.nodify(_LocalJoiningVariablesDict['JoiningTuple'][0])
			self.JoinedNodifiedOrderedDict=copy.copy(self.NodifiedOrderedDict)
			self.JoinedNodifiedNodeStr=self.NodifiedNodeStr
			self.JoinedNodifiedNodedStr=SYS.getDoneStrWithDoStr(self.NodifiedNodeStr)
			self.JoinedNodifiedNodingStr=SYS.getDoneStrWithDoStr(self.NodifiedNodeStr)

			#debug
			print('self.JoinedNodifiedOrderedDict is ',self.JoinedNodifiedOrderedDict)
			print('')

		#debug
		'''
		print("_LocalJoiningVariablesDict['JoiningTuple'] is ",
			_LocalJoiningVariablesDict['JoiningTuple'])
		print('')
		'''

		#If there is a joined model
		if len(self.JoinedNodifiedOrderedDict)==0 or _LocalJoiningVariablesDict['IsJoiningBool']:

			#debug
			'''
			print('We have the right to join !')
			print("_LocalJoiningVariablesDict['IsJoiningBool']",
				_LocalJoiningVariablesDict['IsJoiningBool'])
			print('self.ModeledDict is ',self.ModeledDict)
			print('')
			'''

			#Tabular for the _JoiningRowingStr if JoiningTuple is not None
			if _LocalJoiningVariablesDict['JoiningTuple'][1]!=None:
				self.JoinedModelStr=_LocalJoiningVariablesDict['JoiningTuple'][1]
				self.JoinedModeledStr=SYS.getDoneStrWithDoStr(self.JoinedModelStr)
				self.tabular(self.JoinedModelStr)
				self.JoinedModeledDict=copy.copy(self.ModeledDict)
				self.JoinedModeledKeyStr=self.ModeledKeyStr
				self.JoinedJoinedList[0]=self.ShapedTabularedInt
				self.JoinedTabularedTable=self.TabularedTable

			#debug
			'''
			print('self.JoinedModeledDict is ',self.JoinedModeledDict)
			print('self.JoinedModeledKeyStr is ',self.JoinedModeledKeyStr)
			print('self.JoinedJoinedList is ',self.JoinedJoinedList)
			print('')
			'''

			#Check if the actual setup is already rowed
			if _LocalJoiningVariablesDict['IsCheckingJoiningBool'] and self.JoinedJoinedList[1]==-1:

				#Definition the GettingStrsList and the GettedVariablesList
				if 'ColumningTuplesList' in self.JoinedModeledDict:

					#Get the GettingStrsList and GettedVariablesList
					GettingStrsList=SYS.unzip(self.JoinedModeledDict['ColumningTuplesList'],[0])
					GettedVariablesList=self.pick(GettingStrsList)

					#debug
					'''
					print(map(
							lambda __Row:
							map(
									lambda __GettingStr,__GettedVariable:
									all(__Row[__GettingStr]==__GettedVariable),
									GettingStrsList,
									GettedVariablesList
								),
							JoinedTabularedTable.iterrows()
						)
					)
					'''

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
							self.JoinedTabularedTable.iterrows()
						)					

					#debug
					'''
					print('self.StructuredKeyStr is ',self.StructuredKeyStr)
					print('IsRowedBoolsList is ',IsRowedBoolsList)
					print('')
					'''

					#If it is rowed then set the JoinedJoinedList
					try:
						IndexInt=IsRowedBoolsList.index(True)
					except ValueError:
						IndexInt=-1
					self.JoinedJoinedList[1]=IndexInt

			#Give to itself
			JoinedOrderedSetTagStr=self.JoinedNodifiedNodedStr+'JoinedOrderedDict'
			if hasattr(self,JoinedOrderedSetTagStr):
				self.JoinedOrderedDict=getattr(self,JoinedOrderedSetTagStr)
			if self.JoinedOrderedDict==None:
				self.JoinedOrderedDict=collections.OrderedDict()
			self.JoinedOrderedDict.__setitem__(
				self.JoinedJoinedListKeyStr,self.JoinedJoinedList
			)

			if self.JoinedNodifiedNodedStr!="":
				ParentPointer=getattr(self,self.JoinedNodifiedNodedStr+'ParentPointer')
				if ParentPointer!=None:
					#Give to the Parent
					JoinedOrderedDict=getattr(ParentPointer,JoinedOrderedSetTagStr)
					JoinedOrderedDict[getattr(self,self.JoinedNodifiedNodedStr+'KeyStr'
						)+self.JoinedJoinedListKeyStr]=self.JoinedJoinedList

			#debug
			'''
			print('JoinedModeledDict is ',JoinedModeledDict)
			print('JoinedList is ',JoinedList)
			print('')
			'''

			#Tabular again to set again the ModeledDict
			self.tabular(_ModelStr)
				
		else:

			#debug
			'''
			print('This either a not last level of child or it is not yet authorized to join')
			print('self.JoinedNodifiedOrderedDict.values() is ',self.JoinedNodifiedOrderedDict.values())
			print('len(self.NodifiedOrderedDict.values()) is ',len(self.NodifiedOrderedDict.values()))
			print("_LocalJoiningVariablesDict['IsJoiningBool']",_LocalJoiningVariablesDict['IsJoiningBool'])
			print('so join the deeper children groups first')
			print('')
			'''

			map(
					lambda __JoiningObjects:
					__JoiningObjects.join(
											self.ModeledDict['ModelStr'],
											**_LocalJoiningVariablesDict
										),
					self.JoinedNodifiedOrderedDict.values()
				)

			'''
			print('The deeper children groups are joined now')
			print('So join here !')
			print('')
			'''

			self.join(
						self.ModeledDict['ModelStr'],
						**dict(
								_LocalJoiningVariablesDict,**{'IsJoiningBool':True}
							)
					)


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
													('tabular',{'ArgsVariable':""}),
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
									).tabular(
									).row(
									).insert("Result"
									).hdfclose()

	#Return the object itself
	return "Objects is : \n"+SYS.represent(
		Joiner
		)+'\n\n\n'+SYS.represent(os.popen('/usr/local/bin/h5ls -dlr '+Joiner.HdformatingPathStr
		).read())
#</DefineAttestingFunctions>
