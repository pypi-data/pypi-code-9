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
#BaseModuleStr="ShareYourSystem.Standards.Recorders.Leaker"
BaseModuleStr="ShareYourSystem.Specials.Lifers.Lifer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Stationarizer','Stationarize','Stationarizing','Stationarized')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Recorders import Leaker
import scipy.stats
import numpy as np
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class StationarizerClass(BaseClass):
	
	def default_init(self,
			_StationarizingUnitsInt = 1,
			_StationarizingConstantTimeVariable = None, 
			_StationarizingThresholdVariable = None, 
			_StationarizingResetVariable = None,
			_StationarizingExternalCurrentMeanVariable = None,
			_StationarizingExternalCurrentNoiseVariable = None, 
			_StationarizingMeanWeightVariable = None,
			_StationarizingNoiseWeightVariable = None,
			_StationarizingRateVariable = None, 
			_StationarizingPopulationTagVariable = None, 
			_StationarizingInteractionStr="Rate",
			_StationarizedConstantTimeFloatsList = None,
			_StationarizedThresholdFloatsList = None, 
			_StationarizedResetFloatsList = None, 
			_StationarizedExternalCurrentMeanFloatsList = None,
			_StationarizedExternalCurrentNoiseFloatsList = None, 
			_StationarizedRateFloatsList = None, 
			_StationarizedMeanWeightFloatsList = None,
			_StationarizedNoiseWeightFloatsList = None,
			_StationarizedMeanWeightFloatsArray = None,
			_StationarizedNoiseWeightFloatsArray = None,
			_StationarizedSquareWeightFloatsArray = None,
			_StationarizedRateFloatsArraysList = None,
			_StationarizedTotalCurrentMeanFloatsListsList = None,
			_StationarizedTotalCurrentNoiseFloatsListsList = None,
			_StationarizedPopulationTagStrsList = None,
			_StationarizedParentSingularStr = "",
			_StationarizedNetworkDeriveStationarizerVariable = None,
			**_KwargVariablesDict
		):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	
	def do_stationarize(self):

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
			self.StationarizedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['StationarizedParentSingularStr'])
			]
		)
		'''

		#Check
		if (self.ParentDeriveTeamerVariable==None or "Populations" in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			"Interactions",
			'Inputs'
		]) and self.StationarizedParentSingularStr!='Population':

			#/########################/#
			# Network level
			# 

			#debug
			'''
			self.debug(
				[
					'It is a Network level for the stationarize',
				]
			)
			'''

			#/########################/#
			# Determine parent level
			# 

			#alias
			self.StationarizedNetworkDeriveStationarizerVariable=self

			#/########################/#
			# stationarizeNetwork
			# 

			#stationarize
			self.stationarizeNetwork()

			#/########################/#
			# structure stationarize 
			# 

			#debug
			'''
			self.debug(
				[
					'We structure all the stationarizeing children...'
				]
			)	
			'''

			#structure
			self.structure(
				[
					"Populations",
					'Inputs',
					'Interactomes',
					"Interactions",
				],
				'#all',
				_ManagerCommandSetList=[
						'stationarize'
					]
			)

			#/###################/#
			# Maybe it is a current to rate computation
			# 

			#Check
			if type(self.StationarizingExternalCurrentMeanVariable)!=None.__class__:

				#debug
				'''
				self.debug(
					[
						'We compute the non linear system to solve stationary rates',
						('self.',self,[
								'StationarizingExternalCurrentMeanVariable'
							])
					]
				)
				'''

				#/###################/#
				# We dont want to compute perturbation here
				# 

				#map
				map(
					lambda __PopulationVariable:
					__PopulationVariable.setAttr(
						'LifingComputePerturbationBool',
						False
					),
					self.TeamDict['Populations'].ManagementDict.values(),
				)

				#import
				import scipy.optimize

				#init
				self.StationarizedRateFloatsArraysList=[]
				self.StationarizedTotalCurrentMeanFloatsListsList=[]
				self.StationarizedTotalCurrentNoiseFloatsListsList=[]

				#import
				import itertools

				#set
				StabilizedInitRateFloatsList=[1.,100.]

				#for
				for __InitRateFloatsList in itertools.product(
					*[
						StabilizedInitRateFloatsList for Int in xrange(self.StationarizingUnitsInt)
					]
				):

					#Get the solve of the ScipyOptimizeRoot
					StabilizedOptimizeRoot=scipy.optimize.root(
							self.getStationarySpikeRateFloatsTuple,
							__InitRateFloatsList,
							#method='lm',
							#tol=0.001
							options={
										#'maxiter':1000,
										#'ftol':0.001,
										#'direc':np.array([-0.1,0.1])
									},
						)

					#set
					StabilizedErrorFloat = np.sum(StabilizedOptimizeRoot.fun**2)

					#debug
					'''
					self.debug(
						[
							'StabilizedOptimizeRoot is ',
							str(StabilizedOptimizeRoot),
							"StabilizedErrorFloat is ",
							str(StabilizedErrorFloat)
						]
					)
					'''

					#Check
					if StabilizedOptimizeRoot.success and StabilizedErrorFloat<0.001:

						#debug
						'''
						self.debug(
							[
								"It is a sucess !"
							]
						)
						'''

						#append
						self.StationarizedRateFloatsArraysList.append(
							StabilizedOptimizeRoot.x
						)

						self.StationarizedTotalCurrentMeanFloatsListsList.append(
							map(
								lambda __PopulationVariable:
								__PopulationVariable.LifingStationaryExternalCurrentMeanFloat,
								self.TeamDict['Populations'].ManagementDict.values()
							)
						)

						self.StationarizedTotalCurrentNoiseFloatsListsList.append(
							map(
								lambda __PopulationVariable:
								__PopulationVariable.LifingStationaryExternalCurrentNoiseFloat,
								self.TeamDict['Populations'].ManagementDict.values()
							)
						)


				#debug
				'''
				self.debug(
					[
						"In the end ",
						('self.',self,[
								'StationarizedRateFloatsArraysList',
								'StationarizedTotalCurrentMeanFloatsListsList',
								'StationarizedTotalCurrentNoiseFloatsListsList'
							])
					]
				)
				'''

		else:

			#/########################/#
			# Inside structure
			#

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'StationarizedParentSingularStr'
					])
				]
			)
			'''

			#set
			StationarizedMethodKeyStr='stationarize'+self.StationarizedParentSingularStr

			#Check
			if hasattr(self,StationarizedMethodKeyStr):

				#/########################/#
				# call the special stationarize<StationarizedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.StationarizedParentSingularStr+' level',
						'We stationarize<StationarizedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					StationarizedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted stationarize'+self.StationarizedParentSingularStr
					]
				)
				'''	
	
	def stationarizeNetwork(self):

		#/###################/#
		# Determine the weights
		# 

		#debug
		'''
		self.debug(
			[
				'We stationarize network here',
			]
		)
		'''

		#import
		import numpy as np

		#Check
		if type(self.StationarizingMeanWeightVariable) != None.__class__:

			#alias
			self.StationarizedMeanWeightFloatsList=np.array(
				self.StationarizingMeanWeightVariable
			)

			#set
			self.StationarizingUnitsInt=len(self.StationarizedMeanWeightFloatsList)

		#/###################/#
		# Determine the structures
		# 

		#map
		map(
			lambda __TagStr:
			SYS.setInitList(
				self,'Stationarize',__TagStr
			),
			[
				'ConstantTime',
				'Threshold',
				'Reset',
				'Rate',
				'ExternalCurrentMean',
				'ExternalCurrentNoise',
				'MeanWeight',
				'NoiseWeight'
			]
		)

		#debug
		'''
		self.debug(
			[
				"Now ",
				('self.',self,[
						"DoUnitsInt",
						"StationarizedThresholdFloatsList",
						"StationarizedResetFloatsList",
						"StationarizedMeanWeightFloatsList",
						"StationarizedExternalCurrentMeanFloatsList"
					])
			]
		)
		'''

		#Check
		self.StationarizingUnitsInt=max(self.StationarizingUnitsInt,self.DoUnitsInt)

		#/###################/#
		# Determine the name
		# 

		#Check
		if self.StationarizingPopulationTagVariable == None:

			#set
			self.StationarizedPopulationTagStrsList=map(
				str,range(self.StationarizingUnitsInt)
			)
		
		else:

			#set
			self.StationarizedPopulationTagStrsList=self.StationarizingPopulationTagVariable

		#set
		self.StationarizedMeanWeightFloatsArray = np.array(
				self.StationarizingMeanWeightVariable
			)

		#/###################/#
		# Check for Populations
		# 

		#get
		StationarizedPopulationsDeriveTeamer=self.getTeamer(
			"Populations"
		)

		#map
		map(
			lambda __StationarizedPopulationTagStr:
			StationarizedPopulationsDeriveTeamer.getManager(
				str(__StationarizedPopulationTagStr)
			),
			self.StationarizedPopulationTagStrsList,
		)

	def stationarizePopulation(self):

		#debug
		'''
		self.debug(
			[
				'We stationarize population here',
				'First we get some parameters setted at the network level'
			]
		)
		'''

		#Determine parent
		self.StationarizedNetworkDeriveStationarizerVariable = self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#map
		map(
			lambda __TagStr,__NetworkVariable:
			setattr(
				self,
				"Lifing"+__TagStr+"Float",
				__NetworkVariable[self.ManagementIndexInt]
			)
			if len(__NetworkVariable)>self.ManagementIndexInt and __NetworkVariable[self.ManagementIndexInt]!=None
			else None,
			*zip(
				*(map(
					lambda __TagStr:
					(
						__TagStr,
						getattr(
							self.StationarizedNetworkDeriveStationarizerVariable,
							"Stationarized"+__TagStr+"FloatsList"
						)
					),
					[
						"ConstantTime",
						"Threshold",
						"Reset"
					]
				)+[
						(
							"StationaryRate",
							getattr(
									self.StationarizedNetworkDeriveStationarizerVariable,
									"StationarizedRateFloatsList"
								)
						)
					]
				)
			)
		)

		#debug
		'''
		self.debug(
			[
				"self.StationarizedNetworkDeriveStationarizerVariable.StationarizedMeanWeightFloatsList is ",
				str(self.StationarizedNetworkDeriveStationarizerVariable.StationarizedMeanWeightFloatsList)
			]
		)
		'''

		#/#############/#
		# Get the mean of the weights
		#

		#set
		if len(
			self.StationarizedNetworkDeriveStationarizerVariable.StationarizedMeanWeightFloatsList
		)>self.ManagementIndexInt and self.StationarizedNetworkDeriveStationarizerVariable.StationarizedMeanWeightFloatsList[self.ManagementIndexInt]!=None:

			#set
			self.StationarizedMeanWeightFloatsArray = np.array(
				self.StationarizedNetworkDeriveStationarizerVariable.StationarizedMeanWeightFloatsList[
					self.ManagementIndexInt
				]
			)
		else:

			#set
			self.StationarizedMeanWeightFloatsArray = np.zeros(
				self.StationarizedNetworkDeriveStationarizerVariable.StationarizingUnitsInt,
				dtype=float
			)

		#debug
		'''
		self.debug(
			[
				"Now",
				('self.',self,[
						'StationarizedMeanWeightFloatsArray'
					])
			]
		)
		'''

		#/#############/#
		# Get the std of the weights
		#

		#set
		if len(
			self.StationarizedNetworkDeriveStationarizerVariable.StationarizedNoiseWeightFloatsList
		)>self.ManagementIndexInt and self.StationarizedNetworkDeriveStationarizerVariable.StationarizedNoiseWeightFloatsList[self.ManagementIndexInt]!=None:

			#set
			self.StationarizedNoiseWeightFloatsArray = np.array(
				self.StationarizedNetworkDeriveStationarizerVariable.StationarizedNoiseWeightFloatsList[
					self.ManagementIndexInt
				]
			)
		else:

			#set
			self.StationarizedNoiseWeightFloatsArray = np.zeros(
				self.StationarizedNetworkDeriveStationarizerVariable.StationarizingUnitsInt,
				dtype=float
			)

		#set
		self.StationarizedSquareWeightFloatsArray=self.StationarizedNoiseWeightFloatsArray**2

		#debug
		'''
		self.debug(
			[
				"Now",
				('self.',self,[
						'StationarizedNoiseWeightFloatsArray',
						'StationarizedSquareWeightFloatsArray'
					])
			]
		)
		'''

		#/#############/#
		# Look the type of computation
		#

		#set
		self.LifingMeanToRateBool=type(
			self.StationarizedNetworkDeriveStationarizerVariable.StationarizingRateVariable
		)==None.__class__

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'LifingMeanToRateBool'
					])
			]
		)
		'''

		#Check
		if self.LifingMeanToRateBool==False:

			#Check
			if self.StationarizedNetworkDeriveStationarizerVariable.StationarizingInteractionStr=="Spike":

				#debug
				'''
				self.debug(
					[
						"Ok we are going maybe to lif",
						('self.',self,[
								'LifingMeanToRateBool'
							])
					]
				)
				'''

				#
				#self.Lifing

				#lif
				self.lif()

		else:

			#Check
			if self.StationarizedNetworkDeriveStationarizerVariable.StationarizingInteractionStr=="Rate":

				#set
				self.LifedStationaryTotalFloat = self.LifedStationaryRateFloat

		#debug
		'''
		self.debug(
			[
				"After lif",
				('self.',self,[
						'LifingMeanToRateBool',
						'LifedStationaryTotalFloat',
						'LifedStationaryRateFloat'
					]
				)
			]
		)
		'''

	def getStationaryRateFloat(self,_StationaryRateFloatsArray):
			
		#return
		return 0.

	def getStationarySpikeRateFloatsTuple(self,_StationaryRateFloatsArray):
			
		#debug
		'''
		self.debug(
			[
				"pre rate are ",
				"_StationaryRateFloatsArray is "+str(_StationaryRateFloatsArray),
				#('self.',self,[
				#		'StationarizedExternalCurrentMeanFloatsList',
				#		'StationarizedExternalCurrentNoiseFloatsList',
				#		'StationarizedMeanWeightFloatsList',
				#		'StationarizedNoiseWeightFloatsList'
				#	])
			]
		)
		'''
		
		#init
		LifedStationaryRateFloatsList=[0. for __Int in xrange(len(self.TeamDict['Populations'].ManagementDict))]

		#debug
		for __PopulationVariable in self.TeamDict['Populations'].ManagementDict.values():
			

			__PopulationVariable.LifingStationaryExternalCurrentMeanFloat=self.StationarizedExternalCurrentMeanFloatsList[
				__PopulationVariable.ManagementIndexInt
			] +np.sum(
						(
							#self.StationarizingUnitsInt*__PopulationVariable.LifingConstantTimeFloat*_StationaryRateFloatsArray)*__PopulationVariable.StationarizedMeanWeightFloatsArray
							__PopulationVariable.LifingConstantTimeFloat*_StationaryRateFloatsArray
						)*__PopulationVariable.StationarizedMeanWeightFloatsArray
					)

			__PopulationVariable.LifingStationaryExternalCurrentNoiseFloat=np.sqrt(
						(
							self.StationarizedExternalCurrentNoiseFloatsList[
								__PopulationVariable.ManagementIndexInt
							]**2
							if self.StationarizedExternalCurrentNoiseFloatsList[
								__PopulationVariable.ManagementIndexInt
							]!=None
							else 0.
						)+np.sum(
							(
								#self.StationarizingUnitsInt*__PopulationVariable.LifingConstantTimeFloat*_StationaryRateFloatsArray
								__PopulationVariable.LifingConstantTimeFloat*_StationaryRateFloatsArray
							)*__PopulationVariable.StationarizedSquareWeightFloatsArray
						)
					)

			__PopulationVariable.LifingComputeStationaryBool=True
			__PopulationVariable.lif()


			LifedStationaryRateFloatsList[__PopulationVariable.ManagementIndexInt
			]=__PopulationVariable.LifedStationaryRateFloat

			#debug
			'''
			self.debug(
				[
					('__PopulationVariable.',__PopulationVariable,[
							'LifingStationaryExternalCurrentMeanFloat',
							'LifingStationaryExternalCurrentNoiseFloat',
							'LifedStationaryRateFloat'

						])

				]
			)
			'''

		'''
		#map
		LifedStationaryRateFloatsList = map(
			lambda __PopulationVariable,__StationarizedExternalCurrentMeanFloat,__StationarizedExternalCurrentNoiseFloat:
			__PopulationVariable.mapSetAttr(
				{
					'LifingStationaryExternalCurrentMeanFloat':__StationarizedExternalCurrentMeanFloat+np.sum(
						(__PopulationVariable.LifingConstantTimeFloat*_StationaryRateFloatsArray)*__PopulationVariable.StationarizedMeanWeightFloatsArray
					),
					'LifingStationaryExternalCurrentNoiseFloat':np.sqrt(
						(
							__StationarizedExternalCurrentNoiseFloat**2
							if __StationarizedExternalCurrentNoiseFloat!=None
							else 0.
						)+np.sum(
							(
								__PopulationVariable.LifingConstantTimeFloat*_StationaryRateFloatsArray
							)*__PopulationVariable.StationarizedNoiseWeightFloatsArray
						)
					),
					'LifingComputeStationaryBool':True
				}
			).lif(
			).LifedStationaryRateFloat,
			self.TeamDict['Populations'].ManagementDict.values(),
			self.StationarizedExternalCurrentMeanFloatsList,
			self.StationarizedExternalCurrentNoiseFloatsList
		)
		'''


		#debug
		'''
		self.debug(
			[
				"post rate are ",
				"LifedStationaryRateFloatsList is "+str(LifedStationaryRateFloatsList)
			]
		)
		'''

		#return
		return LifedStationaryRateFloatsList-_StationaryRateFloatsArray

	#/######################/#
	# Augment view
	#
	
	def mimic_view(self):

		#Check
		if self.StationarizedNetworkDeriveStationarizerVariable==self:

			#get the Panels
			ViewedPanelsDerivePyploter=self.getTeamer(
				'Panels'
			)

			#/################/#
			# Build a plot of the isolate transfer
			#

			#map
			StationarizedFrequencyFloatsArray=SYS.numpy.array(
			    [
			        0.
			     ]+list(
			        SYS.numpy.logspace(0,3,100)
			       #[130.]
			    )
			);

			#get
			StationarizedAgentLifer=self.TeamDict['Populations'].ManagementDict.getValue(0) 

			#set
			StationarizedAgentLifer.LifingPerturbationMethodStr="Brunel"
			StationarizedAgentLifer.LifingPerturbationLambdaVariable=None
			StationarizedAgentLifer.LifingComputePerturbationBool=True

			#map
			LifedPerturbationMeanComplexesArray=SYS.numpy.array(
				map(
					lambda __StationarizedFrequencyFloat:
					StationarizedAgentLifer.lif(   
						_PerturbationFrequencyFloat=__StationarizedFrequencyFloat
					).LifedPerturbationMeanComplexVariable,
					StationarizedFrequencyFloatsArray
				)
			)

			#debug
			'''
			self.debug(
				[
					"LifedPerturbationMeanComplexesArray is "+str(
						LifedPerturbationMeanComplexesArray
					)
				]
			)
			'''

			#get
			ViewedChartsDerivePyploter = ViewedPanelsDerivePyploter.getManager(
				'NeuralFunction',
				_IndexInt=1
			).getTeamer(
				'Charts'
			)

			#
			# Amplitude
			#

			ViewedAmplitudeChartDerivePyploter=ViewedChartsDerivePyploter.getManager(
				'Amplitude'
			)

			ViewedAmplitudeDrawDerivePyploter=ViewedAmplitudeChartDerivePyploter.getTeamer(
				'Draws'
			).getManager(
				'Default'
			)

			#set
			ViewedAmplitudeDrawDerivePyploter.PyplotingDrawVariable=[
				(	
					'plot',
					{
						'#liarg':[
							StationarizedFrequencyFloatsArray,
							abs(LifedPerturbationMeanComplexesArray)
						],
						'#kwarg':{
							'linestyle':'-',
							'linewidth':5,
							'color':"blue"
						}
					}
				)
			]

			ViewedAmplitudeChartDerivePyploter.PyplotingChartVariable=[
				(
					'plot',
					{
						'#liarg':[
							[1.,100.],
			   				[StationarizedAgentLifer.LifedPerturbationMeanNullFloat]*2,
						],
						'#kwarg':{
							'linestyle':'--',
							'linewidth':3,
							'color':"blue"
						}
					}
				),
				('set_xscale','log')
			]

			#
			# Phase
			#

			ViewedPhaseChartDerivePyploter=ViewedChartsDerivePyploter.getManager(
				'Phase'
			)

			ViewedPhaseDrawDerivePyploter=ViewedPhaseChartDerivePyploter.getTeamer(
				'Draws'
			).getManager(
				'Default'
			)

			#set
			ViewedPhaseDrawDerivePyploter.PyplotingDrawVariable=[
				(	
					'plot',
					{
						'#liarg':[
							StationarizedFrequencyFloatsArray,
							SYS.getArgumentVariable(LifedPerturbationMeanComplexesArray)
						],
						'#kwarg':{
							'linestyle':'-',
							'linewidth':5,
							'color':"blue"
						}
					}
				)
			]

			ViewedPhaseChartDerivePyploter.PyplotingChartVariable=[
				('set_xscale','log')
			]

		#call the base method
		BaseClass.view(self)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Print things if they are computed
			#

			#Check
			if self.StationarizedNetworkDeriveStationarizerVariable==self:

				#map
				map(
						lambda __KeyStr:
						self.forcePrint(
							[__KeyStr],
							'StationarizerClass'
						)
						if getattr(
							self.PrintingCopyVariable,
							__KeyStr
						) not in [None,0.,""]
						else None,
						[
							'StationarizingConstantTimeVariable'
						]
					)

			else:

				#/##################/#
				# Call the base method
				#


				#call
				BaseClass._print(self,**_KwargVariablesDict)

				#return
				return 


		#/##################/#
		# Call the base method
		#

		#call
		#Leaker.LeakerClass._print(self,**_KwargVariablesDict)
		BaseClass._print(self,**_KwargVariablesDict)


