# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Grider instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Storer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import itertools
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class GriderClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
						'GridingScanTuplesList',
						'GridedGetKeyStrsList',
						'GridedValueVariablesTuplesList',
						'GridedComponentRetrieveListsList',
						'GridedScanRetrieveListsList'
					]

	def default_init(
			self,
			_GridingScanTuplesList=None,
			_GridedGetKeyStrsList=None,
			_GridedValueVariablesTuplesList=None,
			_GridedComponentRetrieveListsList=None,
			_GridedScanRetrieveListsList=None,
			**_KwargVariablesDict
		):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
	
	def do_grid(self):
	
		#just for init
		self.store(_InsertIsBool=False)

		#grid before in all the components
		self.GridedComponentRetrieveListsList=map(
				lambda __DeriveGrider:
				__DeriveGrider.grid().GridedScanRetrieveListsList,
				self.OrganizedComponentCollectionOrderedDict.values()
			)

		#debug
		self.debug(('self.',self,['GridedComponentRetrieveListsList']))

		#set the GridedGettingStrsList
		self.GridedGetKeyStrsList=SYS.unzip(
			self.GridingScanTuplesList,[0]
		)

		#scan the values of this model
		self.GridedValueVariablesTuplesList=list(
				itertools.product(
					*SYS.unzip(
						self.GridingScanTuplesList,[1]
					)
				)
		)

		#set
		self.StoringInsertIsBool=True
		
		#map an update and a store for each combination
		self.GridedScanRetrieveListsList=map(
				lambda __GridedValueVariablesTuple:
				self.update(
					zip(
						self.GridedGetKeyStrsList, 
						__GridedValueVariablesTuple
					)
				).store(
				).OrganizedTopDeriveDatabaserVariable.pick(
					['TabledInt','RowedIndexInt']
				),
				self.GridedValueVariablesTuplesList
			)

		#debug
		'''
		self.debug(('self.',self,['GridedScanRetrieveListsList']))
		'''


#</DefineClass>

