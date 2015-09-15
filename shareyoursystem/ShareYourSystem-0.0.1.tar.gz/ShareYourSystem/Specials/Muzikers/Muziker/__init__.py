# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Muziker

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Systemer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import music21 
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class MuzikerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								"MuzikingScoreStr"
							]

	def default_init(self,
						_MuzikingScoreStr="",
						_MuzikedMusic21Converter=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_muzik(self):

		#debug
		'''
		self.debug(('self.',self,['MuzikingScoreStr']))
		'''

		"""
		#Convert
		if self.FileKeyStr!='' and self.FileKeyStr.endswith('.xml'):

			self.MuzikedMusic21ConverterVariable=music21.converter.parse(
				self.FilePathStr)

		else:

			self.MuzikedMusic21ConverterVariable=music21.converter.parse(
				self.MuzikingScoreStr)
		"""




#</DefineClass>
