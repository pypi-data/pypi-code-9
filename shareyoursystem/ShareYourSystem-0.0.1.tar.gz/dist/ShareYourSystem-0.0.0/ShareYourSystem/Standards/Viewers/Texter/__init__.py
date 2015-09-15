# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>

A Viewer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Viewers.Viewer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class TexterClass(BaseClass):
	
	#Definition 
	RepresentingKeyStrsList=[
								'TextingConditionVariable',
								'TextingQueryVariable',
								'TextedCollectionStrsList',
								'TextedConsoleStr'
							]

	def default_init(self, 
					_TextingConditionVariable=None,
					_TextingQueryVariable=None,
					_TextedCollectionStrsList=None,
					_TextedConsoleStr="",
					**_KwargVariablesDict
			):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_text(self):

		#Init
		self.TextedConsoleStr=""

		#Check
		if hasattr(self,'hdfview'):
			
			#Add
			self.TextedConsoleStr+="Associated Hdf file :\n"
			self.TextedConsoleStr+=self.ViewedPointDeriveControllerVariable.hdfview(
							).HdformatedConsoleStr

		#Check
		if self.ViewedPointDeriveControllerVariable.PymongoneDatabaseVariable!=None:
			
			#Check
			if self.TextingConditionVariable==None:
				self.TextingConditionVariable={}

			#map
			self.TextedCollectionStrsList=map(
					lambda __CollectionTuple:
					__CollectionTuple[0]+' : \n'+SYS._str(
						list(
							__CollectionTuple[1].find(
									self.TextingConditionVariable[__CollectionTuple[0]]
									if __CollectionTuple[0] in self.TextingConditionVariable
									else {},
									self.TextingQueryVariable[__CollectionTuple[0]]
									if __CollectionTuple[0] in self.TextingQueryVariable
									else {}
								)
						)
					),
					self.ViewedPointDeriveControllerVariable.PymongoneDatabaseVariable.__dict__.items()
				)

			self.TextedConsoleStr+="Associated Mongo db :\n"
			self.TextedConsoleStr='\n'.join(self.TextedCollectionStrsList)

#</DefineClass>
