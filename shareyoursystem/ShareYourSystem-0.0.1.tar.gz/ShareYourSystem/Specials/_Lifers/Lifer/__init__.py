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
BaseModuleStr="ShareYourSystem.Standards.Recorders.Leaker"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Lifer','Lif','Lifing','Lifed')
#</DefineAugmentation>

#<DefineLocals>
def getFilterDictByType(**_Dict):

	#init
	FilteredDict={'ComplexDict':{},'DoubleDict':{},'IntDict':{},'StringDict':{}};

	#map
	map(
		lambda __ItemTuple:
		FilteredDict[
			getCTypeNameFromPythonType(
				type(
					__ItemTuple[1]
					)
			)+'Dict'
		].__setitem__(*__ItemTuple),
		_Dict.items()
	)	

	#return
	return FilteredDict;
SYS.getFilterDictByType=getFilterDictByType
def getCTypeNameFromPythonType(_PythonType):

	#import
	import numpy as np

	#check
	if _PythonType in [float,np.float64]:
		return 'Double'
	elif _PythonType in [int]:
		return 'Int'
	elif _PythonType in [str]:
		return 'String'; 
SYS.getCTypeNameFromPythonType=getCTypeNameFromPythonType
def getCArgsFromDict(Dict):
    CArgs=[]
    DictOrderedKeys=Dict.keys()
    for Key in sorted(Dict):
        CArgs.append(Dict[Key]);
    return CArgs;
SYS.getCArgsFromDict=getCArgsFromDict
def getArgumentVariable(_ComplexVariable):

	#Debug
	'''
	print('l 31 Numscipier')
	print('_ComplexVariable is ')
	print(_ComplexVariable)
	print('')
	'''

	#import
	import numpy as np

	#return
	return 2.*np.arctan(
	np.imag(_ComplexVariable)/(
	        np.sqrt(
	            np.imag(
	                _ComplexVariable
	            )**2+np.real(
	                _ComplexVariable
	            )**2)+np.real(
	                _ComplexVariable
	            )
	    )
	);
SYS.getArgumentVariable=getArgumentVariable
#</DefineLocals>

#</DefineLocals>

