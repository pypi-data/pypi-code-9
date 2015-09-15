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
from ShareYourSystem.Standards.Controllers import Controller
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
					_RowKeyStrToColumnStrOrderedDict=None,
					_RowHdfColumnStrsList=None,
					_RowingKeyStrsList=None,
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
		self.debug(
			[
				'We row here'
			]
		)
		'''

		#Check	
		if self.ModeledParentControllerDeriveModelerVariable!=None:
			
			#debug
			'''
			self.ModeledParentControllerDeriveModelerVariable.debug('ParentSpeaking...')
			'''

			#Check
			if self.ModelMongoBool:

				#Update
				self.RowedMongoPickOrderedDict.update(
					zip(
						self.RowingKeyStrsList,
						#self.ModeledParentControllerDeriveModelerVariable[Getter.GetMapStr](
						#	*self.ModelKeyStrsList
						#).ItemizedMapValueVariablesList
						self.ModeledParentControllerDeriveModelerVariable.mapGet(
							self.ModelKeyStrsList
						)
					)
				)

				#debug
				'''
				self.debug(
					[
						('self.',self,[
										'RowedMongoPickOrderedDict',
										'ModeledMongoCollection'
									]
						),
						'list(self.ModeledMongoCollection.find()) is '+SYS._str(
							list(self.ModeledMongoCollection.find()))
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
						self.ModeledMongoCollection.find()
					)

				#debug
				'''
				self.debug(
					[
						('self.',self,[
							'RowedMongoIsBoolsList'
						]),
						'Maybe there is now row or no rowing Key str ...so it is false already',
						'len(self.RowedMongoIsBoolsList)==0 is ',
						str(len(self.RowedMongoIsBoolsList)==0),
						'len(self.RowedMongoPickOrderedDict)==0 is',
						str(len(self.RowedMongoPickOrderedDict))
					]
				)
				'''

				#set
				if len(self.RowedMongoIsBoolsList)==0 or len(self.RowedMongoPickOrderedDict)==0:
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
			if self.ModelHdfBool:

				#debug
				'''
				self.debug('This is a hdf row here')
				'''

				#/##################/#
				# First check the good size
				#

				if self.RowKeyStrToColumnStrOrderedDict==None or len(
					self.ModelingDescriptionTuplesList)!=len(
					self.RowKeyStrToColumnStrOrderedDict):

					#Bind with RowGetStrToColumnStrOrderedDict setting
					self.RowKeyStrToColumnStrOrderedDict=collections.OrderedDict(
							map(
								lambda _ModelingSealTuple:
								(
									_ModelingSealTuple[0],
									_ModelingSealTuple[1]
								),
								self._ModelingDescriptionTuplesList
								)
							)

					#Bind with 
					self.RowHdfColumnStrsList=map(
							lambda __RowingKeyStr:
							self.RowKeyStrToColumnStrOrderedDict[__RowingKeyStr],
							self.RowingKeyStrsList
						)

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
						#self.ModeledParentControllerDeriveModelerVariable[Getter.GetMapStr](
						#	*self.RowingKeyStrsList
						#).ItemizedMapValueVariablesList
						self.ModeledParentControllerDeriveModelerVariable.mapGet(
							self.RowingKeyStrsList
						)
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
						self.ModeledHdfTable.iterrows()
					)

				#debug
				'''
				self.debug(
					[
						'Is is a new row ?',
						('self.',self,['RowedHdfIsBoolsList']),
						'Maybe there is now row or no rowing Key str ...so it is false already',
						'len(self.RowedHdfIsBoolsList)==0 is ',
						str(len(self.RowedHdfIsBoolsList)==0),
						'len(self.RowedHdfPickOrderedDict)==0 is',
						str(len(self.RowedHdfPickOrderedDict))
					]
				)	
				'''

				#set
				if len(self.RowedHdfIsBoolsList)==0 or len(self.RowedHdfPickOrderedDict)==0:
					self.RowedHdfIsBool=False
				else:
					self.RowedHdfIsBool=any(self.RowedHdfIsBoolsList)

				#Init to the len of the table
				self.RowedHdfIndexInt=self.ModeledHdfTable.nrows

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
#</DefineClass>

#<DefineLocals>
Controller.ModelsClass.ManagingValueClass=RowerClass
#<DefineLocals>

#</DefinePrint>
RowerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'RowingKeyStrsList',
		'RowHdfColumnStrsList',	
		'RowKeyStrToColumnStrOrderedDict',
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
