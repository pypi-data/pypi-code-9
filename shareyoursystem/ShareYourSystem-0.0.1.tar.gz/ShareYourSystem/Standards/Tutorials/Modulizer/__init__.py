# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Featurer instances helps for defining Databaser where all 
the rowed variables are identifying items. 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Controller"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import numpy as np
from ShareYourSystem.Functers import Outputer
from ShareYourSystem.Tutorials import Multiplier
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ModulizerClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
									'ModulizingPowerFloat',
									'ModulizedTotalFloat'
								]
								
	def __init__(self,
						_ModulizingPowerFloat=0.5,
						_ModulizedTotalFloat=0.,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)


		#Build the output hierarchy
		self.update(
						[
							('<Output>RealMultiplier',Multiplier.MultiplierClass()),
							('<Output>ImageMultiplier',Multiplier.MultiplierClass()),
						]
					)
						
	@Outputer.OutputerClass()
	def do_modulize(self):
		
		#debug
		'''
		self.debug(('self.',self,['<Group>']))
		'''

		#set the ModulizedTotalFloat
		self.ModulizedTotalFloat=np.power(
			sum(
				map(
					lambda __OutputedDeriveMultiplier:
					__OutputedDeriveMultiplier.MultipliedTotalInt,
					self['<Output>']
				)
			),
			self.ModulizingPowerFloat
		)


#</DefineClass>