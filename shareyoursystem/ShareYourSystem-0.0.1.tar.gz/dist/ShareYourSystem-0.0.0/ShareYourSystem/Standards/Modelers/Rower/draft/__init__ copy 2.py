# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Rower helps to set rowed lines in a Databaser from pointed attributes,
ready then to be inserted in a table.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Modeler"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import copy
from ShareYourSystem.Standards.Itemizers import Getter
#</ImportSpecificModules>

#<DefineFunctions>
def getRowedDictsListWithTable(_Table):
	return map(
			lambda __Row:
			dict(
				zip(
					_Table.colnames,
					map(
						lambda __ColumnStr:
						__Row[__ColumnStr],
						_Table.colnames
					)
				)
			),
			_Table.iterrows()
		)
#</DefineFunctions>


#<DefineClass>
@DecorationClass(
	**{'ClassingSwitchMethodStrsList':["row"]}
)
class RowerClass(
					BaseClass
				):
	
	def default_init(
					self,
					_RowGetStrToColumnStrOrderedDict=None,
					_RowHdfColumnStrsList=None,
					_RowingKeyStrsList={
							'DefaultValueType':property,
							'PropertyInitVariable':[],
							'PropertyDocStr':''
					},
					_RowedMongoPickOrderedDict=None, 																
					_RowedHdfPickOrderedDict=None,
					_RowedMongoIsBoolsList=None,	 
					_RowedHdfIsBoolsList=None,	
					_RowedMongoIsBool=False,
					_RowedHdfIsBool=False,
					_RowedMongoIndexInt=-1,
					_RowedHdfIndexInt=-1,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
		
	def do_row(self):
		""""""
		
		#debug
		'''
		self.debug('We row here')
		'''

		#Check	
		if self.ModelDeriveControllerVariable!=None:
			
			#debug
			'''
			self.ModelDeriveControllerVariable.debug('ParentSpeaking...')
			'''

			#Check
			if self.ModelingMongoBool:

				#Update
				self.RowedMongoPickOrderedDict.update(
					zip(
						self.RowingKeyStrsList,
						self.ModelDeriveControllerVariable[Getter.GetMapStr](
							*self.ModelKeyStrsList
						).ItemizedMapValueVariablesList
					)
				)

				#debug
				'''
				self.debug(
					[
						('self.',self,[
										'RowedMongoPickOrderedDict',
										'TabledMongoCollection'
									]
						),
						'list(self.TabledMongoCollection.find()) is '+SYS._str(
							list(self.TabledMongoCollection.find()))
					]
				)
				'''

				#Check if it was already rowed
				self.RowedMongoIsBoolsList=map(
						lambda __Row:
						all(
							map(
									lambda __RowedItemTuple:
									SYS.getIsEqualBool(
														__Row[__RowedItemTuple[0]],
														__RowedItemTuple[1]
													),
									self.RowedMongoPickOrderedDict.items()
								)
						),
						self.TabledMongoCollection.find()
					)

				#debug
				'''
				self.debug(('self.',self,[
						'RowedMongoIsBoolsList'
					]))
				'''

				#set
				if len(self.RowedMongoIsBoolsList)==0:
					self.RowedMongoIsBool=False
				else:
					self.RowedMongoIsBool=any(self.RowedMongoIsBoolsList)

				#Init to the len of the table
				self.RowedMongoIndexInt=len(self.RowedMongoIsBoolsList)
				
				#debug
				'''
				self.debug(('self.',self,[
						'RowedMongoIndexInt',
						'RowedMongoIsBool'
					]))
				'''
				
				#But maybe find a last index
				if self.RowedMongoIsBool: 
					if len(self.RowedMongoIsBoolsList)>0:
						self.RowedMongoIndexInt=self.RowedMongoIsBoolsList.index(True)

				#debug
				'''
				self.debug(('self.',self,['RowedMongoIsBool','RowedMongoIndexInt']))
				'''

			#Check
			if self.ModelingHdfBool:

				#debug
				'''
				self.debug('This is a hdf row here')
				'''

				#/#################/#
				# Pick the values to be rowed in the hdf variables
				#

				#debug
				'''
				self.debug(
					('self.',self,[
						'RowingKeyStrsList',
						'RowHdfColumnStrsList'
						])
				)
				'''

				#Update
				self.RowedHdfPickOrderedDict.update(
					zip(
						self.RowHdfColumnStrsList,
						self.ModelDeriveControllerVariable[Getter.GetMapStr](
							*self.RowingKeyStrsList
						).ItemizedMapValueVariablesList
					)
				)

				#debug
				'''
				self.debug(
					[
						'Ok we have almost end the row',
						('self.',self,[
									'RowedHdfPickOrderedDict',
								]
						),
						'Check now if it is a new row'
					]
				)
				'''
				
				#/#################/#
				# Check if it is a new row
				#

				#Check if it was already rowed
				self.RowedHdfIsBoolsList=map(
						lambda __Row:
						all(
							map(
									lambda __RowedItemTuple:
									SYS.getIsEqualBool(
														__Row[__RowedItemTuple[0]],
														__RowedItemTuple[1]
													),
									self.RowedHdfPickOrderedDict.items()
								)
							),
						self.TabledHdfTable.iterrows()
					)

				#debug
				'''
				self.debug(
					[
						('self.',self,['RowedHdfIsBoolsList'])
					]
				)	
				'''

				#set
				if len(self.RowedHdfIsBoolsList)==0:
					self.RowedHdfIsBool=False
				else:
					self.RowedHdfIsBool=any(self.RowedHdfIsBoolsList)

				#Init to the len of the table
				self.RowedHdfIndexInt=self.TabledHdfTable.nrows

				#But maybe find a last index
				if self.RowedHdfIsBool: 
					if len(self.RowedHdfIsBoolsList)>0:
						self.RowedHdfIndexInt=self.RowedHdfIsBoolsList.index(True)

				#debug
				'''
				self.debug(
					[
						('self.',self,['RowedHdfIsBool','RowedHdfIndexInt'])
					]
				)
				'''
	
	def propertize_setModelingDescriptionTuplesList(self,_SettingValueVariable):

		#debug
		'''
		self.debug(
					[
						'Before setting ModelingDescriptionTuplesList',
						('self.',self,['ModelingDescriptionTuplesList']),
						'_SettingValueVariable is '+str(_SettingValueVariable)
					]
				)
		'''

		#set
		BaseClass.propertize_setModelingDescriptionTuplesList(self,_SettingValueVariable)

		#debug
		'''
		self.debug(
					[
						'After',
						('self.',self,['ModelingDescriptionTuplesList']),
						'We bind with RowGetStrToColumnStrOrderedDict setting',
					]
				)
		'''

		#Bind with RowGetStrToColumnStrOrderedDict setting
		self.RowGetStrToColumnStrOrderedDict=collections.OrderedDict(
				map(
					lambda _ModelingSealTuple:
					(
						_ModelingSealTuple[0],
						_ModelingSealTuple[1]
					),
					self._ModelingDescriptionTuplesList
					)
				)

		#debug
		'''
		self.debug(
					[
						('self.',self,['RowGetStrToColumnStrOrderedDict'])
					]
				)
		'''

	def propertize_setRowingKeyStrsList(self,_SettingValueVariable):
		
		#debug
		'''
		self.debug('_SettingValueVariable '+str(_SettingValueVariable))
		'''

		#set
		self._RowingKeyStrsList=_SettingValueVariable

		#Check
		if len(self.ModelingDescriptionTuplesList)>0:
			self.ModelingHdfBool=True

		#Check
		if self.ModelingHdfBool:

			#debug
			'''
			self.debug(
							[
								'bind with RowHdfColumnStrsList setting',
								('self.',self,['RowGetStrToColumnStrOrderedDict'])
							]
						)
			'''
			
			#Bind with 
			self.RowHdfColumnStrsList=map(
					lambda __RowingGetStr:
					self.RowGetStrToColumnStrOrderedDict[__RowingGetStr],
					_SettingValueVariable
				)

			#debug
			'''
			self.debug(('self.',self,['RowHdfColumnStrsList']))
			'''
		
#</DefineClass>

#</DefinePrint>
RowerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'RowingKeyStrsList',
		'RowGetStrToColumnStrOrderedDict',
		'RowHdfColumnStrsList',	
		'RowedMongoPickOrderedDict',																									
		'RowedHdfPickOrderedDict',
		'RowedMongoIsBoolsList',
		'RowedHdfIsBoolsList',
		'RowedMongoIsBool',
		'RowedHdfIsBool',
		'RowedMongoIndexInt',
		'RowedHdfIndexInt'
	]
)
#<DefinePrint>