#</DefineClass>

#</DefineLocals>
Leaker.LeakersStructurerClass.ManagingValueClass=StationarizerClass
#<DefineLocals>

#</DefinePrint>
StationarizerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'StationarizingUnitsInt',
		'StationarizingWeightVariable',
		'StationarizingConstantTimeVariable',
		'StationarizingThresholdVariable',
		'StationarizingResetVariable',
		'StationarizingExternalCurrentNoiseVariable',
		'StationarizingExternalCurrentMeanVariable',
		'StationarizingMeanWeightVariable',
		'StationarizingNoiseWeightVariable',
		'StationarizingRateVariable',
		'StationarizingPopulationTagVariable',
		'StationarizingInteractionStr',
		'StationarizingWeightFloatsArray',
		'StationarizedConstantTimeFloatsList',
		'StationarizedThresholdFloatsList',
		'StationarizedExternalNoiseFloatsList',
		'StationarizedResetFloatsList',
		'StationarizedExternalCurrentMeanFloatsList',
		'StationarizedExternalCurrentNoiseFloatsList',
		'StationarizedRateFloatsList',
		'StationarizedTotalCurrentMeanFloatsListsList',
		'StationarizedTotalCurrentNoiseFloatsListsList',
		'StationarizedMeanWeightFloatsList',
		'StationarizedNoiseWeightFloatsList',
		'StationarizedMeanWeightFloatsArray',
		'StationarizedNoiseWeightFloatsArray',
		'StationarizedSquareWeightFloatsArray',
		'StationarizedRateFloatsArraysList',
		'StationarizedPopulationTagStrsList',
		'StationarizedParentSingularStr',
		'StationarizedNetworkDeriveStationarizerVariable'
	]
)
#<DefinePrint>