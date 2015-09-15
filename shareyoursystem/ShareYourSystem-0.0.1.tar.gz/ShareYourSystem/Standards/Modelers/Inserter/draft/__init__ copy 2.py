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
from ShareYourSystem.Standards.Itemizers import Getter
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class InserterClass(
					BaseClass,
				):
	
	def default_init(self,
					_InsertedNotRowGetStrsList=None,
					_InsertedNotRowColumnStrsList=None,
					_InsertedMongoNotRowPickOrderedDict=None,
					_InsertedHdfNotRowPickOrderedDict=None,
					_InsertedIndexInt=-1,	
					_InsertedItemTuplesList=None,	
					**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
			
	def propertize_setRowingKeyStrsList(self,_SettingValueVariable):
		
		#Hook
		BaseClass.propertize_setRowingKeyStrsList(self,_SettingValueVariable)

		#Bind 
		self.InsertedNotRowGetStrsList=set(self.ModelKeyStrsList
			)-set(
				self.RowingKeyStrsList
			)

		#set
		if self.ModelingHdfBool:
			self.InsertedNotRowColumnStrsList=map(
				lambda __NotRowGetStr:
				self.RowGetStrToColumnStrOrderedDict[__NotRowGetStr],
				self.InsertedNotRowGetStrsList
			)

	def do_insert(self,**_KwargVariablesDict):
		""" """

		#/################/#
		# Check the row before
		#

		#debug
		'''
		self.debug('row maybe before...')
		'''
		
		#reset
		self.setDone(Rower.RowerClass)

		#row first
		self.row()

		#debug
		'''
		self.debug(
					('self.',self,['RowedIsBool'])
				)
		self.NodePointDeriveNoder.debug([
				('NOTE : ...ParentSpeaking...')
			])
		'''

		"""
		map(
				lambda __InitVariable:
				setattr(
					self,
					__KeyStr,
					SYS.getInitiatedVariableWithKeyStr(__KeyStr)	
				) if __InitVariable==None else None,
				map(
						lambda __KeyStr:
						(
							__KeyStr,
							getattr(self,__KeyStr)
						),
						[
							'InsertedNotRowPickOrderedDict',
							'InsertedNotRowGetStrsList',
							'InsertedNotRowGetStrsList',
							'InsertedNotRowPickOrderedDict'
						]
					)
			)
		"""

		#debug
		'''
		self.debug(('self.',self,['InsertedNotRowPickOrderedDict']))
		'''
		
		#Check
		if self.ModelingMongoBool:

			#/#################/#
			# Check if the row is unique
			#

			#Debug
			'''
			self.debug(
				[
					'We are going to row mongo',
					('self.',self,[
						'RowedMongoIsBoolsList'
						]),
					'self.TabledMongoCollection.find().count() is '+str(
						self.TabledMongoCollection.find().count()),
					'len(self.RowedMongoIsBoolsList) is '+str(len(self.RowedMongoIsBoolsList))
				]
			)
			'''
			
			#Append and row if it is new
			if self.RowedMongoIsBool==False and self.TabledMongoCollection.find(
				).count()==len(self.RowedMongoIsBoolsList):

				#Check
				if self.TabledMongoCollection!=None:

					#debug
					'''
					self.debug(
						[
							'This is a new collection row',
							('self.',self,[
										'RowingKeyStrsList',
										'InsertedNotRowGetStrsList'
									]),
							'Before update',
							('self.',self,['InsertedMongoNotRowPickOrderedDict'])
						]
					)
					'''

					#Pick and update				
					self.InsertedMongoNotRowPickOrderedDict.update(
						zip(
								self.InsertedNotRowGetStrsList,
								self.ModelDeriveControllerVariable[
									Getter.GetMapStr
								](
									*self.InsertedNotRowGetStrsList
								).ItemizedMapValueVariablesList
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
									'TabledMongoCollection'
								])
						)
					'''

					#insert
					self.TabledMongoCollection.insert(
						dict(self.InsertedItemTuplesList)
					)

					#Define
					InsertedCursor=self.TabledMongoCollection.find()

					#debug
					'''
					self.debug('list(InsertedCursor) is '+SYS._str(list(InsertedCursor)))
					'''

		#Check
		if self.ModelingHdfBool:

			#/#################/#
			# Check if the row is unique
			#

			#Debug
			'''
			self.debug(
				[
					'We are going to row hdf',
					('self.',self,[
						'RowedHdfIsBool'
						]),
					'len(self.RowedHdfIsBoolsList) is '+str(len(self.RowedHdfIsBoolsList)),
					'self.TabledHdfTable.nrows is '+str(self.TabledHdfTable.nrows)
				]
			)
			'''

			#Append and row if it is new
			if self.RowedHdfIsBool==False and len(
				self.RowedHdfIsBoolsList)==self.TabledHdfTable.nrows:

				#Check
				if self.TabledHdfTable!=None:

					#debug
					'''
					self.debug('This is a new hdf row')
					'''

					#Get the row
					Row=None
					Row=self.TabledHdfTable.row

					#debug
					'''
					self.debug(
						[
							'We pick in the controller the values',
							('self.',self,[
								'InsertedNotRowGetStrsList'
							])
						]
					)
					'''

					#Pick and update				
					self.InsertedHdfNotRowPickOrderedDict.update(
						zip(
								self.InsertedNotRowGetStrsList,
								self.ModelDeriveControllerVariable[
								Getter.GetMapStr](
									*self.InsertedNotRowGetStrsList
									).ItemizedMapValueVariablesList
							)
					)

					#debug
					'''
					self.debug(('self.',self,[
												'RowedPickOrderedDict',
												'InsertedHdfNotRowPickOrderedDict'
											]))
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
							#'Colnames are : '+str(self.TabledHdfTable.colnames),
							#'self.TabledHdfTable is '+str(dir(self.TabledHdfTable)),
							#'self.ModeledDescriptionClass is '+(str(self.ModeledDescriptionClass.columns) if hasattr(self.ModeledDescriptionClass,'columns') else ""),
							#'Row is '+str(dir(Row)),
							#'Row.table is '+str(Row.table),
							#'TabularedHdfTablesOrderedDict is '+str(self.TabularedHdfTablesOrderedDict)
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
					self.debug('The Row setting was good, so append insert')
					'''

					#Append and Insert
					Row.append()
					self.TabledHdfTable.flush()
					
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
		
		#setSwitch row
		self.setSwitch('row')

#</DefineClass>

#</DefinePrint>
InserterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'InsertedNotRowGetStrsList',
		'InsertedNotRowColumnStrsList',
		'InsertedMongoNotRowPickOrderedDict',
		'InsertedHdfNotRowPickOrderedDict',
		'InsertedIndexInt',
		'InsertedItemTuplesList'
	]
)
#<DefinePrint>
