# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Interfacer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr=""
DecorationModuleStr="ShareYourSystem.Standards.Classors.Doer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class InterfacerClass(object):
	
	def default_init(self,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		object.__init__(self,**_KwargVariablesDict)

		#Add to the IdDict
		SYS.IdDict[id(self)]=self

	def do_interface(self,**_KwargVariablesDict):

		pass
	
#</DefineClass>

