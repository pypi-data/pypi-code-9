# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Differenciater...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Muzikers.Permuter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Functers import Argumenter,Hooker,Switcher
#</ImportSpecificModules>

#<DefineFunctions>
def getFilteredPitchBoolsListsListWithNotesInt(_PitchBoolsListsList,_NotesInt):
	return SYS._filter(
					lambda __PitchBoolsList:
					len(set(__PitchBoolsList))==_NotesInt,
					_PitchBoolsListsList
				)
#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class DifferenciaterClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
									'DifferenciatedIntsList'
								]

	#@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':BaseClass.__init__}]})
	def default_init(self,
						_DifferenciatedIntsList=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	@Argumenter.ArgumenterClass()
	def differenciate(self,**_KwargVariablesDict):

		#debug
		'''
		self.debug(('self.',self,[]))
		'''

		#permute first
		self.permute()

		#debug
		'''
		self.debug(('self.',self,['PermutedIntsList']))
		'''
		
		#filter
		self.DifferenciatedIntsList=getFilteredPitchBoolsListsListWithNotesInt(
			self.PermutedIntsList,self.PermutingSubsetContentInt
		)

		#Return self
		return self

#</DefineClass>
