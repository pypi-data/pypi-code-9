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
BaseModuleStr="ShareYourSystem.Standards.Recorders.Simulater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Recorders import Recorder
#</ImportSpecificModules>

#<DefineLocals>
BrianConnectPrefixStr='Synaps'
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['brian'],
	'ClassingStructureVariable':[
			('Clock','Clocks'),
			('Population','Populations'),
			('Trace','Traces'),
			('Sample','Samples'),
			('Event','Events'),
			('Interactome','Interactomes'),
			('Interaction','Interactions')
		]
})
class BrianerClass(BaseClass):
		
	def default_init(self,
			_BrianingNeurongroupDict=None,
			_BrianingSynapsesDict=None,
			_BrianingConnectVariable=None,
			_BrianingTraceDict=None,
			_BrianingMoniterTuple=None,
			_BrianingSpikesDict=None,
			_BrianingPyplotDict=None,
			_BrianingTimeQuantityStr='ms',
			_BrianingPyplotBool=True,
			_BrianingStepTimeFloat=0.1,
			_BrianingDebugVariable=0,
			_BrianingRecordBool=True,
			_BrianedTimeQuantityVariable=None,
			_BrianedNetworkVariable=None,
			_BrianedNeurongroupVariable=None,
			_BrianedSynapsesVariable=None,
			_BrianedStateMonitorVariable=None,
			_BrianedSpikeMonitorVariable=None,
			_BrianedClockVariable=None,
			_BrianedParentSingularStr=None,
			_BrianedRecordKeyStrsList=None,
			_BrianedTraceDeriveBrianersList=None,
			_BrianedSynapsesDeriveBrianersList=None,
			_BrianedStateDeriveBrianersList=None,
			_BrianedSpikeDeriveBrianersList=None,
			_BrianedParentNetworkDeriveBrianerVariable=None,
			_BrianedParentPopulationDeriveBrianerVariable=None,
			_BrianedParentInteractomeDeriveBrianerVariable=None,
			_BrianedParentDeriveRecorderVariable=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_brian(self):

		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We brian here',
				'First look for deeper teams in the structure',
			]
		)
		'''

		#Check
		if self.ParentedTotalSingularListDict!=None and len(self.ParentedTotalSingularListDict)>0:

			#debug
			'''
			self.debug(
				[
					'self.ParentedTotalSingularListDict.keys() is ',
					str(self.ParentedTotalSingularListDict.keys())
				]
			)
			'''

			#get
			self.BrianedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,[
					'BrianedParentSingularStr'
				])
			]
		)
		'''

		#/########################/#
		# Network level
		# 

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Clocks',
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			'Interactions'
		]) and self.BrianedParentSingularStr!='Population':

			#debug
			'''
			self.debug(
				[
					'It is a Network level',
					'We set the brian network'
				]
			)
			'''

			#set
			self.brianNetwork()

			#/########################/#
			# Special Network-Neurongroup level
			# 

			#Check
			if 'Populations' not in self.TeamDict:
		
				#debug
				'''
				self.debug(
					[
						'It is a network with a one level pop',
						'So set the neurongroup'
					]
				)
				'''

				#brianPopulation
				self.brianPopulation()

				#debug
				'''
				self.debug(
					[
						'We end to set the neuron group here'
					]
				)
				'''

			#/########################/#
			# structure
			# 

			#debug
			'''
			self.debug(
				[
					'We brian structure in all the brian children...',
				]
			)
			'''

			#structure
			self.structure(
				[
					'Clocks',
					'Populations',
					'Traces',
					'Events',
					'Samples',
					'Interactomes',
					'Interactions'
				],
				'#all',
				_ManagerCommandSetList=['brian']
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have brian structured all the brian children...',
				]
			)	
			'''

		else:

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'BrianedParentSingularStr'
					])
				]
			)
			'''

			#set
			BrianedMethodKeyStr='brian'+self.BrianedParentSingularStr

			#Check
			if hasattr(self,BrianedMethodKeyStr):

				#/########################/#
				# call the special brian<BrianedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.BrianedParentSingularStr+' level',
						'We brian<BrianedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					BrianedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted brian'+self.BrianedParentSingularStr
					]
				)
				'''		

		#debug
		'''
		self.debug(
			[
				'end of brian here'
			]
		)
		'''

	def brianNetwork(self):

		#/####################/#
		# init the Network
		#

		#maybe should import
		import brian2

		#set
		self.BrianedNetworkVariable=brian2.Network()

		#get
		self.BrianedTimeQuantityVariable=getattr(
			brian2,
			self.BrianingTimeQuantityStr
		)

		#/####################/#
		# init a simulation clock
		#

		#debug
		'''
		self.debug(
			[
				'We set a simulation clock at least'
			]
		)
		'''

		#Check
		if 'Clocks' not in self.TeamDict:
			ClocksDeriveManager=self.team('Clocks').TeamedValueVariable
		else:
			ClocksDeriveManager=self.TeamDict['Clocks']

		#manage
		if 'Simulation' not in ClocksDeriveManager.ManagementDict:

			#debug
			'''
			self.debug(
				[
					'We init a simulation clock here'
				]
			)
			'''

			#manage
			SimulationDeriveBrianer=ClocksDeriveManager.manage(
				'Simulation',
				{
					'BrianingStepTimeFloat':self.BrianingStepTimeFloat
				}
			)

	def brianClock(self):

		#/####################/#
		# Determine the parents
		#

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#/####################/#
		# Set the brian clock
		#

		#import
		from brian2 import Clock

		#debug
		'''
		self.debug(
			[
				'We set the brian clock',
				('self.',self,['StructureTagStr'])
			]
		)
		'''

		#init
		self.BrianedClockVariable=Clock(
			dt=self.BrianingStepTimeFloat*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable,
			#name=self.StructureTagStr
		)

		#debug
		'''
		self.debug(
			[
				'We have setted the clock',
				('self.',self,[
						'BrianedClockVariable'
							])
			]
		)
		'''

	def brianPopulation(self):

		#debug
		'''
		self.debug(
			[
				'It is a Neurongroup level, we set the Neurongroup',
				'We adapt the shape of BrianingNeurongroupDict',
				('self.',self,[
							'BrianingNeurongroupDict',
							'RecordingKeyVariable'
						])
			]
		)
		'''

		#/########################/#
		# Determine parents
		#

		#Check
		if self.ParentDeriveTeamerVariable!=None:

			#set the parent
			self.BrianedParentNetworkDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#set the parent
			self.BrianedParentNetworkDeriveBrianerVariable=self

		#/################/#
		# Adapt the arg
		#

		#Check
		if 'N' not in self.BrianingNeurongroupDict:
			self.BrianingNeurongroupDict['N']=0

		#Check
		if 'model' not in self.BrianingNeurongroupDict:
			self.BrianingNeurongroupDict['model']=''

		#maybe should import
		from brian2 import NeuronGroup

		#debug
		'''
		self.debug(
			[
				('self.',self,[
							'BrianingNeurongroupDict'
							]),
				'We now set the model system Neurongroup if N>0 and model!=""'
			]
		)
		'''

		#/################/#
		# Set the brian neurongroup
		#

		#Check
		if self.BrianingNeurongroupDict['N']>0 and self.BrianingNeurongroupDict['model']!="":

			#init
			self.BrianedNeurongroupVariable=NeuronGroup(
				**dict(
					self.BrianingNeurongroupDict,
					**{
						#'name':self.ParentedTotalPathStr.replace('/','_')+'_'+self.ManagementTagStr,
						#'clock':self.BrianedParentNetworkDeriveBrianerVariable.TeamDict[
						#	'Clocks'
						#].ManagementDict['Simulation'].BrianedClockVariable
					} 
				)
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the Neurongroup',
					('self.',self,[
								'BrianedNeurongroupVariable'
								])
				]
			)
			'''

			#/##################/#
			# Define a debug
			#

			#Check
			if self.BrianingDebugVariable>0:

				#import
				from brian2 import network_operation,ms

				@network_operation(
					dt=self.BrianingDebugVariable*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable
				)
				def debugNeurongroup():

					#init
					PrintStr='At time t='+str(self.BrianedNeurongroupVariable.clock.t)+', \n'
					PrintStr+='In the NeuronGroup '+self.BrianedNeurongroupVariable.name+' : \n'

					#loop
					for __KeyStr in self.BrianedNeurongroupVariable.equations._equations.keys():

						#set
						PrintStr+=__KeyStr+" is "+str(
							getattr(
								self.BrianedNeurongroupVariable,
								__KeyStr
							)
						)+'\n'


					#add
					PrintStr+='\n'

					#print
					print PrintStr
				
				#add
				self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
					debugNeurongroup
				)


			#Check
			if self.BrianingNeurongroupDict['N']>0:

				#/##################/#
				# team States first all the brian variables
				#

				#get
				self.BrianedRecordKeyStrsList=self.BrianedNeurongroupVariable.equations._equations.keys()

				#Check
				if len(self.BrianedRecordKeyStrsList)>0:

					#debug
					'''
					self.debug(
							[
								'We simulate with neurongroup',
								'adapt the initial conditions of all the brian variables',
								'so first we team Traces and put Recorders inside or get it and mapSet'
							]
						)
					'''

					#Check
					if 'Traces' not in self.TeamDict:
						BrianedDeriveTraces=self.team(
							'Traces'
						).TeamedValueVariable
					else:
						BrianedDeriveTraces=self.TeamDict[
								'Traces'
							]

					#debug
					'''
					self.debug(
						[
							'We set the tracers',
							('self.',self,['BrianedRecordKeyStrsList'])
						]
					)
					'''

					#map
					self.BrianedTraceDeriveBrianersList=map(
							lambda __ManagementKeyStr,__RecordKeyStr:
							BrianedDeriveTraces.manage(
									__ManagementKeyStr,
									{
										'RecordingKeyVariable':getattr(
											self.BrianedNeurongroupVariable,
											__RecordKeyStr
										),
										'RecordKeyStr':__RecordKeyStr
									}
								).ManagedValueVariable
							if __ManagementKeyStr not in BrianedDeriveTraces.ManagementDict
							else BrianedDeriveTraces.ManagementDict[__ManagementKeyStr].mapSet(
								{
									'RecordingKeyVariable':getattr(
										self.BrianedNeurongroupVariable,
										__RecordKeyStr
									),
									'RecordKeyStr':__RecordKeyStr
								}
							),
							map(
								lambda __BrianedRecordKeyStr:
								Recorder.RecordPrefixStr+__BrianedRecordKeyStr,
								self.BrianedRecordKeyStrsList
							),
							self.BrianedRecordKeyStrsList
						)


			#/##################/#
			# add in the net
			#

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedNeurongroupVariable
			)

			"""
			#/####################/#
			# maybe view a draw plot
			#

			#call
			self.viewPopulation()
			"""

		#debug
		'''
		self.debug(
			[
				'End of brianPopulation'
			]
		)
		'''

	def brianInteraction(self):

		#/########################/#
		# Postlet level
		#  

		#debug
		'''
		self.debug(
			[
				'It is an Interaction level',
				('self.',self,[
							#'BrianingSynapsesDict'
							]
				)
			]
		)
		'''

		#/####################/#
		# Set the parent
		#

		#Check
		if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.BrianedParentSingularStr=='Interactome':

			#debug
			'''
			self.debug(
				[
					'We are in a projectome structure'
				]
			)
			'''

			#set
			self.BrianedParentInteractomeDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.BrianedParentInteractomeDeriveBrianerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#debug
			'''
			self.debug(
				[
					'There is no projectome structure'
				]
			)
			'''

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable


		#/####################/#
		# Set the ConnectedTo Variable
		#

		#debug
		'''
		self.debug(
			[
				'Check if we have to get the connected to variable',
				('self.',self,['ConnectedToVariable'])
			]
		)
		'''

		#Check
		if self.ConnectedToVariable==None:

			#debug
			'''
			self.debug(
				[
					'We setConnection here'
				]
			)
			'''

			#setConnection
			self.setConnection(
				self.ManagementTagStr,
				self,
				self.BrianedParentPopulationDeriveBrianerVariable
			)

		#/####################/#
		# Set the BrianedParentPopulationDeriveBrianerVariable
		#

		#debug
		'''
		self.debug(
			[
				'Do we have to make parent-brian the connected variable ?',
				'self.ConnectedToVariable.BrianedNeurongroupVariable is ',
				str(self.ConnectedToVariable.BrianedNeurongroupVariable)
			]
		)
		'''

		#Check 
		if self.ConnectedToVariable.BrianedNeurongroupVariable==None:

			#parent brian
			self.ConnectedToVariable.parent(
				).brian(
				)

		#set
		BrianedNameStr=self.BrianedParentPopulationDeriveBrianerVariable.StructureTagStr+'_To_'+self.ConnectedToVariable.StructureTagStr

		#debug
		'''
		self.debug(
			[
				'We set the synapses',
				'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable is ',
				str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable),
				'self.ConnectedToVariable.BrianedNeurongroupVariable is ',
				str(self.ConnectedToVariable.BrianedNeurongroupVariable),
				'Maybe we have to make brian the post',
				'BrianedNameStr is '+BrianedNameStr
			]
		)
		'''

		#import
		from brian2 import Synapses

		#init
		self.BrianedSynapsesVariable=Synapses(
			source=self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
			target=self.ConnectedToVariable.BrianedNeurongroupVariable,
			#name=BrianedNameStr.replace('/','_'),
			**self.BrianingSynapsesDict
		)

		#/####################/#
		# Connect options
		#

		#connect
		if type(self.BrianingConnectVariable)==float:

			#debug
			'''
			self.debug(
				[
					'we connect with a sparsity of ',
					('self.',self,[
						'BrianingConnectVariable'
					])
				]
			)
			'''

			#connect
			self.BrianedSynapsesVariable.connect(
				True,
				p=self.BrianingConnectVariable
			)

		#/####################/#
		# add to the structure
		#

		#add
		self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
			self.BrianedSynapsesVariable
		)

		#/##################/#
		# Define a debug
		#

		#Check
		if self.BrianingDebugVariable>0:

			#import
			from brian2 import network_operation,ms

			@network_operation(
				dt=self.BrianingDebugVariable*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable
			)
			def debugSynapses():

				#init
				PrintStr='At time t='+str(self.BrianedSynapsesVariable.clock.t)+', \n'
				PrintStr+='In the Synapses '+self.BrianedSynapsesVariable.name+' : \n'

				#loop
				for __KeyStr in self.BrianedSynapsesVariable.equations._equations.keys():

					#set
					PrintStr+=__KeyStr+" is "+str(
						getattr(
							self.BrianedSynapsesVariable,
							__KeyStr
						)
					)+'\n'


				#add
				PrintStr+='\n'

				#print
				print PrintStr
			
			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				debugSynapses
			)

	def brianTrace(self):

		#debug
		'''
		self.debug(
			[
				'It is a Trace level, we set the Samples',
				('self.',self,[
							#'RecordingKeyVariable',
							'RecordKeyStr'
							])
			]
		)
		'''

		#/####################/#
		# Set the parent
		#

		#get
		self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.BrianingNeurongroupDict['N']>0:
		
			#/####################/#
			# we record
			#

			#Check
			if self.BrianingRecordBool:

				#debug
				'''
				self.debug(
					[
						'We record here'
					]
				)
				'''

				#record
				self.record()

			#/###################/#
			# Build the samples and maybe one default moniter
			#

			#debug
			'''
			self.debug(
				[
					'Look if we have samples here',
					"'Samples' not in self.TeamDict is ",
					str('Samples' not in self.TeamDict)
				]
			)
			'''

			#Check
			if 'Samples' not in self.TeamDict:
				BrianedSamplesDeriveManager=self.team(
					'Samples'
				).TeamedValueVariable
			else:
				BrianedSamplesDeriveManager=self.TeamDict[
						'Samples'
					]

			#debug
			'''
			self.debug(
				[
					'Do we have to set a default moniter ?',
					#'len(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList) is ',
					#str(len(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList)),
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList) is ',
					str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList),
					
				]
			)
			'''

			#Check
			if len(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList)==1:

				#debug
				'''
				self.debug(
					[
						'BrianedSamplesDeriveManager.ManagementDict.keys() is',
						str(BrianedSamplesDeriveManager.ManagementDict.keys())
					]
				)
				'''

				#Check
				if len(BrianedSamplesDeriveManager.ManagementDict)==0 or (
					len(BrianedSamplesDeriveManager.ManagementDict)==1 and 'Default' in BrianedSamplesDeriveManager.ManagementDict
				):

					#debug
					'''
					self.debug(
						[
							'There is just one variable that we sample',
							'we manage and make it brian'
						]
					)
					'''

					#manage
					BrianedDefaultBrianer=BrianedSamplesDeriveManager.manage(
						'Default',
					).ManagedValueVariable

					#Check
					if BrianedDefaultBrianer.RecordingLabelVariable==None:

						#Check
						if self.BrianedParentPopulationDeriveBrianerVariable.RecordingLabelVariable!=None:

							#get
							BrianedDefaultBrianer.RecordingLabelVariable=self.BrianedParentPopulationDeriveBrianerVariable.RecordingLabelVariable
						
						else:

							#set the record labels
							BrianedDefaultBrianer.RecordingLabelVariable=[0] if self.BrianedParentPopulationDeriveBrianerVariable.BrianingNeurongroupDict[
							'N']>0 else []

						#brian
						BrianedDefaultBrianer.parent(
							).brian(
							)

	def brianSample(self):

		#debug
		'''
		self.debug(
			[
				'It is a Sample State Moniter level',
				('self.',self,[
							'RecordingLabelVariable',
							])
			]
		)
		'''

		#/####################/#
		# Set the parent
		#

		#get
		self.BrianedParentDeriveRecorderVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentPopulationDeriveBrianerVariable=self.BrianedParentDeriveRecorderVariable.BrianedParentPopulationDeriveBrianerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable!=None:

		
			#/####################/#
			# Set the brian monitor
			#
		
			#debug
			'''
			self.debug(
				[
					'We set the state monitor',
					('self.',self,[
						#'BrianedParentPopulationDeriveBrianerVariable'
						]),
					#'self.BrianedParentDeriveRecorderVariable.RecordKeyStr is ',
					#str(self.BrianedParentDeriveRecorderVariable.RecordKeyStr)
					'self.ParentedTotalManagementOrderedDict.keys() is ',
					str(self.ParentedTotalManagementOrderedDict.keys())
				]
			)
			'''

			#import
			from brian2 import StateMonitor

			#init
			self.BrianedStateMonitorVariable=StateMonitor(
					self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
					self.BrianedParentDeriveRecorderVariable.RecordKeyStr,
					self.RecordingLabelVariable,
				)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the monitor',
					('self.',self,['BrianedStateMonitorVariable']),
					'Now we add to the structure',
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable is ',
					str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable)
				]
			)
			'''

			#/####################/#
			# add to the structure
			#

			#debug
			'''
			self.debug(
				[
					'We add to the structure'
				]
			)
			'''

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedStateMonitorVariable
			)

			"""
			#/####################/#
			# maybe view a draw plot
			#

			#call
			self.viewSample()
			"""

	def brianEvent(self):

		#debug
		'''
		self.debug(
			[
				'It is a Spike Moniter level',
				('self.',self,[
							])
			]
		)
		'''

		#/####################/#
		# Set the BrianedParentPopulationDeriveBrianerVariable
		#

		#get
		self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable!=None:

			#/####################/#
			# Set the brian monitor
			#
		
			#debug
			'''
			self.debug(
				[
					'We set the spike monitor'
				]
			)
			'''

			#import
			from brian2 import SpikeMonitor

			#init
			self.BrianedSpikeMonitorVariable=SpikeMonitor(
					self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
				)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the monitor',
					('self.',self,['BrianedSpikeMonitorVariable']),
					'Now we add to the structure',
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNetworkVariable is ',
					str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNetworkVariable)
				]
			)
			'''

			#/####################/#
			# add to the structure
			#

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedSpikeMonitorVariable
			)

			"""
			#/####################/#
			# maybe view a draw plot
			#

			#call
			self.viewEvent()
			"""

	def mimic_view(self):

		#/########################/#
		# Network level
		# 

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Clocks',
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			'Interactions'
		]) and self.BrianedParentSingularStr!='Population':

			#debug
			'''
			self.debug(
				[
					'It is a Network level',
					'We sructure view'
				]
			)
			'''

			#/########################/#
			# structure
			# 

			#debug
			'''
			self.debug(
				[
					'We view structure in all the brian children...',
				]
			)
			'''

			#structure
			self.structure(
				[
					'Clocks',
					'Populations',
					'Traces',
					'Events',
					'Samples',
					'Interactomes',
					'Interactions'
				],
				'#all',
				_ManagerCommandSetList=['view']
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have view structured all the brian children...',
				]
			)	
			'''

		else:

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'BrianedParentSingularStr'
					])
				]
			)
			'''

			#set
			BrianedMethodKeyStr='view'+self.BrianedParentSingularStr

			#Check
			if hasattr(self,BrianedMethodKeyStr):

				#/########################/#
				# call the special view<BrianedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.BrianedParentSingularStr+' level',
						'We view<BrianedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					BrianedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted view'+self.BrianedParentSingularStr
					]
				)
				'''	

	def viewPopulation(self):

		#debug
		'''
		self.debug(
			[
				'We complete a view so first fill the draw'
			]
		)
		'''

		#Check
		if 'Charts' not in self.TeamDict:
			BrianedChartsDeriveTeamer=self.team(
				'Charts'
			).TeamedValueVariable
		else:
			BrianedChartsDeriveTeamer=self.TeamDict['Charts']

	def viewSample(self):

		#debug
		self.debug(
			[
				'We complete a view so first fill the draw',
				('self.',self,[
					'RecordingLabelVariable',
					'ViewedLegendLabelStr'
				])
			]
		)

		#/##################/#
		# Determine the way of labeling the variable names
		#

		#set
		if self.ViewedLegendLabelStr=="":

			#set
			self.ViewedLegendLabelStr='$'+self.BrianedParentDeriveRecorderVariable.RecordKeyStr
			'''
			self.ViewedLegendLabelStr+='_{'+str(	
					#self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.name
					#self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.
					
				).replace('_','/')+'}'
			'''

			#debug
			self.debug(
				[
					'We have specified the legend label',
					('self.',self,[
						'ViewedLegendLabelStr'
					])
				]
			)

		#set
		self.PyplotingDrawVariable=map(
			lambda __IndexInt:
			(
				'plot',
				{
					'#liarg:#map@get':[
						'#IdGetStr.BrianedStateMonitorVariable.t',
						'>>SYS.IdDict[#IdStr].BrianedStateMonitorVariable.'+self.BrianedParentDeriveRecorderVariable.RecordKeyStr+'['+str(
							__IndexInt)+',:]'
					],
					'#kwarg':dict(
						{
							'label':self.ViewedLegendLabelStr+'^{'+str(__IndexInt)+'}$',
							'linestyle':'-',
							'color':'b'
						},
						**self.BrianingPyplotDict
					)
				}
			),
			self.RecordingLabelVariable
		)


		#/####################/#
		# maybe set for the Chart
		#

		#init
		self.PyplotingChartVariable=[]

		#/####################/#
		# maybe set the X Chart also
		#

		#get
		BrianedTimeUnit=self.BrianedStateMonitorVariable.t.unit

		#scale
		#self.ViewingXVariable=self.BrianedStateMonitorVariable.t[:]
		self.ViewingXVariable=self.BrianedStateMonitorVariable.t/(
			#(1./self.ViewingXScaleFloat)*BrianedTimeUnit
			BrianedTimeUnit
		)

		#set
		self.ViewingXLabelStr='$t\ ('+str(
			(1./self.ViewingXScaleFloat)*BrianedTimeUnit
		).split('.')[-1]+')$'
	
		#/####################/#
		# maybe set the Y Chart also
		#

		#debug
		self.debug(
			[
				'We set the y axis',
				'self.BrianedParentDeriveRecorderVariable.RecordedTraceFloatsArray is ',
				str(self.BrianedParentDeriveRecorderVariable.RecordedTraceFloatsArray)
			]
		)

		#import
		import brian2

		#get
		ViewingYVariable=getattr(
						self.BrianedStateMonitorVariable,
						self.BrianedParentDeriveRecorderVariable.RecordKeyStr
				)

		#split
		#BrianedDimensionStr=str(ViewingYVariable).split(' ')[-1]
		BrianedActivityUnit=getattr(
				self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr
			).unit

		#divide
		#self.ViewingYVariable=ViewingYVariable/getattr(
		#	brian2,BrianedDimensionStr
		#)
		self.ViewingYVariable=ViewingYVariable/(
			BrianedActivityUnit
		)
		#self.ViewingYVariable=ViewingYVariable
		self.ViewingYVariable=self.ViewingYVariable[:]
		print(self.ViewingYVariable)

		#set
		self.ViewingYLabelStr='$'+self.BrianedParentDeriveRecorderVariable.RecordKeyStr
		"""
		self.ViewingYLabelStr+='_{'+str(
			self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.name
				).replace('_','/')+'}(t)\ ('+str(
					self.BrianedParentDeriveRecorderVariable.RecordedTraceFloatsArray.unit
				)+')'

		"""
		
		#self.ViewingYLabelStr+='\ ('+BrianedDimensionStr+')'
		self.ViewingYLabelStr+='\ ('+str(
			(1./self.ViewingYScaleFloat)*BrianedActivityUnit
		).split('.')[-1]+')'
		self.ViewingYLabelStr+='$'


		#/################/#
		# call the base view method
		#

		#debug
		self.debug(
			[
				('self.',self,[
						'ViewingXVariable',
						'ViewingYVariable'
					]),
				'Now we call the view'
			]
		)

		#call 
		BaseClass.view(self)

		#/####################/#
		# maybe set global Chart also
		#

		self.PyplotingChartVariable+=[
			(
				'tick_params',{
					'#kwarg':{
						'length':10,
						'width':5,
						'which':'major'
					}
				}
			),
			(
				'tick_params',{
					'#kwarg':{
						'length':5,
						'width':2,
						'which':'minor'
					}
				}
			),
			('xaxis.set_ticks_position',
				{
					'#liarg':['bottom']
				}
			),
			('yaxis.set_ticks_position',
				{
					'#liarg':['left']
				}
			),
			('legend',{
				'#liarg':[],
				'#kwarg':{
					'fontsize':10,
					'shadow':True,
					'fancybox':True,
					'ncol':max(1,len(
						getattr(
							self.BrianedStateMonitorVariable,
							self.BrianedParentDeriveRecorderVariable.RecordKeyStr
						)
					)/2),
					'loc':2,
					'bbox_to_anchor':(1.05, 1)
				}
			})
		]

		#/####################/#
		# maybe replace Chart also
		#

		#debug
		'''
		self.debug(
			[
				'Before replace',
				('self.',self,[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''

		#mapReplace
		[
			self.PyplotingDrawVariable,
			self.PyplotingChartVariable
		]=map(
			lambda __Variable:
			SYS.replace(
				__Variable,
				{
					'#IdStr':str(self.PrintIdInt),
					'#IdGetStr':"#id:"+str(self.PrintIdInt)
				},
				self
			)
			if __Variable!=None
			else None,
			map(
				lambda __KeyStr:
				getattr(
					self,
					__KeyStr
				),
				[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				]
			)
		)

		#debug
		'''
		self.debug(
			[
				'After replace',
				('self.',self,[
					#'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''

		#/####################/#
		# Update maybe the 
		# parent neuron group

		#debug
		self.debug(
			[
				'Maybe we also update the view in the parent population'
			]
		)

		#Check
		if 'Charts' in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict:

			#get
			BrianedChartsDeriveManager=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
				'Charts'
			]

			#manage
			BrianedChartDerivePyploter=BrianedChartsDeriveManager.manage(
				self.BrianedParentDeriveRecorderVariable.ManagementTagStr
			).ManagedValueVariable


			#debug
			'''
			self.debug(
				[
					'We update in the parent neurongroup chart',
					'BrianedChartDerivePyploter is ',
					SYS._str(BrianedChartDerivePyploter),
					('self.',self,[])
				]
			)
			'''

			#team
			BrianedDrawDeriveManager=BrianedChartDerivePyploter.team(
				'Draws'
			).TeamedValueVariable

			#manage
			BrianedDrawDeriveManager.manage(
				str(self.ManagementIndexInt),
				{
					'PyplotingDrawVariable':self.PyplotingDrawVariable
				}
			)

	def viewEvent(self):

		#debug
		'''
		self.debug(
			[
				'We complete a view so first fill the draw'
			]
		)
		'''

		#set
		self.ViewedLabelStr='$'+self.ManagementTagStr+'_{'+str(
			self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.name
							).replace('_','/')+'}'

		#set
		self.PyplotingDrawVariable=[
			(
				'plot',
				{
					'#liarg:#map@get':[
						'#IdGetStr.BrianedSpikeMonitorVariable.t',
						'>>SYS.IdDict[#IdStr].BrianedSpikeMonitorVariable.i'
					],
					'#kwarg':dict(
						{
							'label':self.ViewedLabelStr,
							'linestyle':'',
							'marker':'.',
							'color':'b'
						},
						**self.BrianingPyplotDict
					)
				}
			)
		]

		#/####################/#
		# maybe replace Chart also
		#

		#debug
		'''
		self.debug(
			[
				'Before replace',
				('self.',self,[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''

		#mapReplace
		[
			self.PyplotingDrawVariable,
			self.PyplotingChartVariable
		]=map(
			lambda __Variable:
			SYS.replace(
				__Variable,
				{
					'#IdStr':str(self.PrintIdInt),
					'#IdGetStr':"#id:"+str(self.PrintIdInt)
				},
				self
			)
			if __Variable!=None
			else None,
			map(
				lambda __KeyStr:
				getattr(
					self,
					__KeyStr
				),
				[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				]
			)
		)

		#debug
		'''
		self.debug(
			[
				'After replace',
				('self.',self,[
					#'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''

		#/####################/#
		# Update maybe the 
		# parent neuron group

		#get
		BrianedChartDeriveManager=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
			'Charts'
		]

		#manage
		BrianedChartDerivePyploter=BrianedChartDeriveManager.manage(
			self.ManagementTagStr
		).ManagedValueVariable

		#debug
		'''
		self.debug(
			[
				'We update in the parent neurongroup chart',
				'BrianedChartDerivePyploter is ',
				SYS._str(BrianedChartDerivePyploter),
				('self.',self,[])
			]
		)
		'''

		#team
		BrianedDrawDeriveManager=BrianedChartDerivePyploter.team(
			'Draws'
		).TeamedValueVariable

		#manage
		BrianedDrawDeriveManager.manage(
			str(self.ManagementIndexInt),
			{
				'PyplotingDrawVariable':self.PyplotingDrawVariable
			}
		)

	def mimic_simulate(self):

		#parent method
		BaseClass.simulate(self)

		#debug
		'''
		self.debug('We start simulate in brian')
		'''

		#run with the brian method
		self.BrianedNetworkVariable.run(
			self.SimulatingStopTimeFloat*self.BrianedTimeQuantityVariable
		)

		#debug
		'''
		self.debug('We stop running in brian')
		'''

	def mimic_record(self):

		#base method
		BaseClass.record(self)

		#debug
		'''
		self.debug(
			[
				'We have traced, alias the init in the brian object',
				('self.',self,[
					'RecordedTraceFloatsArray',
					'RecordedInitFloatsArray'
				])
			]
		)
		'''

		#alias
		self.RecordedTraceFloatsArray[:]=self.RecordedInitFloatsArray*self.RecordedTraceFloatsArray.unit

		#debug
		'''
		self.debug(
			[
				('self.',self,['RecordedTraceFloatsArray'])
			]
		)
		'''

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Remove the brian objects that are non setted
			#

			#map
			map(
					lambda __KeyStr:
					self.forcePrint(
						[__KeyStr],
						'BrianerClass'
					)
					if getattr(self.PrintingCopyVariable,__KeyStr)!=None
					else None,
					[
						'BrianedNetworkVariable',
						'BrianedNeurongroupVariable',
						'BrianedSynapsesVariable',
						'BrianedStateMonitorVariable',
						'BrianedSpikeMonitorVariable',
						'BrianedClockVariable'
					]
				)


		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

#</DefineClass>

#</DefinePrint>
BrianerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'BrianingNeurongroupDict',
		'BrianingSynapsesDict',
		'BrianingConnectVariable',
		'BrianingTraceDict',
		'BrianingMoniterTuple',
		'BrianingSpikesDict',
		'BrianingPyplotDict',
		'BrianingTimeQuantityStr',
		'BrianingPyplotBool',
		'BrianingStepTimeFloat',
		'BrianingDebugVariable',
		'BrianingRecordBool',
		'BrianedTimeQuantityVariable',
		'BrianedNetworkVariable',
		'BrianedNeurongroupVariable',
		'BrianedSynapsesVariable',
		'BrianedStateMonitorVariable',
		'BrianedSpikeMonitorVariable',
		'BrianedClockVariable',
		'BrianedRecordKeyStrsList',
		'BrianedTraceDeriveBrianersList',
		'BrianedSynapsesDeriveBrianersList',
		'BrianedStateDeriveBrianersList',
		'BrianedSpikeDeriveBrianersList',
		'BrianedParentSingularStr',
		'BrianedParentNetworkDeriveBrianerVariable',
		'BrianedParentPopulationDeriveBrianerVariable',
		'BrianedParentInteractomeDeriveBrianerVariable',
		'BrianedParentDeriveRecorderVariable'
	]
)
#<DefinePrint>
