# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Simulater

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Recorders.Recorder"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import scipy.stats
#</ImportSpecificModules>

#<DefineLocals>
SimulationEventsTeamKeyStr="Events"
SimulationStatesTeamKeyStr="States"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class SimulaterClass(BaseClass):
	
	def default_init(self,
						_SimulatingStopTimeFloat=100.,
						_SimulatingStepTimeFloat=0.1,
						_SimulatingStartTimeFloat=0.,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_simulate(
			self,
			**_KwargVariablesDict
		):	

		#debug
		'''
		self.debug(('self.',self,[

					]))
		'''

		#/##################/#
		# record
		#

		pass
	


#</DefineClass>

#</DefinePrint>
SimulaterClass.PrintingClassSkipKeyStrsList.extend(
	[

		'SimulatingStopTimeFloat',
		'SimulatingStepTimeFloat',
		'SimulatingStartTimeFloat'
	]
)
#<DefinePrint>
