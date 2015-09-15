# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Brianer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Specials.Simulaters.Simulater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Pointer
from ShareYourSystem.Specials.Simulaters import Neurongrouper,Synapser
import operator
#</ImportSpecificModules>

#<DefineLocals>
BrianPopulationTeamKeyStr="Populations"
class PopulationsClass(Pointer.PointerClass):pass
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['brian']
})
class BrianerClass(BaseClass):
		
	def default_init(self,
			_BrianingTimeDimensionVariable=None,
			_BrianingPrintRunIsBool=True,
			_BrianedNetworkVariable=None,
			_BrianedDeriveNeurongroupersList=None,
			_BrianedDeriveSynapsersList=None,
			_BrianedStepTimeFloatsList=None,
			_BrianedClocksList=None,
			_BrianedSimulationClock=None,
			_BrianedNeuronGroupsList=None,
			_BrianedStateMonitorsList=None,
			_BrianedSpikeMonitorsList=None,
			_BrianedSynapsesList=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)


	"""
	def mimic_run(self):

		#parent method
		BaseClass.run(self)

		#debug
		self.debug('We start running in brian')

		#run with the brian method
		self.BrianedNetworkVariable.run(
			self.RunningStopTimeFloat*self.BrianingTimeDimensionVariable
		)

		#debug
		self.debug('We stop running in brian')
	"""

	def mimic_simulate(self):

		#parent method
		BaseClass.simulate(self)

		#debug
		'''
		self.debug('We start simulate in brian')
		'''

		#run with the brian method
		self.BrianedNetworkVariable.run(
			self.SimulatingStopTimeFloat*self.BrianingTimeDimensionVariable
		)

		#debug
		'''
		self.debug('We stop running in brian')
		'''
		
	def do_brian(self):	

		#/###################/#
		# Flat the neurongroups and connections
		#

		#get
		self.BrianedDeriveNeurongroupersList=self.TeamDict[
			BrianPopulationTeamKeyStr
		].ManagementDict.values()

		#flat
		self.BrianedDeriveSynapsersList=SYS.flat(
				map(
					lambda __BrianedDeriveNeurongrouper:
					__BrianedDeriveNeurongrouper.TeamDict[
						Neurongrouper.NeurongroupPostTeamKeyStr
					].ManagementDict.values()
					if Neurongrouper.NeurongroupPostTeamKeyStr in __BrianedDeriveNeurongrouper.TeamDict
					else [],
					self.BrianedDeriveNeurongroupersList
				)
			)

		#debug
		"""
		self.debug(
			[
				'map(self.BrianedDeriveSynapsersList)'
				('self',self,['BrianedDeriveSynapsersList'])
			]
		)
		"""

		"""
		#populate
		map(
				lambda __NetworkedDeriveConnecter:
				__NetworkedDeriveConnecter.populate(),
				self.NetworkedDeriveConnectersList
			)
		
		"""

		"""
		#set the different times
		self.BrianedStepTimeFloatsList=list(
			set(
				SYS.flat(
					map(
						lambda __BrianingDerivePopulater:
						SYS.unzip(
							__BrianingDerivePopulater.MoniteringStateArgumentVariablesList,
							[2]
						) if len(
							__BrianingDerivePopulater.MoniteringStateArgumentVariablesList
						)>0 else [],
						self.NetworkedDeriveConnectersList
					)
				)
			)
		)
		"""

		#debug
		'''
		self.debug(('self.',self,['BrianedStepTimeFloatsList']))
		'''

		#import 
		from brian2 import Clock,Network,ms

		#Check
		if self.BrianingTimeDimensionVariable==None:
			self.BrianingTimeDimensionVariable=ms

		#init
		self.BrianedNetworkVariable=Network()
		
		#set the clocks
		self.BrianedSimulationClock=Clock(
			dt=self.SimulatingStepTimeFloat*self.BrianingTimeDimensionVariable
		)
		self.BrianedClocksDict=dict(
			map(
				lambda __BrianedStepTimeFloat:
				(
					str(__BrianedStepTimeFloat),
					Clock(
							dt=__BrianedStepTimeFloat*self.BrianingTimeDimensionVariable
						)
				),
				self.BrianedStepTimeFloatsList
			)
			,**{
					str(
						self.SimulatingStepTimeFloat
						):self.BrianedSimulationClock
				}
		)

		#debug
		'''
		self.debug(('self.',self,['BrianedClocksDict']))
		'''

		#map populate and neurongroup
		self.BrianedNeuronGroupsList=map(
			lambda __BrianedDeriveNeurongrouper:
			__BrianedDeriveNeurongrouper.neurongroup(
					dict(
						{
							'clock':self.BrianedSimulationClock,
							#Don't forget to replace the '/' by '_' because brian doesn't like them
							'name':__BrianedDeriveNeurongrouper.ParentTagStr.replace(
								'/','_')+'_'+__BrianedDeriveNeurongrouper.ManagementTagStr
						},
						**__BrianedDeriveNeurongrouper.NeurongroupingBrianKwargDict
					)
				).NeurongroupedBrianVariable,
			self.BrianedDeriveNeurongroupersList
			)
		
		#map
		'''
		map(
				lambda __BrianedNeuronGroup:
				__BrianedNeuronGroup.clock.__setattr__(
					'dt',
					self.BrianedSimulationClock.dt
				),
				self.BrianedNeuronGroupsList
			)
		'''

		#flat the spike monitors
		self.BrianedSpikeMonitorsList=SYS.flat(
			map(
				lambda __BrianedDerivePopulater:
				__BrianedDerivePopulater.NeurongroupedSpikeMonitorsList,
				self.BrianedDeriveNeurongroupersList
			)
		)

		#debug
		'''
		self.debug(('self.',self,['BrianedSpikeMonitorsList']))
		'''

		#flat the state monitors
		self.BrianedStateMonitorsList=SYS.flat(
			map(
				lambda __BrianedDeriveNeurongrouper:
				__BrianedDeriveNeurongrouper.NeurongroupedStateMonitorsList,
				self.BrianedDeriveNeurongroupersList
			)
		)	
		
		#debug
		'''
		self.debug(
			[
				('self.',self,['BrianedStateMonitorsList']),
				'Now we synapse...'
			]
		)
		'''

		#map synapse
		self.BrianedSynapsesList=map(
				lambda __BrianedDeriveSynapser:
				__BrianedDeriveSynapser.synapse(
					dict(
						__BrianedDeriveSynapser.SynapsingKwargVariablesDict
						if __BrianedDeriveSynapser.SynapsingKwargVariablesDict!=None 
						else {},
						**{
							'source':__BrianedDeriveSynapser.CatchFromPointVariable.NeurongroupedBrianVariable,
							'target':__BrianedDeriveSynapser.CatchToPointVariable.NeurongroupedBrianVariable,
							#'name':(
							#	__BrianedDeriveSynapser.CatchFromPointVariable.NetworkKeyStr+'To'+__BrianedDeriveSynapser.CatchToPointVariable.NetworkKeyStr).replace('/','_')
							'name':(
								__BrianedDeriveSynapser.SynapsingTagStr 
								if __BrianedDeriveSynapser.SynapsingTagStr!="" 
								else __BrianedDeriveSynapser.CatchKeyStr.replace('>','_').replace('<','_')
							)
						}
					)
				).SynapsedBrianVariable,
				self.BrianedDeriveSynapsersList
			)

		#debug
		'''
		self.debug(('self.',self,['BrianedSynapsesList']))
		'''

		#map the add
		map(
				lambda __BrianedVariable:
				self.BrianedNetworkVariable.add(__BrianedVariable),
				self.BrianedNeuronGroupsList+self.BrianedSynapsesList+self.BrianedStateMonitorsList+self.BrianedSpikeMonitorsList
			)

		"""
		#Check
		if self.BrianingPrintRunIsBool:

			#debug
			self.debug(('self.',self,[
								'BrianedSimulationClock'
								]))


			#define
			@brian.network_operation(
				self.BrianedSimulationClock
			)
			def printControl():

				#Print Time
				print(
					"time is "+str(
						self.BrianedSimulationClock.t*self.BrianingTimeDimensionVariable
					)
				)

				'''
				#Print NeuronGroup
				print(
					"variables are"+str(
					self.BrianedNeuronGroupsList[0]
					)
				)
				'''
				
			self.BrianedNetworkVariable.add(printControl);
		"""
#</DefineClass>

#<DefineLocals>

#set
BrianerClass.TeamingClassesDict[BrianPopulationTeamKeyStr]=PopulationsClass

#set
PopulationsClass.ManagingValueClass=Neurongrouper.NeurongrouperClass

#</DefineLocals>


#</DefinePrint>
BrianerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'BrianingTimeDimensionVariable',
		'BrianingPrintRunIsBool',
		'BrianedNetworkVariable',
		'BrianedDeriveNeurongroupersList',
		'BrianedDeriveSynapsersList',
		'BrianedStepTimeFloatsList',
		'BrianedClocksList',
		'BrianedSimulationClock',
		'BrianedNeuronGroupsList',
		'BrianedStateMonitorsList',
		'BrianedSpikeMonitorsList',
		'BrianedSynapsesList'
	]
)
#<DefinePrint>
