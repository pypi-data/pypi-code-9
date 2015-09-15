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

from ShareYourSystem.Functers import Triggerer
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class SumerClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
									'SumingFirstInt',
									'SumingSecondInt',
									'SumedTotalInt'
								]
								
	def __init__(self,
						_SumingFirstInt=0,
						_SumingSecondInt=0,
						_SumedTotalInt=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
						
	@Triggerer.TriggererClass(**{
									'TriggeringConditionVariable':[
										('SettingKeyVariable',(SYS.getIsInListBool,[
											'SumingFirstInt',
											'SumingSecondInt'
										]))
									]
								}
							)
	#<DefineDoMethods>
	def do_sum(self):
		
		#debug
		'''
		self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
		'''

		#set the SumedTotalInt
		self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#</DefineClass>