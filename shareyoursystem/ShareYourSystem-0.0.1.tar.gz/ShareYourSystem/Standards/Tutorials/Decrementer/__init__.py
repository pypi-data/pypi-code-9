# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Decrementer...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Printer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<DefineAttest>
AttestingFunctionStrsList=['attest_decrement']
#</DefineAttest>

#<DefineClass>
@DecorationClass()
class DecrementerClass(BaseClass):

	def default_init(self,
					_DecrementingStartInt=0,
					_DecrementingStartIsBool=False,
					_DecrementedNextInt=0
					):

		#init with the base method
		BaseClass.__init__(self)
	
	def do_decrement(self):

		#Check
		if self.DecrementingStartIsBool:
			self.DecrementedNextInt=self.DecrementingStartInt

		#add
		self.DecrementedNextInt-=1

	def attest_decrement(self):

		#return
		return self.decrement().DecrementedNextInt
#</DefineClass>

