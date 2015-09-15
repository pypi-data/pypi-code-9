# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Vexflower

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Specials.Muzikers.Muziker"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from music21 import vexflow
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class VexflowerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								]

	def default_init(self,
						_VexflowedMusic21Str="",
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_vexflow(self):

		#first muzik
		self.muzik()

		#vexflow now
		self.VexflowedMusic21Vexflow=vexflow.fromObject(
			self.MuzikedMusic21Converter)

#</DefineClass>
