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
from ShareYourSystem.Functers import Triggerer,Outputer
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class MultiplierClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
									'MultiplyingFirstInt',
									'MultiplyingSecondInt',
									'MultipliedTotalInt'
								]
								
	def __init__(self,
						_MultiplyingFirstInt=0,
						_MultiplyingSecondInt=0,
						_MultipliedTotalInt=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
			

	#@Triggerer.TriggererClass(**{
	#								'TriggeringConditionVariable':[
	#									('SettingKeyVariable',(SYS.getIsInListBool,[
	#										'MultiplyingFirstInt',
	#										'MultiplyingSecondInt'
	#									]))
	#								]
	#							}
	#						)
	@Outputer.OutputerClass()
	def do_multiply(self):
		
		#debug
		'''
		self.debug(('self.',self,['MultiplyingFirstInt','MultiplyingSecondInt']))
		'''

		#set the MultipliedTotalInt
		self.MultipliedTotalInt=self.MultiplyingFirstInt*self.MultiplyingSecondInt
#</DefineClass>