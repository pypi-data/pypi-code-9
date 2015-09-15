# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


An harmonizer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Objects.Harmonizer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import itertools
from ShareYourSystem.Functers import Argumenter,Hooker,Switcher
#</ImportSpecificModules>

#<DefineFunctions>
def getFlattenedListWithVariablesList(_VariablesList):
	return functools.reduce(
					lambda x,y:
						x+list(y) if type(y)==tuple 
						else list(x)+[y] if type(x) in [list,tuple] 
						else [x,y],_VariablesList
				)

def getPermutedIntsListWithCategoriesIntAndLengthInt(_CategoriesInt,_LengthInt):
	return functools.reduce(
					lambda x,y:
						map(
								lambda __IntOrTuple:
										getFlattenedListWithVariablesList(list(__IntOrTuple)) 
										if type(__IntOrTuple)==tuple
										else __IntOrTuple,
										itertools.product(x,y)
							),
						map(lambda Int:range_(_LengthInt),range_(_CategoriesInt))
				)

def getFilteredPitchBoolsListsListWithNotesInt(_PitchBoolsListsList,_NotesInt):
	return filter_(
					lambda __PitchBoolsList:
					len(
						filter_(
								lambda Int:
								Int==1,
								__PitchBoolsList
							)
						)==_NotesInt,
					_PitchBoolsListsList
				)

def getFilteredPitchBoolsListsListWithPitchesIntAndNotesInt(_PitchesInt,_NotesInt):
	if type(_PitchesInt)==int and _PitchesInt>0:
		PitchBoolsListsList=getPermutedIntsListWithCategoriesIntAndLengthInt(
			_PitchesInt,
			2
		)
		if type(_NotesInt)==int and _NotesInt>0:
			return getFilteredPitchBoolsListsListWithNotesInt(PitchBoolsListsList,_NotesInt)
		return PitchBoolsListsList
	return []
#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class HarmonizerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
									'HarmonizingNotesInt',
									'HarmonizingPitchesInt',
									'HarmonizedPitchBoolsListsList'
								]

	#@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':BaseClass.__init__}]})
	def default_init(self,
						_HarmonizingNotesInt=0,
						_HarmonizingPitchesInt=0,
						_HarmonizedPitchBoolsListsList=[],
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	@Argumenter.ArgumenterClass()
	def harmonize(self,**_KwargVariablesDict):

		pass

		#Return self
		return self

#</DefineClass>