#<DefineClass>
@DecorationClass()
class LiferClass(BaseClass):
	
	def default_init(self, 
			_LifingConstantTimeFloat = 0.02, 
			_LifingRefractoryPeriodFloat = 0.,
			_LifingRestFloat = -70., 
			_LifingResetFloat = -60., 
			_LifingThresholdFloat = -50.,
			_LifingStationaryExternalCurrentMeanFloat = 0.,
			_LifingStationaryExternalCurrentNoiseFloat = 5., 
			_LifingStationaryRateFloat = 5., 
			_LifingMeanToRateBool = True,
			_LifingNoiseToRateBool = True,
			_LifingComputeStationaryBool = True,
			_LifingPerturbationLambdaVariable = None,
			_LifingPerturbationFrequencyFloat = None,
			_LifingPerturbationMethodStr = 'Brunel',
			_LifingComputeNoisePerturbationBool = False,
			_LifingComputePerturbationBool = True,
			_LifedSwigVariable = None,
			_LifedStationaryTotalFloat = None,
			_LifedStationaryRateFloat = None,
			_LifedPerturbationMeanNullFloat = 0.,
			_LifedPerturbationNoiseNullFloat = 0.,
			_LifedPerturbationMethodVariable = None,
			_LifedPerturbationMeanComplexVariable = None,
			_LifedPerturbationNoiseComplexVariable = None,
			_LifedInverseStationaryFunctionVariable = None,
			**_KwargVariablesDict
		):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_lif(self):
		
		#/##################/#
		# Get the swig function
		#

		#Check
		if self.LifedSwigVariable==None:

			#import
			import sys
			from os.path import dirname
			sys.path.append(dirname(__file__))
			import CIntegrateAndFireTransferFunction

			#get
			self.LifedSwigVariable=CIntegrateAndFireTransferFunction.CIntegrateAndFireTransferFunctionClass()

		#debug
		'''
		self.debug(
			[
				'We have getted dthe Lif swig variable',
				('self.',self,[
						'LifedSwigVariable'
					])
			]
		)
		'''

		#/##################/#
		# Look if the stationary point was already computed
		#

		#debug
		'''
		self.debug(
			[
				"The stationary point was computed ?",
				('self.',self,['LifingComputeStationaryBool'])
			]
		)
		'''

		#set
		self.LifedSwigVariable.IntDict['ComputeStationary']=int(
			self.LifingComputeStationaryBool
		)

		#Check
		if self.LifingComputeStationaryBool:

			#debug
			'''
			self.debug(
				[
					'We lif compute stationary here',
					('self.',self,[
							'LifingConstantTimeFloat',
							'LifingRefractoryPeriodFloat',
							'LifingStationaryRateFloat',
							'LifingRestFloat',
							'LifingStationaryExternalCurrentNoiseFloat',
							'LifingResetFloat',
							'LifingThresholdFloat'
						])
				]
			)
			'''

			#Set inside the Swig
			self.LifedSwigVariable.setDicts(
				*getCArgsFromDict(
					getFilterDictByType(**{
							'ConstantTime':self.LifingConstantTimeFloat,
							'RefractoryPeriod':self.LifingRefractoryPeriodFloat,
							'VoltageReset':self.LifingResetFloat, 
							'VoltageThreshold':self.LifingThresholdFloat
						}
					)
				)
			)

			#Check
			if self.LifingMeanToRateBool:

				#set
				self.LifedStationaryTotalFloat = self.LifingRestFloat+self.LifingStationaryExternalCurrentMeanFloat

				#Set inside the Swig
				self.LifedSwigVariable.setDicts(
					*getCArgsFromDict(
						getFilterDictByType(**{
								'StationaryCurrent':self.LifedStationaryTotalFloat,
								'VoltageNoise':self.LifingStationaryExternalCurrentNoiseFloat
							}
						)
					)
				)

				#Compute the IntegralLowerBound and the IntegralUpperBound
				self.LifedSwigVariable.computeIntegralLowerBound();
				self.LifedSwigVariable.computeIntegralUpperBound();
		    	
				#set
				self.LifedStationaryRateFloat=self.LifedSwigVariable.getLifStationaryRate();

				#debug
				'''
				self.debug(
					[
						"This is rate from current and we have",
						('self.',self,[
								'LifingConstantTimeFloat',
								'LifingRefractoryPeriodFloat',
								'LifingRestFloat',
								'LifingResetFloat',
								'LifingThresholdFloat',
								'LifingStationaryExternalCurrentNoiseFloat',
								'LifedStationaryTotalFloat',
								'LifedStationaryRateFloat'
							])
					]
				)
				'''
				
			#Check
			else:

				#debug
				'''
				self.debug(
					[
						"This is current from rate",
						('self',self,[
								'LifingStationaryRateFloat'
							])
					]
				)
				'''

				#temp
				LifedTempRateFloat=self.LifingStationaryRateFloat

				#set
				if self.LifedInverseStationaryFunctionVariable == None:

					#get
					self.LifedInverseStationaryFunctionVariable=SYS.getInverseFunction(
						lambda __StationaryCurrentFloat:
						self.mapSetAttr(
								{
									'LifingRestFloat':__StationaryCurrentFloat,
									'LifingStationaryRateFloat':None,
									'LifingMeanToRateBool':True,
									'LifingComputeStationaryBool':True
								}
							).lif(
							).LifedStationaryRateFloat
						)
				
				#set
				self.LifedStationaryTotalFloat = self.LifedInverseStationaryFunctionVariable(
					LifedTempRateFloat
				)

				#set
				self.LifingStationaryRateFloat = LifedTempRateFloat

				#set
				self.LifingMeanToRateBool=False
				
				#set
				self.LifedStationaryRateFloat = None

				#Set inside the Swig
				self.LifedSwigVariable.setDicts(
					*getCArgsFromDict(
						getFilterDictByType(**{
								'StationaryCurrent':self.LifedStationaryTotalFloat,
								'VoltageNoise':self.LifingStationaryExternalCurrentNoiseFloat
							}
						)
					)
				)

				#debug
				'''
				self.debug(
					[
						"In the end of rateToCurrent",
						('self.',self,[
								'LifingStationaryRateFloat',
								'LifedStationaryTotalFloat'
							])
					]
				)
				'''
				
			#set
			self.LifingComputeStationaryBool=False
			self.LifedSwigVariable.IntDict['ComputeStationary']=0

		#debug
		'''
		self.debug(
			[
				"In the end",
				('self.',self,[
					'LifingMeanToRateBool',
					'LifingRestFloat',
					'LifingStationaryRateFloat',
					'LifedStationaryTotalFloat',
					'LifedStationaryRateFloat',
					'LifingComputePerturbationBool'
				])
			]
		)
		'''

		#Check
		if self.LifingComputePerturbationBool:

			#/##################/#
			# Compute a perturbaton
			#

			#debug
			'''
			self.debug(
				[
					"We compute a perturbation",
					('self.',self,[
							'LifingPerturbationFrequencyFloat',
							'LifingPerturbationLambdaVariable'
						])
				]
			)
			'''

			#/##################/#
			# Get the method
			#

			#Check
			if self.LifingPerturbationMethodStr == "Rate":

				#alias
				self.LifedPerturbationMethodVariable = self.setRatePerturbationRate

				#Check
				if self.LifedPerturbationMeanNullFloat==0.:

					#set
					self.LifedPerturbationMeanNullFloat=self.LifedSwigVariable.getLifPerturbationNullRate(
						'StationaryCurrent'
					)

			else:

				#get
				self.LifedPerturbationMethodVariable = getattr(
					self.LifedSwigVariable,
					'set'+self.LifingPerturbationMethodStr+'LifPerturbationRate'
				)


			#/#################/#
			# Check if it is real or complex
			#

			#Choose
			if self.LifingPerturbationLambdaVariable!=None:

				#set
				LifedPerturbationPreVariable=self.LifingPerturbationLambdaVariable

			else:

				#import
				import numpy as np

				#set
				LifedPerturbationPreVariable=2.*np.pi*self.LifingPerturbationFrequencyFloat*1j

			#/#################/#
			# Check if it null perturbation or complex
			#

			#debug
			'''
			self.debug(
				[
					'LifedPerturbationPreVariable is ',str(
						LifedPerturbationPreVariable)
				]
			)
			'''

			#unpack
			if LifedPerturbationPreVariable==0.:

				#debug
				'''
				self.debug(
					[
						"It is a get of real null perturbation"
					]
				)
				'''

				#get
				self.LifedPerturbationMeanComplexVariable=self.LifedSwigVariable.getLifPerturbationNullRate(
						'StationaryCurrent'
					)

				#set
				self.LifedPerturbationMeanNullFloat=self.LifedPerturbationMeanComplexVariable

				#Check
				if self.LifingComputeNoisePerturbationBool:

					#get
					self.LifedPerturbationNoiseComplexVariable=self.LifedSwigVariable.getLifPerturbationNullRate(
							'VoltageNoise'
						)

					#set
					self.LifedPerturbationNoiseNullFloat=self.LifedPerturbationMeanComplexVariable


			else:

				#debug
				'''
				self.debug(
					[
						"It is a complex computation",
						"LifedPerturbationPreVariable is "+str(
							LifedPerturbationPreVariable
						),
						('self.',self,[
									'LifingConstantTimeFloat',
									'LifingRefractoryPeriodFloat',
									'LifingRestFloat',
									'LifingStationaryExternalCurrentMeanFloat',
									'LifingStationaryExternalCurrentNoiseFloat',
									'LifingResetFloat',
									'LifingThresholdFloat',
									'LifedStationaryTotalFloat',
									'LifedStationaryRateFloat',
									'LifingMeanToRateBool'
								])
					]
				)
				'''

				#get
				if self.LifingPerturbationMethodStr != "Rate":
					
					#set
					self.LifedSwigVariable.IntDict['ComputeNoise']=int(
						self.LifingComputeNoisePerturbationBool
					)


				#debug
				'''
				self.debug(
					[
						"Ok we call",
						"LifedPerturbationPreVariable is "+str(LifedPerturbationPreVariable),
						('self.',self,[
								'LifedPerturbationMethodVariable'
							])
					]
				)
				'''
				
				#call
				self.LifedPerturbationMethodVariable(
					LifedPerturbationPreVariable
				)

				#get
				if self.LifingPerturbationMethodStr != "Rate":
					
					#get
					self.LifedPerturbationMeanComplexVariable=self.LifedSwigVariable.ComplexDict["PerturbationMean"]

					#Check			
					if self.LifingComputeNoisePerturbationBool:
						self.LifedPerturbationNoiseComplexVariable=self.LifedSwigVariable.ComplexDict["PerturbationNoise"]

				#debug
				'''
				self.debug(
					[
						('self.',self,[
								'LifedPerturbationMeanComplexVariable'
							])
					]
				)
				'''
			
	def setRatePerturbationRate(self,_PerturbationComplex):

		#set
		self.LifedPerturbationMeanComplexVariable = self.LifedPerturbationMeanNullFloat/(
			1.+self.LifingConstantTimeFloat*_PerturbationComplex
		)

		#debug
		'''
		self.debug(
			[
				'_PerturbationComplex is '+str(_PerturbationComplex),
				('self.',self,[
						'LifedPerturbationMeanComplexVariable',
						'LifedPerturbationMeanNullFloat'
					])
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
			# Print things if they are computed
			#

			#Check
			if (
				self.ParentDeriveTeamerVariable==None and 'Populations' not in self.TeamDict
			) or (
				self.ParentDeriveTeamerVariable!=None and self.ParentDeriveTeamerVariable.TeamTagStr=="Populations"
			):

				#map
				map(
						lambda __KeyStr:
						self.forcePrint(
							[__KeyStr],
							'LiferClass'
						)
						if getattr(self.PrintingCopyVariable,__KeyStr) not in [None,0.]
						else None,
						[
							'LifingConstantTimeFloat', 
							'LifingRefractoryPeriodFloat',
							'LifingStationaryExternalCurrentNoiseFloat', 
							'LifingResetFloat', 
							'LifingThresholdFloat',
							'LifingPerturbationLambdaVariable',
							'LifingPerturbationFrequencyFloat',
							'LifingPerturbationMethodStr',
							'LifedPerturbationMeanNullFloat',
							'LifedPerturbationNoiseNullFloat',
							'LifedPerturbationMeanComplexVariable',
							'LifedPerturbationNoiseComplexVariable',
						]+(['LifingStationaryExternalCurrentMeanFloat'] if self.LifingMeanToRateBool else [])
						+(['LifingStationaryRateFloat'] if self.LifingMeanToRateBool==False else [])
						+(['LifedStationaryTotalFloat'] if self.LifingMeanToRateBool==False else [])
						+(['LifedStationaryRateFloat'] if self.LifingMeanToRateBool else [])
					)

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

#</DefineClass>

#</DefinePrint>
LiferClass.PrintingClassSkipKeyStrsList.extend(
	[
		'LifingConstantTimeFloat', 
		'LifingRefractoryPeriodFloat',
		'LifingRestFloat', 
		'LifingStationaryRateFloat',
		'LifingMeanToRateBool',
		'LifingNoiseToRateBool',
		'LifingStationaryExternalCurrentMeanFloat',
		'LifingStationaryExternalCurrentNoiseFloat', 
		'LifingResetFloat', 
		'LifingThresholdFloat',
		'LifingComputeStationaryBool',
		'LifingPerturbationLambdaVariable',
		'LifingPerturbationFrequencyFloat',
		'LifingPerturbationMethodStr',
		'LifingComputeNoisePerturbationBool',
		'LifingComputePerturbationBool',
		'LifedSwigVariable',
		'LifedStationaryTotalFloat',
		'LifedStationaryRateFloat',
		'LifedPerturbationMeanNullFloat',
		'LifedPerturbationNoiseNullFloat',
		'LifedPerturbationMethodVariable',
		'LifedPerturbationMeanNullFloat=0.,',
		'LifedPerturbationMeanComplexVariable',
		'LifedPerturbationNoiseComplexVariable',
		'LifedInverseStationaryFunctionVariable'
	]
)
#<DefinePrint>