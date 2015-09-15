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
BaseModuleStr="ShareYourSystem.Specials.Predicters.Predisenser"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Prediploter','Prediplot','Prediploting','Prediploted')
#</DefineAugmentation>

#<ImportSpecificModules>
from matplotlib import pyplot
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PrediploterClass(BaseClass):
	
	def default_init(self,

						_PrediplotedPyplotFigureVariable=None,
						_PrediplotedSensorAxisVariable=None,

						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_prediplot(self):

		#/################/#
		# Prepare figure
		#

		#init
		self.PrediplotedPyplotFigureVariable=pyplot.figure()

		#/#################/#
		# Command and sensors
		#

		#subplot
		self.PrediplotedSensorAxisVariable=pyplot.subplot(3,1,1)

		#command
		map(
				lambda __IndexInt:
				self.PrediplotedSensorAxisVariable.plot(
						self.PredisensedTimeFloatsArray,
						self.PredictingConstantTimeFloat*self.PredisensedCommandTraceFloatsArray[__IndexInt],
						label='$\\tau_{D}c(t)$',
					)
				if __IndexInt<len(self.PredisensedCommandTraceFloatsArray)
				else None,
				[0]
			)

		#debug
		'''
		self.debug(
				('self.',self,['PredisensedSensorTraceFloatsArray'])
			)
		'''

		#sensor
		map(
				lambda __IndexInt:
				self.PrediplotedSensorAxisVariable.plot(
						self.PredisensedTimeFloatsArray,
						self.PredisensedSensorTraceFloatsArray[__IndexInt,:],
						color='g',
						label='$x(t)$',
						linewidth=3
					)
				if __IndexInt<len(self.PredisensedSensorTraceFloatsArray)
				else None,
				[0,1]
			)

		#set
		self.PrediplotedSensorAxisVariable.legend()
		self.PrediplotedSensorAxisVariable.set_ylabel('$\\tau_{D}c(t),\ x(t)$')
		self.PrediplotedSensorAxisVariable.set_xlim([0.,self.PredispikingRunTimeFloat])
		self.PrediplotedSensorAxisVariable.set_ylim(
			[
				-0.1,
				1.5*self.PredispikingClampFloat*self.PredictingConstantTimeFloat
			]
		)
	

#</DefineClass>

#</DefinePrint>
PrediploterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PrediplotedPyplotFigureVariable',
		'PrediplotedSensorAxisVariable'
	]
)
#<DefinePrint>