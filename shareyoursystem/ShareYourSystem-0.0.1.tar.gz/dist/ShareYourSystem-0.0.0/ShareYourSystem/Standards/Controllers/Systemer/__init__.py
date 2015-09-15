# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Systemer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Shower"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class SystemerClass(BaseClass):

	def default_init(self,
						_SystemingServerMethodStr="",
						_SystemingServerCollectionStr="",
						_SystemingHelperMethodStr="",
						_SystemingCollectionDict=None,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_system(self):

		#call
		self.MeteoredConcurrentDDPClientVariable.call(
				self.SystemingServerMethodStr,
				self.SystemingServerCollectionStr,
				self.SystemingHelperMethodStr,
				self.SystemingCollectionDict
			)
		
		
#</DefineClass>

#</DefinePrint>
SystemerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'SystemingServerMethodStr',
		'SystemingServerCollectionStr',
		'SystemingHelperMethodStr',
		'SystemingCollectionDict'
	]
)
#<DefinePrint>

