# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Leaker

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Recorders.Brianer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Leaker','Leak','Leaking','Leaked')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Interfacers import Printer
from ShareYourSystem.Standards.Recorders import Recorder
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['leak'],
	'ClassingStructureVariable':[
			('Population','Populations'),
			('Trace','Traces'),
			('Sample','Samples'),
			('Event','Events'),
			('Interactome','Interactomes'),
			('Interaction','Interactions'),
			('Input','Inputs')
		]
})
class LeakerClass(BaseClass):
		
	def default_init(self,
			_LeakingUnitsInt=0,
			_LeakingActivitySymbolStr="V",
			_LeakingCurrentStr="",
			_LeakingTimeConstantFloat=0.,
			_LeakingTimeDirectBool=True,
			_LeakingActivityDimensionStr='volt',
			_LeakingMonitorIndexIntsList=None,
			_LeakingTimeUnitStr='ms',
			_LeakingInteractionClampStr='Rate',
			_LeakingInteractionPrefixSymbolStr='J',
			_LeakingInputPrefixSymbolStr='I',
			_LeakingExternalVariable=None,
			_LeakedTimeSymbolStr="tau_V",
			_LeakedModelStr="",
			_LeakedInteractionSymbolStr="",
			_LeakedInputSymbolStr="",
			_LeakedParentSingularStr="",
			_LeakedParentNetworkDeriveLeakerVariable=None,
			_LeakedParentPopulationDeriveLeakerVariable=None,
			_LeakedParentInteractomeDeriveLeakerVariable=None,
			_LeakedTimedArrayVariable=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)


	def filterLeak(self):

		#/#################/#
		# Look for the StructureTopDeriveStructurerVariable
		#

		#debug
		self.debug(
			[
				'Check if we can leak',
				'self.StructureTopDeriveStructurerVariable!=None',
				str(self.StructureTopDeriveStructurerVariable!=None)
			]
		)

		#Check
		if self.StructureTopDeriveStructurerVariable!=None:

			#Check
			if self.StructureTopDeriveStructurerVariable.StructureFilterTeamTagStrsList!=None:

				#Check
				if self.ParentDeriveTeamerVariable!=None:

					#debug
					self.debug(
						[
							'Check if we can leak',
							'self.ParentDeriveTeamerVariable.TeamTagStr is ',
							str(self.ParentDeriveTeamerVariable.TeamTagStr)
						]
					)

					#Check
					if self.ParentDeriveTeamerVariable.TeamTagStr in self.StructureTopDeriveStructurerVariable.StructureFilterTeamTagStrsList:

						#return
						return

		#leak
		self.leak()

	def do_leak(self):

		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We leak here',
				'First look for deeper teams in the structure',
			]
		)
		'''

		#Check
		if self.ParentedTotalSingularListDict!=None and len(
			self.ParentedTotalSingularListDict
		)>0:

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
			self.LeakedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['LeakedParentSingularStr'])
			]
		)
		'''

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			'Interactions',
			'Inputs'
		]) and self.LeakedParentSingularStr!='Population':

			#/########################/#
			# Network level
			# 

			#debug
			self.debug(
				[
					'It is a Network level for the leak',
				]
			)
			
			#/########################/#
			# network the interactions
			# 

			#debug
			self.debug(
				[
					'We structure filterLeak all the interacting children...'
					'So we pass thrugh the populations and leak the interactomes, interactions and inputs',
				]
			)	

			#set
			self.StructureFilterTeamTagStrsList=[
				'Populations'
			]

			#structure
			self.structure(
				[
					'Populations',
					'Interactomes',
					'Interactions',
					'Inputs'
				],
				'#all',
				_ManagerCommandSetList=[
					'filterLeak'
				]
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have structured the interacting children',
				]
			)
			'''

			#/########################/#
			# setNetwork
			#

			#set
			self.setNetwork()

			#/########################/#
			# Special Network-Neurongroup level
			# 

			#Check
			if 'Populations' not in self.TeamDict:
		
				#debug
				self.debug(
					[
						'...But there is no population',
						'so set a leak model here '
					]
				)

				#set
				self.BrianedParentNetworkDeriveBrianerVariable=self

				#setPopulation
				self.setPopulation()

				#debug
				'''
				self.debug(
					[
						'Ok we have leak setted the population',
						'Now we also neurongroup'
					]
				)
				'''

				#setNeurongroup
				self.setNeurongroup()

				#debug
				'''
				self.debug(
					[
						'Ok we have brian setted the population'
					]
				)
				'''

			#/########################/#
			# network the populations
			# 

			#debug
			self.debug(
				[
					'We structure leak brian all the children...',
					'self.TeamDict.keys() is ',
					str(self.TeamDict.keys())
				]
			)

			#set
			self.StructureFilterTeamTagStrsList=None

			#add
			self.StructuringManagerCommandSetList=['leak','brian']

			#structure
			self.structure(
				[
					'Populations',
					'Traces',
					'Samples',
					'Events',
					'Interactomes',
					'Interactions',
				],
				'#all'
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have structured leak brian all the children',
				]
			)
			'''

		#Check
		if self.LeakedParentSingularStr=='Population':

			#/################/#
			# Look how to define the time constant
			#

			#debug
			self.debug(
				[
					'It is the Population level',
					'Check if we direct define the time constant or not'
				]
			)

			#setPopulation
			self.setPopulation()

		elif self.LeakedParentSingularStr=='Interaction':

			#/################/#
			# Interaction level
			#

			#debug
			self.debug(
				[
					'It is the Interaction level',
				]
			)

			#setPopulation
			self.setInteraction()

		elif self.LeakedParentSingularStr=='Input':

			#/################/#
			# Input level
			#

			#debug
			self.debug(
				[
					'It is an Input level',
				]
			)

			#/################/#
			# Determine the parent
			#

			#set
			self.LeakedParentPopulationDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#Check
			if self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable!=None:

				#get
				self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			else:

				#get
				self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable


			#/################/#
			# Add in the model
			#

			#set
			self.LeakedInputSymbolStr=self.LeakingInputPrefixSymbolStr+self.ParentTagStr.split(
				'Inputs'
			)[-1].replace('/','_')

			#debug
			self.debug(
				[
					'we add in the model of the parent population',
					('self.',self,['LeakedInputSymbolStr'])
				]
			)

			#debug
			self.debug(
				[
					'We add the interaction in the population model',
					'self.LeakedParentPopulationDeriveLeakerVariable.LeakingCurrentStr is ',
					self.LeakedParentPopulationDeriveLeakerVariable.LeakingCurrentStr
				]
			)

			#define in the model
			self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedInputSymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivityDimensionStr+'\n'

			#add in the current
			self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(self.LeakedInputSymbolStr)


	def setPopulation(self):

		#/################/#
		# Look for the time constant
		#

		#debug
		self.debug(
			[
				'We set a population here',
				'look for the time constant'
			]
		)

		#Check
		if self.LeakingTimeDirectBool:

			#set
			self.LeakedTimeSymbolStr=str(self.LeakingTimeConstantFloat)

		else:

			#set
			self.LeakedTimeSymbolStr="tau_"+self.LeakingActivitySymbolStr

			#define the time constant variable
			self.LeakedModelStr+=self.LeakedTimeSymbolStr+' : 1\n'

		#/################/#
		# Define the main leak equation
		#

		#debug
		self.debug(
			[
				'We define the main leak equation but maybe it is just a direct value',
				('self.',self,['LeakingTimeConstantFloat'])
			]
		)

		#Check
		if self.LeakingTimeConstantFloat==0:

			#debug
			self.debug(
				[
					'Build just a variable definition',
					('self.',self,['LeakingTimeConstantFloat'])
				]
			)

			#set the left 
			self.LeakedModelStr+=self.LeakingActivitySymbolStr+' : '+self.LeakingActivityDimensionStr

		else:

			#debug
			self.debug(
				[
					'Build a differential equation'
				]
			)

			#set the left 
			self.LeakedModelStr+="d"+self.LeakingActivitySymbolStr+'/dt='

			#set the right
			self.LeakedModelStr+='(-'+self.LeakingActivitySymbolStr

			#Check
			if self.LeakingCurrentStr!="":
				self.LeakedModelStr+='+'+self.LeakingCurrentStr

			#set
			self.LeakedModelStr+=')'

			#set the right denominator
			self.LeakedModelStr+='/('+self.LeakedTimeSymbolStr+'*'+self.LeakingTimeUnitStr+')'

			#set the dimension
			self.LeakedModelStr+=' : '+self.LeakingActivityDimensionStr

		#debug
		self.debug(
			[
				'We have defined the leak model str',
				('self.',self,['LeakedModelStr'])
			]
		)

		#/################/#
		# Now update the brianer stuff
		#

		
		#team traces
		LeakedTracesDeriveManager=self.team(
			'Traces'
			).TeamedValueVariable

		#manage
		LeakedRecordDeriveLeaker=LeakedTracesDeriveManager.manage(
				'*'+self.LeakingActivitySymbolStr
			).ManagedValueVariable

		#set
		LeakedRecordDeriveLeaker.NumscipyingStdFloat=0.001
		LeakedSamplesDeriveLeaker=LeakedRecordDeriveLeaker.team(
				'Samples'
			).TeamedValueVariable
		LeakedDefaultDeriveLeaker=LeakedSamplesDeriveLeaker.manage(
				'Default'
			).ManagedValueVariable

		#Check
		if len(self.LeakingMonitorIndexIntsList)==0:
			self.LeakingMonitorIndexIntsList=[0]

		#set
		LeakedDefaultDeriveLeaker.MoniteringLabelIndexIntsArray=self.LeakingMonitorIndexIntsList

		#/##################/#
		# Update in the Neurongroup dict
		#

		#Check
		if self.BrianingNeurongroupDict==None:
		
			#init
			self.BrianingNeurongroupDict={
					'N':self.LeakingUnitsInt,
					'model':self.LeakedModelStr
				}

		else:

			#update
			self.BrianingNeurongroupDict.update(
				{
					'N':self.LeakingUnitsInt,
					'model':self.LeakedModelStr
				}
			)

		"""
		#/##################/#
		# Call the brian setNeurongroup
		#
	
		#call
		#self.setNeurongroup()
		"""

	def setInteraction(self):

		#/####################/#
		# Set the parent
		#

		#Check
		if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.LeakedParentSingularStr=='Projectome':

			#debug
			'''
			self.debug(
				[
					'We are in a projectome structure'
				]
			)
			'''

			#set
			self.LeakedParentProjectomeDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.LeakedParentPopulationDeriveLeakerVariable=self.LeakedParentProjectomeDeriveLeakerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

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
			self.LeakedParentPopulationDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#Check
		if self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable!=None:

			#get
			self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#get
			self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable



		#debug
		self.debug(
			[
				'We set Interaction here',
				'Look for the type of interaction'
			]
		)

		#Check
		if self.LeakingInteractionClampStr=='Rate':

			#set
			self.LeakedInteractionSymbolStr=self.LeakingInteractionPrefixSymbolStr+self.ParentTagStr.split(
				'Interactions'
			)[-1].replace('/','_')

			#debug
			self.debug(
				[
					'It is a rate interaction',
					'self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivitySymbolStr is ',
					self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivitySymbolStr,
					'First we set the model in the synapse',
					('self.',self,['LeakedInteractionSymbolStr'])
				]
			)

			#set
			self.LeakedModelStr+="\n"+self.LeakedInteractionSymbolStr+" : 1 \n"
			self.LeakedModelStr+=self.LeakedInteractionSymbolStr+self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivitySymbolStr+"_post="
			self.LeakedModelStr+=self.LeakedInteractionSymbolStr+self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivitySymbolStr+"_pre : 1 (summed)\n"

			#debug
			self.debug(
				[
					'We add the interaction in the population model',
					'self.LeakedParentPopulationDeriveLeakerVariable.LeakingCurrentStr is ',
					self.LeakedParentPopulationDeriveLeakerVariable.LeakingCurrentStr
				]
			)

			#set
			LeakedInteractionActivitySymbolStr=self.LeakedInteractionSymbolStr+self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivitySymbolStr

			#define in the model
			self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=LeakedInteractionActivitySymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakingActivityDimensionStr+'\n'

			#add in the current
			self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(LeakedInteractionActivitySymbolStr)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Print the leaked Model str if it is defined
			#

			#Check
			if self.LeakedModelStr!='':

				#Check
				if 'PrintDeepInt' in _KwargVariablesDict:
					PrintedDeepInt=_KwargVariablesDict['PrintDeepInt']
				else:
					PrintedDeepInt=0

				#join
				PrintedAlineaStr="".join([Printer.PrintIndentStr]*(PrintedDeepInt+3))

				#debug
				'''
				print('Leaker l 409')
				print('PrintedDeepInt is ')
				print(PrintedDeepInt)
				print('PrintedAlineaStr is ')
				print(PrintedAlineaStr)
				print('')
				'''

				#replace
				self.PrintingCopyVariable.LeakedModelStr=self.LeakedModelStr.replace(
					'\n','\n'+PrintedAlineaStr
				)

				#add
				self.forcePrint(
					['LeakedModelStr'],
					'LeakerClass'
				)

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)


	def setNeurongroup(self):

		#/##################/#
		# Call the base method
		#

		#debug
		self.debug(
			[
				'We call first the base method'
			]
		)

		#call
		BaseClass.setNeurongroup(self)

		#/###################/#
		# Special input current case
		#

		#Check
		if 'Inputs' in self.TeamDict:

			#debug
			self.debug(
				[
					'We are going to set all the input variables',
				]
			)

			#map
			map(
				lambda __DeriveLeaker:
				__DeriveLeaker.setInput(),
				self.TeamDict['Inputs'].ManagementDict.values()
			)

	def setInput(self):

		#debug
		self.debug(
			[
				'Yeah we set a TimedArray here',
				#('self.',self,[
				#	'LeakingExternalVariable'
				#	]),
				#'self.BrianedParentNetworkDeriveBrianerVariable.BrianingTimeDimensionVariable is ',
				#str(self.BrianedParentNetworkDeriveBrianerVariable.BrianingTimeDimensionVariable),
				#'self.BrianedNeurongroupVariable.clock.dt is ',
				#str(self.BrianedNeurongroupVariable.clock.dt),
				'len(self.LeakingExternalVariable) is ',
				str(len(self.LeakingExternalVariable))
			]
		)	

		#import
		from brian2 import TimedArray

		"""
		#Check
		if len(self.LeakingExternalVariable)==1 and self.LeakingUnitsInt>1:

			#import
			import numpy as np

			#reproduce
			LeakedTimedArray=np.array(
					[self.LeakingExternalVariable]*self.LeakingUnitsInt
				)

			#debug
			self.debug(
				[
					'LeakedTimedArray is ',
					SYS._str(LeakedTimedArray)
				]
			)

			#init
			self.LeakedTimedArrayVariable=TimedArray(
				LeakedTimedArray,
				dt=self.BrianedNeurongroupVariable.clock.dt
			)
		"""
		#else:

		#init
		self.LeakedTimedArrayVariable=TimedArray(
			self.LeakingExternalVariable,
			dt=self.BrianedNeurongroupVariable.clock.dt
		)

		#debug
		'''
		self.debug(
			[
				'Yeah we have timed arrayed ',
				('self.',self,[
					'LeakedTimedArrayVariable'
					])
			]
		)	
		'''
			



	"""
	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#/##################/#
		# Maybe brian
		#

		#debug
		'''
		self.debug(
			[
				'We are going to parent but before',
				('self.',self,['StructuringDoStr']),
				'self.StructureTopDeriveStructurerVariable!=self is ',
				str(self.StructureTopDeriveStructurerVariable!=self),
				'self.ParentedTotalListDict.keys() is ',
				str(self.ParentedTotalListDict.keys()),
				'self.ParentedTotalSingularListDict.keys() is ',
				str(self.ParentedTotalSingularListDict.keys())
			]
		)
		''' 

		#Check
		if self.StructuringDoStr=='Leak' and self.StructureTopDeriveStructurerVariable!=self:

			#leak
			self.leak()

		#Check
		if self.StructuringDoStr=='Leak-Brian' and self.StructureTopDeriveStructurerVariable!=self:

			#debug
			self.debug(
				[
					'We leak first'
				]
			)

			#leak
			self.leak()

			#debug
			self.debug(
				[
					'We brian then'
				]
			)

			#brian
			self.brian()

		#/##################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
			[
				'Now we call the base setParent method'
			]
		)
		'''

		#set
		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)
	"""

	"""
	def mimic_structure(self):

		#/##################/#
		# Maybe brian
		#

		#debug
		self.debug(
			[
				'We are going to link structure maybe with leak and brian',
				('self.',self,['StructuringDoStr']),
				#'self.StructureTopDeriveStructurerVariable!=self is ',
				#str(self.StructureTopDeriveStructurerVariable!=self),
				#'self.ParentedTotalListDict.keys() is ',
				#str(self.ParentedTotalListDict.keys()),
				#'self.ParentedTotalSingularListDict.keys() is ',
				#str(self.ParentedTotalSingularListDict.keys())
			]
		)

		#Check
		if self.StructuringDoStr=='Leak' and self.StructureTopDeriveStructurerVariable!=self:


			#debug
			self.debug(
				[
					'We just leak'
				]
			)

			#leak
			self.leak()

		#Check
		elif self.StructuringDoStr=='Leak-Brian' and self.StructureTopDeriveStructurerVariable!=self:

			#debug
			self.debug(
				[
					'We leak first'
				]
			)

			#leak
			self.leak()

			#debug
			self.debug(
				[
					'We brian then'
				]
			)

			#brian
			self.brian()

		else:

			#/##################/#
			# Call the base method
			#

			#debug
			'''
			self.debug(
				[
					'It is the top',
					'Now we call the base method'
				]
			)
			'''

			#set
			BaseClass.structure(self)
	"""

	def addCurrentStr(self,_CurrentStr):

		#Check
		if self.LeakingCurrentStr=="":
			self.LeakingCurrentStr=_CurrentStr
		else:
			self.LeakingCurrentStr+='+ '+_CurrentStr



#</DefineClass>

#</DefinePrint>
LeakerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'LeakingUnitsInt',
		'LeakingActivitySymbolStr',
		'LeakingCurrentStr',
		'LeakingTimeConstantFloat',
		'LeakingTimeDirectBool',
		'LeakingActivityDimensionStr',
		'LeakingMonitorIndexIntsList',
		'LeakingTimeUnitStr',
		'LeakingInteractionClampStr',
		'LeakingInteractionPrefixSymbolStr',
		'LeakingInputPrefixSymbolStr',
		'LeakingExternalVariable',
		'LeakedTimeSymbolStr',
		'LeakedModelStr',
		'LeakedInteractionSymbolStr',
		'LeakedInputSymbolStr',
		'LeakedParentSingularStr',
		'LeakedParentNetworkDeriveLeakerVariable',
		'LeakedParentPopulationDeriveLeakerVariable',
		'LeakedParentInteractomeDeriveLeakerVariable',
		'LeakedTimedArrayVariable'
	]
)
#<DefinePrint>
