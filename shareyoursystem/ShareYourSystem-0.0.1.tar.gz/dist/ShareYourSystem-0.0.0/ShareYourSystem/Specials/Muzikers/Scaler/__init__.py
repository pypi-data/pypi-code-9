# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Scaler

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Specials.Muzikers.Pooler"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import music21
import collections
from ShareYourSystem.Specials.Muzikers import Streamer
#</ImportSpecificModules>

#<DefineLocals>
ScalingSharpNoteStrsList=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
ScalingFlatNoteStrsList=["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ScalerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								'ScalingSharpIsBool',
								'ScalingHeightStr',
								'ScaledNoteStrsListsList',
								'ScaledOrderedDict'
							]

	def default_init(self,
						_ScalingSharpIsBool=True,
						_ScalingHeightStr='4',
						_ScaledNoteStrsListsList=None,
						_ScaledOrderedDict=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_scale(self):

		#pool
		self.pool(8,12)

		#map
		self.ScaledNoteStrsListsList=map(
				lambda __PooledIntsList:
				map(
						ScalingSharpNoteStrsList.__getitem__
						if self.ScalingSharpIsBool
						else ScalingFlatNoteStrsList.__getitem__,
						__PooledIntsList
					),
				self.PooledIntsListsList
			)

		#map
		self.ScaledOrderedDict=collections.OrderedDict(
			map(
				lambda __PooledIntsList,__ScaledNoteStrsList:
				(
					#str(__PooledIntsList),
					str(__ScaledNoteStrsList),
					{
						'IndexIntsList':__PooledIntsList,
						'NoteStrsList':__ScaledNoteStrsList
					}
				),
				self.PooledIntsListsList,
				self.ScaledNoteStrsListsList
			)
		)

		#map
		map(
			lambda __ItemTuple:
			self.ScaledOrderedDict[
				__ItemTuple[0]
			].update(
				{
					'IsThirdMajorBool':4 in __ItemTuple[1]['IndexIntsList'],
					'IsThirdMinorBool':3 in __ItemTuple[1]['IndexIntsList'],
					'IsFairMinorBool':3 in __ItemTuple[1]['IndexIntsList'],
					'IsSevenMajorBool':11 in __ItemTuple[1]['IndexIntsList'],
					'IsSevenMinorBool':10 in __ItemTuple[1]['IndexIntsList'],
					'Streamer':Streamer.StreamerClass(
						).stream(
							__ItemTuple[1]['NoteStrsList']
						)
				}
			),
			self.ScaledOrderedDict.items()
		)
#</DefineClass>
