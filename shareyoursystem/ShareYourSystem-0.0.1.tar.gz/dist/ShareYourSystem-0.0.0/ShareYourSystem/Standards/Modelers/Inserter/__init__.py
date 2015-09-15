# -*- coding: utf-8 -*-
"""

<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Inserter instances can insert a RowedVariablesList into a table
checking maybe before if this line is new in the table or not
depending on identifying items.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
import collections
BaseModuleStr="ShareYourSystem.Standards.Modelers.Rower"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Rower=BaseModule
from ShareYourSystem.Standards.Itemizers import Getter,Setter
from ShareYourSystem.Standards.Modelers import Modeler
from ShareYourSystem.Standards.Controllers import Controller
import copy
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class InserterClass(
					BaseClass,
				):
	
	def default_init(self,
					_InsertedNotRowKeyStrsList=None,
					_InsertedNotRowColumnStrsList=None,
					_InsertedMongoNotRowPickOrderedDict=None,
					_InsertedHdfNotRowPickOrderedDict=None,
					_InsertedIndexInt=-1,	
					_InsertedItemTuplesList=None,	
					_InsertedErrorBool=False,
					**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
			
	def do_insert(self,**_KwargVariablesDict):
		""" """

		#/################/#
		# Check the row before
		#

		#debug
		'''
		self.debug(
			[
				'row maybe before...',
				'self.getSwitch(\'row\') is',
				SYS.indent(self.getSwitch('row'))
			]
		)
		'''
		
		#reset
		self.setDone(Rower.RowerClass)

		#row first
		self.row()

		#debug
		'''
		self.debug(
			[
				('self.',self,[
					'InsertedMongoNotRowPickOrderedDict',
					'InsertedHdfNotRowPickOrderedDict'
				])
			]
		)
		'''

		#/###################/#
		# set
		# 

		#Bind 
		self.InsertedNotRowKeyStrsList=set(self.ModelKeyStrsList
			)-set(
				self.RowingKeyStrsList
			)

		#Check
		if self.ModelMongoBool:

			#/#################/#
			# Check if the row is unique
			#

			#Debug
			'''
			self.debug(
				[
					'We are mongo insert here',
					('self.',self,[
						'RowedMongoIsBoolsList'
						]),
					'self.ModeledMongoCollection.find().count() is '+str(
						self.ModeledMongoCollection.find().count()),
					'len(self.RowedMongoIsBoolsList) is '+str(len(self.RowedMongoIsBoolsList))
				]
			)
			'''
			
			#Append and row if it is new
			if self.RowedMongoIsBool==False and self.ModeledMongoCollection.find(
				).count()==len(self.RowedMongoIsBoolsList):

				#Check
				if self.ModeledMongoCollection!=None:

					#debug
					'''
					self.debug(
						[
							'This is a new collection row',
							('self.',self,[
										'RowingKeyStrsList',
										'InsertedNotRowKeyStrsList'
									]),
							'Before update',
							('self.',self,['InsertedMongoNotRowPickOrderedDict'])
						]
					)
					'''

					#Pick and update				
					self.InsertedMongoNotRowPickOrderedDict.update(
						zip(
								self.InsertedNotRowKeyStrsList,
								#self.ModeledParentControllerDeriveModelerVariable[
								#	Getter.GetMapStr
								#](
								#	*self.InsertedNotRowKeyStrsList
								#).ItemizedMapValueVariablesList
								self.ModeledParentControllerDeriveModelerVariable.mapGet(
									self.InsertedNotRowKeyStrsList
								)
							)
					)

					#debug
					'''
					self.debug(
						[
							'After update',
							('self.',self,['InsertedMongoNotRowPickOrderedDict'])
						]
					)
					'''
					
					#Definition the InsertedItemTuplesList
					self.InsertedItemTuplesList=[
											('RowInt',self.RowedMongoIndexInt)
										]+self.RowedMongoPickOrderedDict.items(
					)+self.InsertedMongoNotRowPickOrderedDict.items()

					#debug
					'''
					self.debug(
							('self.',self,[
									'InsertedItemTuplesList',
									'ModeledMongoCollection'
								])
						)
					'''

					#insert
					self.ModeledMongoCollection.insert(
						dict(self.InsertedItemTuplesList)
					)

					#Define
					InsertedCursor=self.ModeledMongoCollection.find()

					#debug
					'''
					self.debug('list(InsertedCursor) is '+SYS._str(list(InsertedCursor)))
					'''

		#Check
		if self.ModelHdfBool:

			#map
			self.InsertedNotRowColumnStrsList=map(
				lambda __NotRowKeyStr:
				self.RowKeyStrToColumnStrOrderedDict[__NotRowKeyStr],
				self.InsertedNotRowKeyStrsList
			)

			#/#################/#
			# Check if the row is unique
			#

			#Debug
			'''
			self.debug(
				[
					'We are hdf insert here',
					('self.',self,[
						'RowedHdfIsBool'
						]),
					'len(self.RowedHdfIsBoolsList) is '+str(len(self.RowedHdfIsBoolsList)),
					'self.ModeledHdfTable.nrows is '+str(self.ModeledHdfTable.nrows)
				]
			)
			'''

			#Append and row if it is new
			if self.RowedHdfIsBool==False and len(
				self.RowedHdfIsBoolsList)==self.ModeledHdfTable.nrows:

				#Check
				if self.ModeledHdfTable!=None:

					#debug
					'''
					self.debug('This is a new hdf row')
					'''

					#Get the row
					Row=None
					Row=self.ModeledHdfTable.row

					#debug
					'''
					self.debug(
						[
							'We pick in the controller the values',
							('self.',self,[
								'InsertedNotRowKeyStrsList'
							])
						]
					)
					'''

					#Pick and update				
					self.InsertedHdfNotRowPickOrderedDict.update(
						zip(
								self.InsertedNotRowKeyStrsList,
								self.ModeledParentControllerDeriveModelerVariable[
									Getter.GetMapStr
								](
									*self.InsertedNotRowKeyStrsList
									).ItemizedMapValueVariablesList
							)
					)

					#debug
					'''
					self.debug(
						[
							'We prepare the InsertedItemTuplesList',
							('self.',self,[
											'RowedHdfPickOrderedDict',
											'InsertedHdfNotRowPickOrderedDict'
										])
						]
					)
					'''

					#Definition the InsertedItemTuplesList
					self.InsertedItemTuplesList=[
											('RowInt',self.RowedHdfIndexInt)
										]+self.RowedHdfPickOrderedDict.items(
					)+self.InsertedHdfNotRowPickOrderedDict.items()
							
					#debug
					'''
					self.debug(
						[
							'This is a new hdf row',
							('self.',self,['InsertedItemTuplesList'])
							#'Colnames are : '+str(self.ModeledHdfTable.colnames),
							#'self.ModeledHdfTable is '+str(dir(self.ModeledHdfTable)),
							#'self.ModeledDescriptionClass is '+(str(self.ModeledDescriptionClass.columns) if hasattr(self.ModeledDescriptionClass,'columns') else ""),
							#'Row is '+str(dir(Row)),
							#'Row.table is '+str(Row.table),
							#'TabularedHdfTablesOrderedDict is '+str(self.TabularedHdfTablesOrderedDict)
						]
					)
					'''
					
					#/###################/#
					# Watch... The list or arrays needs to be at least one dimension
					#

					#debug
					'''
					self.debug(
						[
							'We filter the items that have null size...',
							('self.',self,['InsertedItemTuplesList'])
						]
					)
					'''

					#filter
					self.InsertedItemTuplesList=SYS._filter(
						lambda __InsertedItemTuple:
						hasattr(
							__InsertedItemTuple[1],
							'__len__'
						)==False or len(__InsertedItemTuple[1])!=0,
						self.InsertedItemTuplesList
					)

					try:

						#debug
						'''
						self.debug(
								[
									'Ok now we try to append in the rows',
									('self.',self,['InsertedItemTuplesList'])
								]
							)
						'''

						#set
						map(
								lambda __InsertingTuple:
								Row.__setitem__(*__InsertingTuple),
								self.InsertedItemTuplesList
							)

						#debug
						'''
						self.debug(
								[
									'It has worked !'
								]
							)
						'''

					except ValueError:

						#debug
						'''
						self.debug(
								[
									'It hasn\'t worked !',
									'Check if we have already tried to change the shapes',
									('self.',self,['InsertedErrorBool'])
								]
							)
						'''

						#Check
						if self.InsertedErrorBool==False:

							#debug
							'''
							self.debug(
									[
										'First try to change shapes !',
										'so find the shape that was not good'
									]
								)
							'''

							#set
							self.InsertedErrorBool=True

							#/###################/#
							# Then find where the shape was not good
							#

							#Definition the InsertedOldDimensionIntsListsList
							InsertedOldDimensionIntsList=map(
									lambda __ModeledDescriptionDimensionGetKeyStrsList:
									self.ModeledParentControllerDeriveModelerVariable[Getter.GetMapStr](
										__ModeledDescriptionDimensionGetKeyStrsList
									).ItemizedMapValueVariablesList,
									self.ModeledDescriptionDimensionGetKeyStrsListsList
								)

							#import numpy
							import numpy as np

							#Definition the InsertedNewDimensionIntsListsList
							InsertedNewDimensionIntsListsList=map(
								lambda __ModeledDescriptionGetKeyStr:
								list(
										np.shape(
											self.ModeledParentControllerDeriveModelerVariable[
												__ModeledDescriptionGetKeyStr
											]
										)
								),
								self.ModeledDescriptionGetKeyStrsList
							)

							#debug
							'''
							self.debug(
								[
									('vars ',vars(),
											[
												'InsertedOldDimensionIntsList',
												'InsertedNewDimensionIntsListsList'
											]),
									('self.',self,[
											'ModeledDescriptionDimensionGetKeyStrsListsList'
										])
								]
							)
							'''

							#set the shaping attributes to their new values
							map(
									lambda __ModeledDescriptionDimensionGetKeyStrsList,__InsertedOldDimensionList,__InsertedNewDimensionList:
									self.ModeledParentControllerDeriveModelerVariable[
											Setter.SetMapStr
										](
										zip(
											__ModeledDescriptionDimensionGetKeyStrsList,
											__InsertedNewDimensionList
											)
									) if __InsertedNewDimensionList!=__InsertedOldDimensionList
									else None,
									self.ModeledDescriptionDimensionGetKeyStrsListsList,
									InsertedOldDimensionIntsList,
									InsertedNewDimensionIntsListsList
								)

							#debug
							'''
							self.debug(
									[
										'Ok we have updated the shaping variables'
									]
								)
							'''

							#/###################/#
							# Reset the configurating methods
							#

							#debug
							'''
							self.debug(
									[
										'Refind the original ModelingDescriptionTuplesList',
										('self.',self,[
											'ModelingDescriptionTuplesList',
											'ModelDescriptionTuplesList'
										])
									]
								)
							'''

							#Keep the old ModelDescription
							self.ModelingDescriptionTuplesList=copy.copy(
								self.ModelDescriptionTuplesList
							)

							#switch model
							self.setSwitch('model')

							#setDone
							self.setDone(
								[
									Modeler.ModelerClass,
								]
							)
							
							#debug
							'''
							self.debug(
									[
										'Now we remodel...',
										('self.',self,[
											'WatchBeforeModelWithModelerBool',
											'ModelingDescriptionTuplesList'
										])
									]
								)
							'''

							#model to relaunch everything
							self.model()

							#debug
							'''
							self.debug(
									[
										'Now we have remodeled...',
										('self.',self,[
											'ModelingDescriptionTuplesList'
										])
									]
								)
							'''

							#/###################/#
							# insert again
							#

							#debug
							'''
							self.debug(
								[
									'Ok model again is done, so now we insert'
								]
							)
							'''

							#switch row
							self.setSwitch('row')

							#insert 
							self.MroClassesDict['InserterClass'].insert(self)

							#debug
							'''
							self.debug(
								[
									'Cool it seems that insert worked now'
								]
							)
							'''
							
							#set
							self.InsertedErrorBool=False

						#Check
						else:

							#debug
							self.debug(
								[	
									'Nope definitely that is not working...'
								]
							)

					#/###################/#
					# Finish with append and flush
					#

					#debug
					'''
					self.debug('The Row setting was good, so append insert')
					'''

					#Append and Insert
					Row.append()
				
					#flush
					self.ModeledHdfTable.flush()

			else:

				#debug
				'''
				self.debug(
							[
								'This is maybe not an IdentifyingInserter',
								'Or it is already rowed',
								'self.InsertedIsBoolsList is '+str(self.InsertedIsBoolsList)
							]
						)
				'''
				pass

		#/################/#
		# setSwitch row
		#
		
		#debug
		'''
		self.debug(
			[
				'Before to leave we setSwitch row again'
			]
		)
		'''

		#setSwitch row
		self.setSwitch('row')

		#debug
		'''
		self.debug(
			[
				'self.getSwitch("row") is ',
				SYS.indent(self.getSwitch('row'))
			]
		)
		'''

#</DefineClass>

#<DefineLocals>
Controller.ModelsClass.ManagingValueClass=InserterClass
#<DefineLocals>

#</DefinePrint>
InserterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'InsertedNotRowKeyStrsList',
		'InsertedNotRowColumnStrsList',
		'InsertedMongoNotRowPickOrderedDict',
		'InsertedHdfNotRowPickOrderedDict',
		'InsertedIndexInt',
		'InsertedItemTuplesList',
		'InsertedErrorBool'
	]
)
#<DefinePrint>
