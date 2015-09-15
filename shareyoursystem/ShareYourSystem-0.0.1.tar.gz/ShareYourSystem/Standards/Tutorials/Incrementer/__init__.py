# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Incrementer is a super complicated object toy for incrementing an Int 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Printer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Attester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<DefineClass>
@DecorationClass()
class IncrementerClass(BaseClass):

	def default_init(
				self,
				_IncrementingStartInt=0,
				_IncrementingStartIsBool=False,
				_IncrementedNextInt=0
		):

		#init with the base method
		BaseClass.__init__(self)
	
	def do_increment(self):

		#Check
		if self.IncrementingStartIsBool:
			self.IncrementedNextInt=self.IncrementingStartInt

		#add
		self.IncrementedNextInt+=1

	def attest_increment(self):

		#return
		return self.increment().IncrementedNextInt

#</DefineClass>


