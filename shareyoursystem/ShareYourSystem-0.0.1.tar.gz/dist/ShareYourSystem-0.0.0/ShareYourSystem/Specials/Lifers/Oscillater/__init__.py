# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


"""

#<DefineAugmentation>
import ShareYourSystem as SYS
import types
BaseModuleStr="ShareYourSystem.Specials.Lifers.Transferer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Oscillater','Oscillate','Oscillating','Oscillated')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Recorders import Leaker
import scipy.stats
import numpy as np
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingStructureVariable':[
		('Mode','Modes'),
		('Resonance','Resonances')
	]
})
class OscillaterClass(BaseClass):
	
	def default_init(self,
			_OscillatingMeanWeightVariable = None,
			_OscillatedRateBool = False,
			**_KwargVariablesDict
		):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def oscillateUpToDownTop(self):

		#map
		map(
			lambda __Variable:
			__Variable.setAttr('OscillatedRateBool',False),
			self.TeamDict['Modes'].ManagementDict.values()
		)

	def oscillateUpToDownMode(self):

		#debug
		self.debug(
			[
				"We oscillate up to down mode here"
			]
		)

		#set
		self.OscillatedTopVariable = self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#alias
		self.StationarizingMeanWeightVariable = self.OscillatedTopVariable.OscillatingMeanWeightVariable

		#debug
		self.debug(
			[
				"Check if we need to compute rate stationary",
				('self.',self,[
						"OscillatedRateBool"
					]),
				('self.OscillatedTopVariable.',self.OscillatedTopVariable,[
						'OscillatingMeanWeightVariable'
					])
			]
		)
		
		#Check
		if self.OscillatedRateBool == False:

			#stationarize
			self.stationarize(
				).stabilize(
					_ComputeBool=False
				)

			#set
			self.OscillatedRateBool = True

		#transfer
		self.transfer()

	def oscillateUpToDownResonance(self):
		
		#/####################/#
		# Determine the parent
		#

		#set
		self.OscillatedModeOscillater = self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#set
		self.OscillatedTopVariable = self.OscillatedModeOscillater.OscillatedTopVariable

		#debug
		self.debug(
			[
				"We oscillate up to down resonance here",
				('self.OscillatedModeOscillater.',
					self.OscillatedModeOscillater,
					[
						#'TransferedRateComplexesArray',
						'TransferedPeakVariable',
						'StationarizedMeanWeightFloatsArray'
					]
				)
			]
		)

		



#</DefineClass>

#</DefineLocals>
Leaker.LeakersStructurerClass.ManagingValueClass=OscillaterClass
#<DefineLocals>

#</DefinePrint>
OscillaterClass.PrintingClassSkipKeyStrsList.extend(
	[
		"OscillatingMeanWeightVariable",
		"OscillatedRateBool"
	]
)
#<DefinePrint>