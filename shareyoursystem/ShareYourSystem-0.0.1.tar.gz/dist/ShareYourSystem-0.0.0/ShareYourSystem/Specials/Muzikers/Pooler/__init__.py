# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Pooler...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Systemer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import itertools
#</ImportSpecificModules>


#<DefineClass>
@DecorationClass()
class PoolerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
									'PoolingSubsetLengthInt',
									'PoolingSetLengthInt',
									'PooledIntsListsList'
								]

	def default_init(self,
						_PoolingSubsetLengthInt=0,
						_PoolingSetLengthInt=0,
						_PooledIntsListsList=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_pool(self):

		#debug
		self.debug(('self.',self,[
									'PoolingSubsetLengthInt',
									'PoolingSetLengthInt'
								]))

		#Combine
		self.PooledIntsListsList=list(
			itertools.combinations(
				xrange(self.PoolingSetLengthInt),
				self.PoolingSubsetLengthInt
			)
		)
		
		#debug
		'''
		self.debug(('self.',self,['PooledIntsListsList']))
		'''

		#filter only the one with the pitch 0
		self.PooledIntsListsList=SYS._filter(
			lambda __PooledInt:
			__PooledInt[0]==0,
			self.PooledIntsListsList
		)

#</DefineClass>
