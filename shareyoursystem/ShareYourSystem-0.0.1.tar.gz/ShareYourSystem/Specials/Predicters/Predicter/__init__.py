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
SYS.addDo('Predicter','Predict','Predicting','Predicted')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Recorders import Recorder,Leaker
import scipy.stats
import numpy as np
PredictSlowTimeFloat=10.
#</ImportSpecificModules>

#<DefineLocals>
def getNullFloatsArray(_FloatsArray, _RtolFloat=1e-5):
	u, s, v = np.linalg.svd(_FloatsArray)
	RankInt = (s > _RtolFloat*s[0]).sum()
	return v[RankInt:].T.copy()

class DynamicDict(dict):

	def __init__(self,*_LiargVariablesList,**_KwargVariablesDict):

		#init
		dict.__init__(self,*_LiargVariablesList,**_KwargVariablesDict)

		#map
		map(
			lambda __ItemTuple:
			self.__setitem__(
				*__ItemTuple
			) if __ItemTuple[0] not in self
			else None,
			[
				('ModeStr',"Track"),
				('ConstantTimeFloat',PredictSlowTimeFloat)
			]
		)

#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PredicterClass(BaseClass):
	
	def default_init(self,
			_PredictingSensorUnitsInt = 1,
			_PredictingAgentUnitsInt = 1,
			_PredictingDaleBool = False,
			_PredictingDynamicBool = True,
			_PredictingJacobianVariable = None,
			_PredictingCommandVariable = None,
			_PredictingEncodPerturbStdFloat = 0.,
			_PredictingEncodWeightVariable = None,
			_PredictingRateCostVariable = None,
			_PredictingRateTransferVariable = None,
			_PredictingAgentRestVariable = None,
			_PredictingAgentResetVariable = None,
			_PredictingAgentNoiseVariable = None,
			_PredictingAgentThresholdVariable = None,
			_PredictingAgentRefractoryVariable = None,
			_PredictingAgentRecordVariable = None,
			_PredictingAgentTimeFloat = 10.,
			_PredictingDecoderVariable = None,
			_PredictingDecoderMeanVariable = None,
			_PredictingDecoderStdFloat = 1.,
			_PredictingDecoderSparseFloat=0.,
			_PredictingDecoderTimeFloat = PredictSlowTimeFloat,
			_PredictingDecoderRecordVariable = None,
			_PredictingFastPerturbStdFloat=0.,
			_PredictingFastSymmetryFloat=1.,
			_PredictingSlowPerturbStdFloat=0.,
			_PredictingInteractionStr="Rate",
			_PredictingEncodPlasticBool=False,
			_PredictingFastPlasticBool=False,
			_PredictingFastLearnRateFloat=0.01,
			_PredictingFastWeightVariable=None,
			_PredictingDelayFloat=0.,
			_PredictingStationaryBool=False,
			_PredictingSpikeRecordVariable=None,
			_PredictedDynamicDict=None,
			_PredictedSensorJacobianFloatsArray=None,
			_PredictedDecoderFloatsArray=None,
			_PredictedFastFloatsArray=None,
			_PredictedThresholdFloatsArray=None,
			_PredictedSlowFloatsArray=None,
			_PredictedParentSingularStr="",
			_PredictedSlowBool=True,
			_PredictedDelayFloatsArray=None,
			_PredictedDecoderInverseFloatsArray=None,
			_PredictedSensorDerivePredicterVariable=None,
			_PredictedAgentDerivePredicterVariable=None,
			_PredictedDecoderDerivePredicterVariable=None,
			_PredictedNetworkDerivePredicterVariable=None,
			**_KwargVariablesDict
		):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	#/######################/#
	# predict
	#

	def do_predict(self):

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
			self.PredictedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['PredictedParentSingularStr'])
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
		]) and self.PredictedParentSingularStr!='Population':

			#/########################/#
			# Network level
			# 

			#debug
			'''
			self.debug(
				[
					'It is a Network level for the predict',
				]
			)
			'''

			#/########################/#
			# Determine parent level
			# 

			#alias
			self.PredictedNetworkDerivePredicterVariable=self

			#/########################/#
			# predictNetwork
			# 

			#predict
			self.predictNetwork()

			#/########################/#
			# structure predict 
			# 

			#debug
			'''
			self.debug(
				[
					'We structure all the predicting children...'
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
						'predict'
					]
			)

			#/########################/#
			# leak
			#

			#leak
			self.leak()
			

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
						'PredictedParentSingularStr'
					])
				]
			)
			'''

			#set
			PredictedMethodKeyStr='predict'+self.PredictedParentSingularStr

			#Check
			if hasattr(self,PredictedMethodKeyStr):

				#/########################/#
				# call the special predict<PredictedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.PredictedParentSingularStr+' level',
						'We predict<PredictedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					PredictedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted predict'+self.PredictedParentSingularStr
					]
				)
				'''	
	
	def predictNetwork(self):

		#/###################/#
		# Check for Populations
		# 

		#get
		LeakedPopulationsDeriveManager=self.getTeamer("Populations")

		#debug
		'''
		self.debug(
			[
				'We predict network here',
				'Check for a sensor population'
			]
		)
		'''

		#/###################/#
		# Check for Sensor
		# 

		#get
		PredictedSensorDerivePredicter=LeakedPopulationsDeriveManager.getManager(
			"Sensor",
			_IndexInt=0
		)

		#/###################/#
		# Check for Agent
		# 

		#get
		PredictedAgentDerivePredicter=LeakedPopulationsDeriveManager.getManager(
			"Agent",
			_IndexInt=1
		)

		#/###################/#
		# Check for Decoder
		# 

		#get
		PredictedDecoderDerivePredicter=LeakedPopulationsDeriveManager.getManager(
			"Decoder",
			_IndexInt=2
		)

		#debug
		'''
		self.debug(
			[
				'Ok we have created the Decoder'
			]
		)
		'''

		#import
		import numpy as np

		#/###################/#
		# When Command specify the number of sensors
		# 

		#Check
		if type(self.PredictingCommandVariable)==tuple:

			#Check
			if self.PredictingCommandVariable[0].startswith(Leaker.LeakCustomPrefixStr):

				#len
				self.PredictingSensorUnitsInt=len(self.PredictingCommandVariable[1])

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'PredictingSensorUnitsInt'
					])
			]
		)
		'''

		#/###################/#
		# When Decoder matrix is already specified
		# 

		#type
		PredictedDecoderType=type(self.PredictingDecoderVariable)

		#Check
		if PredictedDecoderType in [list,tuple,np.ndarray]: 

			#Check
			self.PredictedDecoderFloatsArray=np.array(
				self.PredictingDecoderVariable
			)

			#shape
			PredictedShapeIntsList=list(
				np.shape(self.PredictingDecoderVariable)
			)

			#debug
			'''
			self.debug(
				[
					'Update the PredictingAgentUnitsInt with the size of the array',
					'PredictedShapeIntsList is ',
					str(PredictedShapeIntsList),
					'len(PredictedShapeIntsList) is',
					str(len(PredictedShapeIntsList))
				]
			)
			'''

			#Check
			if len(PredictedShapeIntsList)==1:

				#get
				self.PredictingAgentUnitsInt=PredictedShapeIntsList[0]

				#recast into a 2D array
				self.PredictedDecoderFloatsArray=np.array(
					[self.PredictedDecoderFloatsArray]
				)
			else:

				#get
				self.PredictingAgentUnitsInt=PredictedShapeIntsList[1]

			#debug
			'''
			self.debug(
				[
					'Now',
					('self.',self,[
							'PredictingAgentUnitsInt'
						])
				]
			)
			'''

		else:

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'PredictingAgentUnitsInt',
							'PredictingSensorUnitsInt'
						])
				]
			)
			'''

			#Check
			if self.PredictingAgentUnitsInt<self.PredictingSensorUnitsInt:

				#debug
				'''
				self.debug(
					[
						'We need to make so many agents compared to the sensors at least'
					]
				)
				'''

				#set
				self.PredictingAgentUnitsInt=self.PredictingSensorUnitsInt

		#/###################/#
		# When Decoder matrix has to be sparse
		# 

		#Check
		if self.PredictingDecoderSparseFloat>0.:

			#debug
			'''
			self.debug(
				[
					'The decoder is built from a sparse matrix, so it infers that',
					'the number of sensors is the same as the number of agents'
				]
			)
			'''

			#set
			self.PredictingSensorUnitsInt=self.PredictingAgentUnitsInt

		#/################/#
		# Build the Jacobian
		#

		#set
		JacobianType = type(self.PredictingJacobianVariable)

		#Check
		if JacobianType in [dict,None.__class__]:

			#init
			self.PredictedDynamicDict = DynamicDict(
					self.PredictingJacobianVariable
				) if self.PredictingJacobianVariable!=None else DynamicDict()

			#alias
			PredictedConstantTimeFloat = self.PredictedDynamicDict['ConstantTimeFloat']

			#Check
			if self.PredictedDynamicDict["ModeStr"]=="Track":

				
				#debug
				'''
				self.debug(
					[
						'We set a sensor variable leaking at'+str(PredictedConstantTimeFloat)
					]
				)
				'''

				#diag
				self.PredictedSensorJacobianFloatsArray =- (1./PredictedConstantTimeFloat)*np.diag(
					np.ones(
						self.PredictingSensorUnitsInt
					)
				)

				#debug
				self.debug(
					[
						('self.',self,[
							'PredictedDynamicDict',
							'PredictedSensorJacobianFloatsArray'
						])
					]
				)


			elif self.PredictedDynamicDict["ModeStr"]=="Damp":

				#Check
				if self.PredictedDynamicDict["LoopIntsList"]==[1]:
					self.PredictingSensorUnitsInt=2
				if self.PredictedDynamicDict["LoopIntsList"]==[1,2]:
					self.PredictingSensorUnitsInt=6

				#debug
				'''
				self.debug(
					[
						'We build the oscillatory jacobian matrix',
						('self.',self,[
								'PredictingSensorUnitsInt'
							])
					]
				)
				'''

				#diag
				self.PredictedSensorJacobianFloatsArray=-np.diag(
					(1./PredictedConstantTimeFloat)*np.ones(
						self.PredictingSensorUnitsInt
					)
				)

				#set
				self.PredictedSensorJacobianFloatsArray[0,0]+=(1.5/PredictedConstantTimeFloat)
				self.PredictedSensorJacobianFloatsArray[1,0]+=-(3.7/PredictedConstantTimeFloat)
				self.PredictedSensorJacobianFloatsArray[0,1]+=(3.7/PredictedConstantTimeFloat)
				self.PredictedSensorJacobianFloatsArray[1,1]+=-(1./PredictedConstantTimeFloat)

				#Check
				if self.PredictedDynamicDict["LoopIntsList"]==[1,2]:

					#set
					self.PredictedSensorJacobianFloatsArray[2,3]+=(1./PredictedConstantTimeFloat)
					self.PredictedSensorJacobianFloatsArray[3,4]+=-(1.2/PredictedConstantTimeFloat)
					self.PredictedSensorJacobianFloatsArray[4,5]+=-(1.4/PredictedConstantTimeFloat)
					self.PredictedSensorJacobianFloatsArray[5,2]+=-(1.6/PredictedConstantTimeFloat)

		else:

			#alias
			self.PredictedSensorJacobianFloatsArray = self.PredictingJacobianVariable
			self.PredictingSensorUnitsInt = np.shape(
				self.PredictedSensorJacobianFloatsArray)[0]

		#debug
		'''
		self.debug(
			[
				'We have prepared the sensor jacobian',
				('self.',self,['PredictedSensorJacobianFloatsArray'])
			]
		)
		'''

		#/################/#
		# Build the DecoderFloatsArray
		#

		#Check
		if PredictedDecoderType==str:

			#/################/#
			# Maybe be we want to scale the weights in order to build realistic neuron threshold
			#

			#debug
			self.debug(
				[
					"Do we have already a Mean float for decoder",
					('self.',self,[
							'PredictingDecoderMeanVariable'
						])
				]
			)

			#Check
			if self.PredictingDecoderSparseFloat>0. and self.PredictingDecoderMeanVariable==None:

				#debug
				self.debug(
					[
						"Look if we have a Threshold",
						('self.',self,[
								'PredictingAgentThresholdVariable'
							])
					]
				)

				#Check
				if type(self.PredictingAgentThresholdVariable)==None.__class__:
					self.PredictingAgentThresholdVariable = 10.

				#sqrt
				self.NumscipyingMeanFloat=np.sqrt(
					2.*self.PredictingAgentUnitsInt*self.PredictingAgentThresholdVariable/self.PredictingDecoderSparseFloat
				)


			else:

				#set
				self.NumscipyingMeanFloat=self.PredictingDecoderMeanVariable/self.PredictingAgentUnitsInt

			#debug
			self.debug(
				[
					'We have setted the mean of the decoder to have neuron threshold',
					('self.',self,[
							'NumscipyingMeanFloat',
							'PredictingDecoderSparseFloat'
						])
				]
			)

			#numscipy
			self.NumscipyingSparseFloat=self.PredictingDecoderSparseFloat
			self.NumscipyingStdFloat=self.PredictingDecoderStdFloat/np.sqrt(
					self.PredictingAgentUnitsInt
				)
			self.NumscipyingRowsInt=self.PredictingSensorUnitsInt
			self.NumscipyingColsInt=self.PredictingAgentUnitsInt

			#debug
			self.debug(
				[
					"We numscipy the decoder weights here",
					('self.',self,[
							'NumscipyingStdFloat',
							'NumscipyingMeanFloat',
							'NumscipyingSeedVariable'
						])
				]
			)


			#call
			self.numscipy()

			#Check
			self.PredictedDecoderFloatsArray=1.*self.NumscipiedValueFloatsArray

		#debug
		'''
		self.debug(
			[
				'We normalize the PredictedDecoderFloatsArray',
				('self.',self,[
						'PredictedDecoderFloatsArray'
					])
			]
		)	
		'''


		#/################/#
		# Build the Fast Connection
		#

		#Check
		if type(self.PredictingFastWeightVariable)!=None.__class__:

			#array
			self.PredictedFastFloatsArray=np.array(
				self.PredictingFastWeightVariable
			)

		else:

			#Check
			if self.PredictingFastSymmetryFloat>0.:

				#debug
				'''
				self.debug(
					[
						'We build a symmetry fast connectivity',
						('self.',self,[
								'PredictingFastSymmetryFloat',
								'PredictedDecoderFloatsArray'
							])
					]
				)
				'''

				#diag
				self.PredictedFastFloatsArray=-self.PredictingFastSymmetryFloat*np.dot(
					self.PredictedDecoderFloatsArray.T,
					self.PredictedDecoderFloatsArray
				)

			else:

				#debug
				'''
				self.debug(
					[
						'PredictingFastSymmetryFloat is null'
					]
				)
				'''

				#pinv
				self.PredictedDecoderFloatsArray=self.PredictingRateCostVariable*np.linalg.pinv(
					self.PredictedDecoderFloatsArray.T
				)

			#debug
			'''
			self.debug(
				[
					'Look if we have to perturb',
					'self.PredictingFastPerturbStdFloat is ',
					str(self.PredictingFastPerturbStdFloat)
				]
			)
			'''

			#Check
			if self.PredictingFastPerturbStdFloat>0.:

				#debug
				'''
				self.debug(
					[
						'before setting the perturb fast matrix',
						('self.',self,[
								'NumscipyingMeanFloat',
								'NumscipyingStdFloat'
							])
					]
				)
				'''

				#numscipy
				self.NumscipyingMeanFloat=0.
				self.NumscipyingStdFloat=self.PredictingFastPerturbStdFloat/np.sqrt(self.PredictingAgentUnitsInt)
				self.NumscipyingSizeTuple=(self.PredictingAgentUnitsInt,self.PredictingAgentUnitsInt)
				self.numscipy()

				#debug
				'''
				self.debug(
					[
						'We are going to add this perturbation to fast',
						('self.',self,[
								'NumscipiedValueFloatsArray',
								'PredictedFastFloatsArray'
							])
					]
				)
				'''

				#link
				self.PredictedFastFloatsArray+=self.NumscipiedValueFloatsArray

		#debug
		'''
		self.debug(
			[
				'We have builded the fast connections',
				('self.',self,[
						'PredictedFastFloatsArray'
					])
			]
		)
		'''

		#/################/#
		# Build the Thresholds
		#

		#Check
		if self.PredictingInteractionStr=="Spike":

			#Compute
			#self.PredictedThresholdFloatsArray=np.sum(
			#	(self.PredictedDecoderFloatsArray**2)/2.,axis=0
			#)

		
			#set
			self.PredictedThresholdFloatsArray=np.array(
				[
					sum(
						self.PredictedDecoderFloatsArray[:,__IndexInt]**2
					)/2. for __IndexInt in xrange(self.PredictingAgentUnitsInt)
				]
			)

			#debug
			'''
			self.debug(
				[
					'We have setted the thresholds',
					('self.',self,[
							'PredictedDecoderFloatsArray',
							'PredictedThresholdFloatsArray'
						])
				]
			)
			'''

		#/################/#
		# PredictingDynamicBool Case
		#

		#debug
		self.debug(
			[
				"Do we have to build a dynamic slow connection",
				('self.',self,['PredictingDynamicBool'])
			]
		)

		#Check
		if self.PredictingDynamicBool:

			#/################/#
			# Build the Slow Connection
			#

			#debug
			self.debug(
				[
					'We build the PredictedSlowFloatsArray',
					'CAREFUL PredictingDecoderTimeFloat has to be in ms',
					('self.',self,[
						'PredictedSensorJacobianFloatsArray',
						'PredictingDecoderTimeFloat'
						]),
					'AND ALSO here Slow is D.T(A+lambdaI) just (not D.T(A+lambdaI)D)'
				]
			)

			#diag
			PredictedRightSlowFloatsArray=1000.*self.PredictedSensorJacobianFloatsArray+(
				1./(0.001*self.PredictingDecoderTimeFloat)
				#1.
			)*np.diag(
				np.ones(
					self.PredictingSensorUnitsInt
				)
			)

			#debug
			self.debug(
				[
					'PredictedRightSlowFloatsArray is '+str(PredictedRightSlowFloatsArray),
					('self.',self,[
							'PredictedSensorJacobianFloatsArray',
							'PredictingDecoderTimeFloat'
						])
				]
			)

			#Check 
			if (PredictedRightSlowFloatsArray==0.).all():

				#debug
				'''
				self.debug(
					[
						'Actually the slow is a null matrix'
					]
				)
				'''

				#Check
				if self.PredictingSlowPerturbStdFloat==0.:

					#set
					self.PredictedSlowBool=False

			else:

				#debug
				self.debug(
					[
						'In intermediate values',
						'PredictedRightSlowFloatsArray is '+str(PredictedRightSlowFloatsArray)
					]
				)

				#link
				self.PredictedSlowFloatsArray = np.dot(
					self.PredictedDecoderFloatsArray.T,
					PredictedRightSlowFloatsArray
				)

				#debug
				self.debug(
					[
						'We have built the slow connection',
						('self.',self,[
								'PredictedSlowFloatsArray',
								#'PredictedSensorJacobianFloatsArray',
								#'PredictingDecoderTimeFloat',
								#'PredictedDecoderFloatsArray'
							])
					]
				)

				#renormalize in s
				#self.PredictedSlowFloatsArray = 0.001 * self.PredictedSlowFloatsArray
 

			#/################/#
			# Perturb maybe
			#

			#Check
			if self.PredictingSlowPerturbStdFloat>0.:

				#set
				self.PredictedSlowBool=True

				#numscipy
				self.NumscipyingStdFloat=self.PredictingSlowPerturbStdFloat
				self.NumscipyingSizeTuple=(
					self.PredictingAgentUnitsInt,
					self.PredictingSensorUnitsInt
				)
				self.numscipy()

				#debug
				'''
				self.debug(
					[
						'We are going to add this perturbation to fast',
						('self.',self,[
								'NumscipiedValueFloatsArray',
								'PredictedSlowFloatsArray'
							])
					]
				)
				'''

				#link
				if type(self.PredictedSlowFloatsArray)==None.__class__:
	
					#alias
					self.PredictedSlowFloatsArray=self.NumscipiedValueFloatsArray

				else:

					#add
					self.PredictedSlowFloatsArray+=self.NumscipiedValueFloatsArray

		else:

			#set
			self.PredictedSlowBool=False

		#/###############/#
		# Renormalize compared to the rate model time constant
		#

		#Check
		if self.PredictingInteractionStr=="Rate":

			#debug
			'''
			self.debug(
				[
					'As we divide by a rate time constant of 10ms in the agent',
					'We need here to multiply by 10 the connectivity',
					('self.',self,[
							'PredictingAgentTimeFloat'
						])
				]
			)
			'''

			#set
			self.PredictedFastFloatsArray = self.PredictingAgentTimeFloat*self.PredictedFastFloatsArray
			#self.PredictedFastFloatsArray = self.PredictingAgentTimeFloat*self.PredictedFastFloatsArray

		#Check
		if type(self.PredictedSlowFloatsArray) != None.__class__:

			#mul
			self.PredictedSlowFloatsArray = self.PredictingAgentTimeFloat*self.PredictedSlowFloatsArray

		#/###############/#
		# Consider the sum of Antileak
		#

		#Check
		if self.PredictingRateTransferVariable!=None:

			#debug
			'''
			self.debug(
				[
					'There is a rate transfer function so add the leak term into the fast',
					('self.',self,[
							'PredictedFastFloatsArray'
						])
				]
			)
			'''
			
			#set
			self.PredictedFastFloatsArray+=np.diag(
				np.ones(
					self.PredictingAgentUnitsInt
				)
			)

		#/################/#
		# Build a delay matrice ?
		# 

		#Check
		if self.PredictingDelayFloat>0.:

			#set
			self.PredictedDelayFloatsArray=self.PredictedNetworkDerivePredicterVariable.PredictingDelayFloat*np.ones(
				(
					self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt,
					self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt
				)
			)

			#remove diag
			self.PredictedDelayFloatsArray -= np.diag(
				np.diagonal(
					self.PredictedDelayFloatsArray
					)
				)

			#debug
			'''
			self.debug(
				[
					'We add some delay',
					('self.',self,[
							'PredictedDelayFloatsArray'
						]),
					'but not on the autapses'
				]
			)
			'''

		#/###############/#
		# Look if we can compute the stationary values
		#

		#Check
		if self.PredictingStationaryBool:

			#debug
			'''
			self.debug(
				[
					'We check the stationary points',
					('self.',self,[
							'PredictedDecoderFloatsArray'
						])
				]
			)
			'''

			#try:

			#get
			self.PredictedDecoderInverseFloatsArray=np.linalg.inv(
				self.PredictedDecoderFloatsArray
			)

			#except:

			#	#debug
			#	self.debug(
			#		[
			#			'We could not compute the inverse of the decoder matrix'
			#		]
			#	)

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'PredictedDecoderInverseFloatsArray'
						]
					)
				]
			)	
			'''

	def predictPopulation(self):

		#debug
		'''
		self.debug(
			[
				'We predict Population here'
			]
		)
		'''

		#Check
		if self.ManagementTagStr=="Sensor":

			#debug
			'''
			self.debug(
				[
					'We predict in the Sensor',
					('self.',self,[
							'PredictingDecoderTimeFloat'
						])
				]
			)
			'''

			#/####################/#
			# Simplify the leak equation
			#

			#set
			self.LeakingTimeVariable='#scalar:1.*ms'

			#set
			self.LeakingWeightVariable='0'

			#/####################/#
			# Determine the relations
			#

			#set
			self.PredictedAgentDerivePredicterVariable=self.ParentDeriveTeamerVariable.ManagementDict['Agent']

			#set
			self.PredictedNetworkDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#/####################/#
			# Determine the number of leaking units
			#

			#debug
			'''
			self.debug(
				[
					'Look for LeakingUnitsInt',
					('self.',self,[
							'LeakingUnitsInt',
							'PredictingSensorUnitsInt'
						])
				]
			)
			'''

			#set default
			if self.LeakingUnitsInt==0:
				self.LeakingUnitsInt=1

			#set
			if self.PredictedNetworkDerivePredicterVariable.PredictingSensorUnitsInt>-1:

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingDecoderSparseFloat==0.:
					self.LeakingUnitsInt=self.PredictedNetworkDerivePredicterVariable.PredictingSensorUnitsInt

			#debug
			self.debug(
				[
					('self.',self,[
							'LeakingUnitsInt'
						])

				]
			)

			#/####################/#
			# Set the record
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDecoderRecordVariable !=None:

				#set
				self.RecordingLabelVariable = self.PredictedNetworkDerivePredicterVariable.PredictingDecoderRecordVariable

			#/###################/#
			# Check for Inputs in the Sensor
			#

			#get
			PredictedInputsDeriveManager=self.getTeamer(
				"Inputs"
			)

			#/###################/#
			# Specify the Command Input in the Sensor
			#

			#get
			PredictedCommandDerivePredicter=PredictedInputsDeriveManager.getManager(
				"Command"
			)

			#/###################/#
			# Check for Interactions in the Sensor
			#

			#get
			PredictedInteractionsDerivePredicter=self.getTeamer(
				"Interactions"
			)

			#/###################/#
			# Specify the Jacobian Interaction in the Sensor
			#	

			#get
			PredictedJacobianDerivePredicter=PredictedInteractionsDerivePredicter.getManager(
				"Jacobian"
			)

			#/###################/#
			# Specify the Sensor to Agent interaction
			#

			#get
			PredictedEncoderDerivePredicter=PredictedInteractionsDerivePredicter.getManager(
				"Encod"
			)

			#debug
			'''
			self.debug(
				[
					'It is a rate sensor to agent interaction'
					'We have defined the Encoder interaction in the Sensor'
				]
			)
			'''

		elif self.ManagementTagStr=="Agent":

			#debug
			'''
			self.debug(
				[
					'We predict in the Agent',
					('self.',self,[
							'PredictingDecoderVariable',
							'LeakingUnitsInt',
							'PredictedSensorDerivePredicterVariable'
						])
				]
			)
			'''

			#/####################/#
			# Find the Sensor Population
			#

			#set
			self.PredictedSensorDerivePredicterVariable=self.ParentDeriveTeamerVariable.ManagementDict["Sensor"]

			#set
			self.PredictedNetworkDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#/####################/#
			# Set the TransferVariable
			#

			#debug
			'''
			self.debug(
				[
					'set the LeakingTransferVariable'
				]
			)
			'''

			#set
			self.LeakingTransferVariable=self.PredictedNetworkDerivePredicterVariable.PredictingRateTransferVariable
										
			#debug
			'''
			self.debug(
				[
					'self.PredictedNetworkDerivePredicterVariable.PredictingRateCostVariable is ',
					str(
						self.PredictedNetworkDerivePredicterVariable.PredictingRateCostVariable
					),
					'Determine the interaction',
					'self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr is ',
					self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr
				]
			)
			'''

			#/####################/#
			# Set label to record
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingAgentRecordVariable!=None:

				#set
				self.RecordingLabelVariable = self.PredictedNetworkDerivePredicterVariable.PredictingAgentRecordVariable

			#/####################/#
			# Set the time constant
			#

			#set
			self.LeakingInteractionStr=self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr

			#/####################/#
			# LeakingUnitsInt
			#

			#debug
			'''
			self.debug(
				[
					'Look for LeakingUnitsInt',
					('self.',self,[
							'LeakingUnitsInt'
						]),
					'self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt)
				]
			)
			'''

			#set default
			if self.LeakingUnitsInt==0:
				self.LeakingUnitsInt=1

			#set
			if self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt>-1:
				self.LeakingUnitsInt=self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt

			#/####################/#
			# Spike case 
			#

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'LeakingInteractionStr'
						])
				]
			)
			'''

			#Check
			if self.LeakingInteractionStr == "Spike":
				
				#/####################/#
				# Add a refractory period
				#

				if type(
					self.PredictedNetworkDerivePredicterVariable.PredictingAgentRefractoryVariable
				) != None.__class__ :

					#set
					self.LeakingRefractoryVariable = self.PredictedNetworkDerivePredicterVariable.PredictingAgentRefractoryVariable

				#/####################/#
				# Add noise
				#

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingAgentNoiseVariable!=None:

					#set
					self.LeakingNoiseStdVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentNoiseVariable

				#/####################/#
				# Add a rest input
				#

				#debug
				'''
				self.debug(
					[
						"It is a spike model, we add a neuron like rest",
						"self.PredictedNetworkDerivePredicterVariable.PredictingAgentRestVariable is "+str(
							self.PredictedNetworkDerivePredicterVariable.PredictingAgentRestVariable)
					]
				)
				'''

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingAgentRestVariable!=None:
					
					#get
					PredictedRestVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentRestVariable
				
				else:

					#default
					#PredictedRestVariable=-0.06
					PredictedRestVariable=-60.

				#debug
				'''
				self.debug(
					[
						'PredictedRestVariable is '+str(PredictedRestVariable)
					]
				)
				'''

				#alias
				self.getTeamer(
					"Inputs"
				).getManager(
					"Rest"
				).setAttr(
					"LeakingWeightVariable",
					PredictedRestVariable
				)

				#/####################/#
				# Add a reset if units >1
				#

				#debug
				'''
				self.debug(
					[
						'do we have to add a reset',
						('self.',self,['LeakingUnitsInt'])
					]
				)
				'''

				#Check
				#if self.LeakingUnitsInt>1 and self.PredictedNetworkDerivePredicterVariable.PredictingAgentResetVariable:
				if self.PredictedNetworkDerivePredicterVariable.PredictingAgentResetVariable:

					#Check
					self.LeakingResetVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentResetVariable
					

				#debug
				'''
				self.debug(
					[
						'The agents are IF models',
						('self.',self,[
								'LeakingThresholdVariable'
							])
					]
				)
				'''

				#/####################/#
				# Set a threshold
				#

				#Check
				if type(
					self.PredictedNetworkDerivePredicterVariable.PredictingAgentThresholdVariable
				) ==  None.__class__:

					#alias
					self.LeakingThresholdVariable = PredictedRestVariable+self.PredictedNetworkDerivePredicterVariable.PredictedThresholdFloatsArray

				else:

					#alias
					self.LeakingThresholdVariable = self.PredictedNetworkDerivePredicterVariable.PredictingAgentThresholdVariable


				#debug
				'''
				self.debug(
					[
						'We have setted the LeakingThresholdVariable',
						('self.',self,[
								'LeakingThresholdVariable'
							]),
						'PredictedRestVariable is',
						str(PredictedRestVariable),
						'self.PredictedNetworkDerivePredicterVariable.PredictedThresholdFloatsArray is ',
						str(self.PredictedNetworkDerivePredicterVariable.PredictedThresholdFloatsArray)
					]
				)
				'''

				#/####################/#
				# Look for events to record
				#

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingSpikeRecordVariable!=None:

					#get
					self.getTeamer(
						'Events'
					).getManager(
						'Default_Events'
					).setAttr(
						'BrianingEventSelectVariable',
						self.PredictedNetworkDerivePredicterVariable.PredictingSpikeRecordVariable
					)
	
			else:

				#debug
				'''
				self.debug(
					[
						'The agents are rate models',
						'In the Agent, we set a time constant that is 10ms'
					]
				)
				'''

				pass

			#debug
			'''
			self.debug(
				[
					'self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat)
				]
			)
			'''

			#set
			self.LeakingTimeVariable='#scalar:'+str(
				self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat
			)+'*ms'

			#/###################/#
			# Check for Interactions in the Agent
			#

			#get
			PredictedInteractionsDerivePredicter=self.getTeamer(
				"Interactions"
			)

			#/###################/#
			# Specify the Fast interaction
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingFastSymmetryFloat>0.:	

				#get
				LeakedFastDerivePredicter=PredictedInteractionsDerivePredicter.getManager(
					"Fast"
				)

				#set the connect target
				LeakedFastDerivePredicter.ConnectingKeyVariable=self

				#debug
				'''
				self.debug(
					[
						'We have defined the Fast interaction in the Agent',
						'Look maybe for slow',
						'self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool is ',
						str(self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool)
					]
				)
				'''


			#/###################/#
			# Specify the Decoder interaction
			#

			#get
			LeakedDecodDerivePredicter=PredictedInteractionsDerivePredicter.getManager("Decod")

			#set the connect target
			LeakedDecodDerivePredicter.ConnectingKeyVariable=self.ParentDeriveTeamerVariable.ManagementDict[
				"Decoder"
			]

			#/###################/#
			# Rate Case
			#

			#Check
			if self.LeakingInteractionStr=="Rate":

				#debug
				'''
				self.debug(
					[
						'PredictingDynamicBool is False',
						"self.LeakingInteractionStr=='Rate' ",
						'So set a direct interaction'
					]
				)
				'''
				
				#/####################/#
				# Transfer function Case
				#

				#Check
				if self.LeakingTransferVariable!=None:

					#debug
					'''
					self.debug(
						[
							'We are in the rate and there is a transfer function',
							'build the antileak interaction'
						]
					)
					'''

					"""
					#/###################/#
					# Specify the Antileak interaction
					#

					#Check
					if "Antileak" in PredictedInteractionsDerivePredicter.ManagementDict:

						#get
						LeakedAntileakDerivePredicter=PredictedInteractionsDerivePredicter.ManagementDict[
							"Antileak"
						]

					else:

						#manage
						LeakedAntileakDerivePredicter=PredictedInteractionsDerivePredicter.manage(
							"Antileak"
						).ManagedValueVariable

					#set the connect target
					LeakedAntileakDerivePredicter.ConnectingKeyVariable=self

					#debug
					'''
					self.debug(
						[
							"We have defined the Antileak interaction in the Agent"
						]
					)
					'''
					"""

				else:

					#Check
					if self.PredictedNetworkDerivePredicterVariable.PredictingRateCostVariable==None:

						#debug
						'''
						self.debug(
							[
								"There is no transfer function neither rate cost ",
								"so put the leak term to null"
							]
						)
						'''

						#set
						self.LeakingWeightVariable='0'

					else:

						#debug
						'''
						self.debug(
							[
								"There is no transfer function neither rate cost ",
								"so put the leak term to null"
							]
						)
						'''

						#set
						self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingRateCostVariable

			"""
			#/###################/#
			# Specify the J_EncodI_Command' 
			#

			#get
			self.getTeamer(
					"Traces"
				).getManager(
					"J_EncodI_Command"
				).getTeamer(
					"Samples"
				).getManager(
					"Default"
				)
			"""

		#Check
		elif self.ManagementTagStr=="Decoder":

			#debug
			'''
			self.debug(
				[
					'We predict in the Decoder',
					('self.',self,[
							'PredictingDecoderTimeFloat'
						])
				]
			)
			'''

			#/####################/#
			# Determine the parent
			#

			#set
			self.PredictedAgentDerivePredicterVariable=self.ParentDeriveTeamerVariable.ManagementDict["Agent"]

			#set
			self.PredictedSensorDerivePredicterVariable=self.ParentDeriveTeamerVariable.ManagementDict["Sensor"]

			#set
			self.PredictedNetworkDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#/####################/#
			# Determine if we have to compute the stats
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDecoderSparseFloat>0.:

				#debug
				'''
				self.debug(
					[
						'We are going to compute the stats in the decoder'
					]
				)	
				'''

				#Check
				self.LeakingTotalBool=True

			#/####################/#
			# Determine the number of leaking units
			#

			#debug
			'''
			self.debug(
				[
					'Look for LeakingUnitsInt',
					('self.',self,[
							'LeakingUnitsInt',
							'PredictingSensorUnitsInt'
						])
				]
			)
			'''

			#set default
			if self.LeakingUnitsInt==0:
				self.LeakingUnitsInt=1

			#set
			if self.PredictedNetworkDerivePredicterVariable.PredictingSensorUnitsInt>-1:
				self.LeakingUnitsInt=self.PredictedNetworkDerivePredicterVariable.PredictingSensorUnitsInt


			#/####################/#
			# Set the record
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDecoderRecordVariable !=None:

				#set
				self.RecordingLabelVariable = self.PredictedNetworkDerivePredicterVariable.PredictingDecoderRecordVariable

			#/####################/#
			# The Decoder
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool==False:

				#debug
				'''
				self.debug(
					[
						'self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool is False',
						'set LeakingTimeVariable to 0'
					]
				)
				'''

				#set
				self.LeakingTimeVariable=0.

			else:

				#set
				self.LeakingTimeVariable = self.PredictingDecoderTimeFloat


			#/###################/#
			# PredictingDynamicBool
			#

			#debug
			'''
			self.debug(
				[
					'Look if we have to add slow connection from decoder to agents',
					('self.',self,[

						]),
					'self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool is '+str(
						self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool
					),
					'self.PredictedNetworkDerivePredicterVariable.PredictedSlowBool is '+str(
						self.PredictedNetworkDerivePredicterVariable.PredictedSlowBool
						)
				]
			)
			'''

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool and self.PredictedNetworkDerivePredicterVariable.PredictedSlowBool:

				#debug
				'''
				self.debug(
					[
						'PredictingDynamicBool is true'
					]
				)
				'''

				#/###################/#
				# Specify the Slow interaction
				#

				#get
				LeakedSlowDerivePredicter=self.getTeamer(
						"Interactions"
					).getManager(
						"Slow"
					)

				#debug
				'''
				self.debug(
					[
						'We have defined the Decod interaction in the Agent'
					]
				)
				'''

				#set the connect target
				LeakedSlowDerivePredicter.ConnectingKeyVariable=self.ParentDeriveTeamerVariable.ManagementDict[
					"Agent"
				]

			else:

				#Check
				if "Interactions" in self.TeamDict:

					#delete
					del self.TeamDict[
							"Interactions"
						]

					"""
					#delete
					del self.getTeamer(
							"Interactions"
						).ManagementDict[
							"Slow"
						]
					"""


			
	def predictInput(self):

		#Check
		if self.ManagementTagStr=='Command':
			
			#/####################/#
			# Determine the parent
			#

			#set
			self.PredictedAgentDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.PredictedNetworkDerivePredicterVariable=self.PredictedAgentDerivePredicterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#/####################/#
			# Determine the LeakingWeightVariable
			#
	
			#debug
			'''
			self.debug(
				[
					"self.PredictedNetworkDerivePredicterVariable.PredictingCommandVariable is "+str(
						self.PredictedNetworkDerivePredicterVariable.PredictingCommandVariable)
				]
			)
			'''
			
			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingCommandVariable!=None:

				#set
				self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingCommandVariable
	
			else:

				#set
				self.LeakingWeightVariable="#custom:#clock:200*ms:5.*mV*int(t==200*ms)"


			#debug
			'''
			self.debug(
				[
					'We set here the Command dynamic',
					('self.',self,[
							'LeakingWeightVariable'
						])
				]
			)
			'''

	def predictInteraction(self):

		#Check
		if self.ManagementTagStr=="Jacobian":

			#debug
			'''
			self.debug(
				[
					'We predict in the Jacobian',
					('self.',self,[
							'PredictingDynamicDict'
						])
				]
			)
			'''

			#/################/#
			# Determine the relations
			#

			#set
			self.PredictedSensorDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.PredictedAgentDerivePredicterVariable=self.PredictedSensorDerivePredicterVariable.ParentDeriveTeamerVariable.ManagementDict[
				"Agent"
			]

			#set
			self.PredictedNetworkDerivePredicterVariable=self.PredictedSensorDerivePredicterVariable.PredictedNetworkDerivePredicterVariable

			#set
			self.ConnectingKeyVariable=self.PredictedSensorDerivePredicterVariable

			#debug
			'''
			self.debug(
				[
					'We have determined the relations for predictInteraction',
					('self.',self,[
						'ConnectingKeyVariable'
					])
				]
			)
			'''

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDecoderSparseFloat>0.:

				#link
				self.LeakingWeightVariable=[
					[
					self.PredictedNetworkDerivePredicterVariable.PredictedSensorJacobianFloatsArray[0,0]
					]
				]

			else:

				#link
				self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictedSensorJacobianFloatsArray

			#debug
			'''
			self.debug(
				[
					"the weights in the sensors",
					('self.',self,['LeakingWeightVariable'])
				]
			)
			'''

		#Check
		elif self.ManagementTagStr=="Encod":

			#debug
			'''
			self.debug(
				[
					'We predict in the Encod interaction',
					('self.',self,[
						])
				]
			)
			'''

			#/################/#
			# Determine the relations
			#

			#set
			self.PredictedSensorDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.PredictedAgentDerivePredicterVariable=self.PredictedSensorDerivePredicterVariable.ParentDeriveTeamerVariable.ManagementDict["Agent"]

			#set
			self.PredictedNetworkDerivePredicterVariable=self.PredictedSensorDerivePredicterVariable.PredictedNetworkDerivePredicterVariable
	
			#set
			self.ConnectingKeyVariable=self.PredictedAgentDerivePredicterVariable

			#/################/#
			# Build the variable in the sensor to be the input in the Agent
			#

			#debug
			'''
			self.debug(
				[
					'Is it Rate : put x as post',
					'Is it Spike : put c as post',
					"self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool is ",
					self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool
				]
			)
			'''

			#set
			self.LeakingInteractionStr='Rate'

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool:

				#debug
				'''
				self.debug(
					[
						'There is a dynamic to transfer',
						'so we bind c instead of x'
					]
				)
				'''

				#set
				self.LeakingVariableStr='I_Command'

			#/################/#
			# Build the LeakingWeightVariable
			#

			#debug
			'''
			self.debug(
				[
					'We set the weights in the Encod',
					'self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray is ',
					str(
						self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray
					),
					'but dont forget to also multiply by the agent time constant',
					('self.',self,[

					])
				]
			)
			'''
				
			#type
			PredictedEncodType=type(self.PredictedNetworkDerivePredicterVariable.PredictingEncodWeightVariable)


			#link
			#self.LeakingWeightVariable=0.001*self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray.T
			
			if self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool==False:

				#/###############/#
				# This is directly the x
				#

				#Check
				if PredictedEncodType == None.__class__:

					#set
					self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray.T
					#self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray.T
			
				else:

					#set
					self.LeakingWeightVariable = self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictingEncodWeightVariable

			else:



				#/###############/#
				# This is the c
				#

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr == "Rate":
				
					#Check
					if PredictedEncodType == None.__class__:

						#set
						self.LeakingWeightVariable=1000.*self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray.T
						#self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray.T

					else:

						#set
						self.LeakingWeightVariable = 1000.*self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictingEncodWeightVariable


				else:

					#Check
					if PredictedEncodType == None.__class__:

						#set
						self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray.T
			
					else:

						#set
						self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictingAgentTimeFloat*self.PredictedNetworkDerivePredicterVariable.PredictingEncodWeightVariable
			

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingDecoderSparseFloat>0.:

					#set
					self.LeakingWeightVariable=[[self.LeakingWeightVariable[0]]]

			#self.LeakingWeightVariable=0.

			#/################/#
			# Look for perturb
			#

			#debug
			'''
			self.debug(
				[
					'Look if we have to perturb',
					'self.PredictedNetworkDerivePredicterVariable.PredictingEncodPerturbStdFloat is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictingEncodPerturbStdFloat)
				]
			)
			'''

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingEncodPerturbStdFloat>0.:

				#numscipy
				self.NumscipyingStdFloat=self.PredictedNetworkDerivePredicterVariable.PredictingEncodPerturbStdFloat
				self.NumscipyingRowsInt=self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt
				self.NumscipyingColsInt=self.PredictedNetworkDerivePredicterVariable.PredictingSensorUnitsInt
				self.numscipy()

				#link
				self.LeakingWeightVariable+=self.NumscipiedValueFloatsArray
				
			#debug
			'''
			self.debug(
				[
					"In the end for the encod input",
					('self.',self,[
							'LeakingWeightVariable'
						])
				]
			)	
			'''

			#/################/#
			# Say that we want to record it
			#

			#Check
			#if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr=="Spike":
				
			#set
			self.LeakingRecordBool=True

		elif self.ManagementTagStr=="Decod":

			#debug
			'''
			self.debug(
				[
					'We predict in the Decod interaction',
					('self.',self,[
						])
				]
			)
			'''

			#/################/#
			# Determine the relations
			#

			#set
			self.PredictedAgentDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.PredictedDecoderDerivePredicterVariable=self.PredictedAgentDerivePredicterVariable.ParentDeriveTeamerVariable.ManagementDict["Decoder"]

			#set
			self.PredictedNetworkDerivePredicterVariable=self.PredictedAgentDerivePredicterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.ConnectingKeyVariable=self.PredictedDecoderDerivePredicterVariable

			#/####################/#
			# Determine the interaction
			#

			#link
			self.LeakingInteractionStr=self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr

			#/################/#
			# Build the LeakingWeightVariable
			#

			#debug
			'''
			self.debug(
				[
					'We set the weights in the Decod',
					'self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray)
				]
			)
			'''

			if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr=="Rate":

				#set
				self.LeakingWeightVariable = 1.*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray

			else:

				#set
				self.LeakingWeightVariable = 1.*self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray


			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool:

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr=="Rate":

					#debug
					'''
					self.debug(
						[
							'We have to rescale with the time constant of the decoder',
							"self.PredictedNetworkDerivePredicterVariable.PredictingDecoderTimeFloat is ",
							str(self.PredictedNetworkDerivePredicterVariable.PredictingDecoderTimeFloat)
						]
					)
					'''

					#set
					self.LeakingWeightVariable = (
						0.001*self.PredictedNetworkDerivePredicterVariable.PredictingDecoderTimeFloat
					)*self.LeakingWeightVariable

				else:

					#set
					#self.LeakingWeightVariable = 0.001*self.LeakingWeightVariable
					#self.LeakingWeightVariable = self.PredictedNetworkDerivePredicterVariable.PredictingDecoderTimeFloat*self.LeakingWeightVariable
					self.LeakingWeightVariable = self.LeakingWeightVariable

			#debug
			'''
			self.debug(
				[
					'In the end ',
					('self.',self,[
							'LeakingWeightVariable'
						]),
					'self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictedDecoderFloatsArray)
				]
			)
			'''

		elif self.ManagementTagStr=="Fast":

			#debug
			'''
			self.debug(
				[
					'We predict in the Fast interaction',
					('self.',self,[
						])
				]
			)
			'''

			#/################/#
			# Determine the relations
			#

			#set
			self.PredictedAgentDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.PredictedNetworkDerivePredicterVariable=self.PredictedAgentDerivePredicterVariable.PredictedNetworkDerivePredicterVariable
	
			#/################/#
			# Determine the interactions
			#

			#link
			self.LeakingInteractionStr=self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr

			#/################/#
			# Build the LeakingWeightVariable
			#

			#debug
			'''
			self.debug(
				[
					'We set the weights in the Fast',
					'self.PredictedNetworkDerivePredicterVariable.PredictedFastFloatsArray is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictedFastFloatsArray)
				]
			)
			'''

			#link
			self.LeakingWeightVariable=self.PredictedNetworkDerivePredicterVariable.PredictedFastFloatsArray

			#/################/#
			# Consider maybe delay
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDelayFloat!=0.:
				
				#set
				self.LeakingDelayVariable=self.PredictedNetworkDerivePredicterVariable.PredictedDelayFloatsArray

			#/################/#
			# Consider if we need to record J
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingFastPlasticBool:

				#set
				self.RecordingLabelVariable=range(
					min(
						self.PredictedNetworkDerivePredicterVariable.PredictingAgentUnitsInt**2,
						4
					)
				)


		elif self.ManagementTagStr=="Slow":

			#debug
			'''
			self.debug(
				[
					'We predict in the Slow interaction',
					('self.',self,[
						])
				]
			)
			'''

			#/################/#
			# Determine the relations
			#

			#set
			self.PredictedAgentDerivePredicterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#set
			self.PredictedSensorDerivePredicterVariable=self.PredictedAgentDerivePredicterVariable.ParentDeriveTeamerVariable["Sensor"]

			#set
			self.PredictedNetworkDerivePredicterVariable=self.PredictedAgentDerivePredicterVariable.PredictedNetworkDerivePredicterVariable
	
			#/################/#
			# Build the LeakingWeightVariable
			#

			#debug
			self.debug(
				[
					'We set the weights in the Slow',
					'self.PredictedNetworkDerivePredicterVariable.PredictedSlowFloatsArray is ',
					str(self.PredictedNetworkDerivePredicterVariable.PredictedSlowFloatsArray),
					('self.',self,['LeakingWeightVariable']),
					"self.PredictedNetworkDerivePredicterVariable.LeakingInteractionStr is "+str(
						self.PredictedNetworkDerivePredicterVariable.LeakingInteractionStr)
				]
			)

			#Check
			if type(self.LeakingWeightVariable) == None.__class__:

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr == "Spike":

					#link
					self.LeakingWeightVariable = 0.001 * self.PredictedNetworkDerivePredicterVariable.PredictedSlowFloatsArray

				else:

					#link
					self.LeakingWeightVariable = 1. * self.PredictedNetworkDerivePredicterVariable.PredictedSlowFloatsArray


			#debug
			self.debug(
				[
					'In the end slow is ',
					('self.',self,[
							'LeakingWeightVariable'
						])
				]
			)

	#/######################/#
	# Augment leak
	#

	def leakPopulation(self):

		#Call the base method
		BaseClass.leakPopulation(self)

		#Check
		if self.ManagementTagStr=="Sensor":

			#/##################/#
			# Is there a stationary point r0 to compute
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingStationaryBool:

				#debug
				'''
				self.debug(
					[
						'We compute a global stationary rate variable',
						('self.',self,[
								'LeakedModelStr'
							])
					]
				)
				'''

				#add
				self.LeakedModelStr='r0 : '+self.LeakedDimensionStr+'\n'+self.LeakedModelStr

				#debug
				self.debug(
					[
						'In the end',
						('self.',self,[
								'LeakedModelStr'
							])
					]
				)

				#add
				self.BrianingNeurongroupDict['model']=self.LeakedModelStr

				#append
				self.LeakedRecordSkipStrsList.append('r0')

	def leakInput(self):

		#call the base
		BaseClass.leakInput(self)

		#Check
		if self.ManagementTagStr=='Command':

			#/####################/#
			# Remove from record if it is DynamicBool False
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool==False:

				#append
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList=SYS.append(
							self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList,
							self.LeakedSymbolStr
						)

				#debug
				'''
				self.debug(
					[
						'We have removed the I_Command from record and plot',
						'self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList is ',
						str(self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList)
					]
				)
				'''

	def leakInteraction(self):

		#Check
		if self.ManagementTagStr=="Encod":

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingEncodPlasticBool:

				#Check
				if self.LeakingSymbolPrefixStr=="":
					self.LeakingSymbolPrefixStr="J"

				#debug
				'''
				self.debug(
					[
						'We make the encod synapses plastic'
					]
				)
				'''

				#set
				LeakedPlasticStr=""

				#Check
				if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr=="Rate":
					
					#debug
					'''
					self.debug(
						[
							'It is a rate model',
							('self.',self,[
									'LeakedSymbolStr',
									'LeakingSymbolStr',
									'BrianingSynapsesDict'
								])
						]
					)
					'''

					#set
					self.LeakingPlasticRuleVariable='beta : 1'
					self.LeakingPlasticRuleVariable+='\nlambda : 1'
					self.LeakingPlasticRuleVariable+='\nd'+self.LeakingSymbolPrefixStr+'/dt=beta*('
					self.LeakingPlasticRuleVariable+='I_Command_post-lambda*'+self.LeakingSymbolPrefixStr+')'	

					#debug
					'''
					self.debug(
						[
							'after update of the model',
							('self.',self,[
									'LeakingPlasticRuleVariable'
								])
						]
					)
					'''

				else:

					#debug
					'''
					self.debug(
						[
							'It is a spike model',
							('self.',self,[
									'LeakedSymbolStr',
									'LeakingSymbolStr',
								])
						]
					)
					'''

					#set
					LeakedPlasticStr+='\n'+self.LeakingSymbolPrefixStr+'+=0.*('+self.PredictedDecoderDerivePredicterVariable.LeakedSymbolStr+'_post'
					LeakedPlasticStr+='/mV)-'+self.LeakingSymbolPrefixStr

					#set
					self.LeakingPlasticRuleVariable=LeakedPlasticStr


					#debug
					'''
					self.debug(
						[
							'after update of the model',
							('self.',self,[
									'LeakingPlasticRuleVariable'
								])
						]
					)
					'''

		#Check
		elif self.ManagementTagStr=='Fast':

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingFastPlasticBool:

				#Check
				if self.LeakingSymbolPrefixStr=="":
					self.LeakingSymbolPrefixStr=Leaker.LeakInteractionPrefixStr

				#debug
				self.debug(
					[
						'We make the fast synapses plastic',
						('self.',self,[
								'LeakingInteractionStr',
								'LeakingSymbolPrefixStr'
							])
					]
				)

				#init
				LeakedPlasticStr='('

				#Check
				if self.LeakingInteractionStr=="Rate":
					
					#debug
					'''
					self.debug(
						[
							'It is a rate model',
							('self.',self,[
									'LeakedSymbolStr',
									'LeakingSymbolStr',
								])
						]
					)
					'''

					#set
					self.LeakingPlasticRuleVariable='epsilon : 1'
					self.LeakingPlasticRuleVariable+='\nalpha : 1'
					self.LeakingPlasticRuleVariable+='\nd'+self.LeakingSymbolPrefixStr+'/dt=epsilon*('
					self.LeakingPlasticRuleVariable+='dot(I_Command_post,'+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr+'_post)-alpha*'+self.LeakingSymbolPrefixStr+')'	

					#debug
					'''
					self.debug(
						[
							'after update of the model',
							('self.',self,[
									'LeakingPlasticRuleVariable'
								])
						]
					)
					'''

				else:

					#debug
					self.debug(
						[
							'It is a spike model',
							('self.',self,[
									'LeakedModelStr',
									'LeakedSymbolStr',
									'LeakingSymbolPrefixStr',
									'LeakingThresholdVariable'
								])
						]
					)

					#/################/#
					# We first set the thresholds
					#

					#set
					#self.PredictedAgentDerivePredicterVariable.LeakingThresholdVariable=-50.

					#/################/#
					# Build the plastic rule
					#

					#set
					LeakedPlasticStr+='(('+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr+'_post'
				
					#Check
					if 'Rest' in self.PredictedAgentDerivePredicterVariable.TeamDict[
						'Inputs'
					].ManagementDict:

						#get
						PredictedRestVariable=self.PredictedAgentDerivePredicterVariable.TeamDict[
							'Inputs'
						].ManagementDict[
							'Rest'
						].LeakingWeightVariable


						#debug
						'''
						self.debug(
							[
								'We set a plasticity rule regarding the deviation compared to the rest',
								'PredictedRestVariable is '+str(PredictedRestVariable)
							]
						)
						'''

						#import
						import numpy as np

						#type
						PredictedRestType=type(PredictedRestVariable)

						#Check
						if PredictedRestType in [float,np.float64]:

							#str
							PredictedRestStr=str(
								PredictedRestVariable
							)

							#debug
							self.debug(
								[
									"PredictedRestStr is "+str(PredictedRestStr)
								]
							)

							#Check
							if PredictedRestStr[0]=='-':

								#add
								LeakedPlasticStr+='+'+PredictedRestStr[1:]
						
							else:

								#add
								LeakedPlasticStr+='-'+PredictedRestStr[1:]

							#add
							LeakedPlasticStr+='*mV'

							#add
							LeakedPlasticStr+=')/mV)'

					else:

						#add
						LeakedPlasticStr+=')/mV)'
					
					#add
					LeakedPlasticStr+='+((1.+alpha)/2.)*'+self.LeakingSymbolPrefixStr
					LeakedPlasticStr+=')'
					LeakedPlasticStr+='*int(i!=j)'
					#LeakedPlasticStr+='*int('+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr+'_post>-61*mV)'
					LeakedPlasticStr+='*(int('+self.LeakingSymbolPrefixStr+'>0.1)'
					LeakedPlasticStr+='+int('+self.LeakingSymbolPrefixStr+'<-0.1)'
					LeakedPlasticStr+=')'

					#add
					self.LeakingPlasticRuleVariable=""
					
					#NOT DEBUG
					self.LeakingPlasticRuleVariable+=self.LeakingSymbolPrefixStr+'-='+str(
						self.PredictedNetworkDerivePredicterVariable.PredictingFastLearnRateFloat
					)+'*'+LeakedPlasticStr
					
					#DEBUG
					#self.LeakedModelStr+="\nDeltaJ : 1\n"
					#self.LeakingPlasticRuleVariable+="DeltaJ="+LeakedPlasticStr
					
					#add in the model
					self.LeakedModelStr+="alpha : 1"

					#debug
					'''
					self.debug(
						[
							'after update of the model',
							('self.',self,[
									'LeakingPlasticRuleVariable'
								])
						]
					)
					'''

		#call the base
		BaseClass.leakInteraction(self)


	#/######################/#
	# Augment brian
	#

	def setDebugNeurongroup(self):

		#/################/#
		# Call the base
		# 

		#set
		BaseClass.setDebugNeurongroup(self)

		#Check
		if self.ManagementTagStr=="Decoder":

			#Check
			PrintStr='In the Decod, LeakingWeightVariable is \n'
			LeakingWeightVariable=self.PredictedAgentDerivePredicterVariable.TeamDict["Interactions"
			].ManagementDict["Decod"].LeakingWeightVariable
			PrintStr+=str(LeakingWeightVariable)

			#print
			print PrintStr


	def brianPopulation(self):

		#Call the base
		BaseClass.brianPopulation(self)

		#Check
		if self.ManagementTagStr=='Sensor':

			#/################/#
			# Look for computing stationary variable
			#

			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingStationaryBool:

				#debug
				'''
				self.debug(
					[
						'We compute global statistical variables'
					]
				)
				'''

				#import
				from brian2 import Synapses,StateMonitor

				#set
				LeakedStationarySymbolStr='r0'

				#set
				LeakedStationaryModelStr='D_inv : 1\n'
				LeakedStationaryModelStr+=LeakedStationarySymbolStr+'_post = D_inv*'+self.LeakedSymbolStr+'_pre : '+self.LeakedDimensionStr+' (summed)\n'

				#debug
				self.debug(
					[
						'LeakedStationaryModelStr is ',
						LeakedStationaryModelStr,
						('self.',self,[
								'LeakedModelStr'
							]),
						'self.BrianedNeurongroupVariable.equations._equations.keys() is ',
						str(self.BrianedNeurongroupVariable.equations._equations.keys())
					]
				)

				#init
				self.LeakedStationarySynapsesVariable=Synapses(
					self.BrianedNeurongroupVariable,
					self.BrianedNeurongroupVariable,
					LeakedStationaryModelStr,
					clock=self.BrianedNeurongroupVariable.clock
				)

				#connect
				self.LeakedStationarySynapsesVariable.connect(True)

				#debug
				self.debug(
					[
						('self.',self,[
								'LeakedStationarySynapsesVariable',
								'LeakingUnitsInt'
							])
					]
				)

				#D_inv
				self.LeakedStationarySynapsesVariable.D_inv[
					:
				]=np.reshape(
					self.PredictedNetworkDerivePredicterVariable.PredictedDecoderInverseFloatsArray.T,
					self.LeakingUnitsInt**2
				)

				#init
				self.PredictedStationaryStateMonitorVariable=StateMonitor(
					self.LeakedStationarySynapsesVariable,
					LeakedStationarySymbolStr,
					self.TeamDict[
						'Traces'
					].ManagementDict[
						Recorder.RecordPrefixStr+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr
					].TeamDict[
						'Samples'
					].ManagementDict[
						'Default'
					].RecordingLabelVariable
				)

				#debug
				'''
				self.debug(
					[
						'self.BrianedNeurongroupVariable.N is ',
						str(self.BrianedNeurongroupVariable.N),
						('self.',self,[
							'LeakedGlobalSynapsesVariable',
						])
					]
				)
				'''

				#/##############/#
				# add
				#

				#add
				self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
					self.LeakedStationarySynapsesVariable
				)
				self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
					self.PredictedStationaryStateMonitorVariable
				)

		"""
		#Check
		if self.ManagementTagStr=='Agent':

			#debug
			self.debug(
				[
					"We brian pop predict"
				]
			)

			self.TeamDict[
				'Traces'
			].ManagementDict[
				'J_EncodI_Command'
			].TeamDict[
				'Samples'
			].ManagementDict[
				''
			]
		"""

	def brianTrace(self):

		#/###################/#
		# std
		#

		#debug
		'''
		self.debug(
			[
				'We reduce the size of initial conditions',
				('self.',self,[
						'ManagementTagStr'
					])
			]
		)
		'''

		#set
		self.NumscipyingStdFloat=0.00001

		#/################/#
		# switch case
		#

		#Check
		if self.ManagementTagStr=='U':

			#/###################/#
			# Switch case
			#

			#Check
			if self.LeakedParentPopulationDeriveLeakerVariable.ManagementTagStr=="Sensor":

				#debug
				'''
				self.debug(
					[
						'We set a special label name for the Sensor'
					]
				)
				'''

				#set
				self.BrianingActivityStr="x"

			#Check
			if self.LeakedParentPopulationDeriveLeakerVariable.ManagementTagStr=="Agent":

				#debug
				'''
				self.debug(
					[
						'We set a special label name for the Agent'
					]
				)
				'''

				#Check
				if self.LeakedParentPopulationDeriveLeakerVariable.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr=="Rate":

					#set
					self.BrianingActivityStr="r" 

				else:

					#set
					self.BrianingActivityStr="V"

					"""
					#debug
					'''
					self.debug(
						[
							'We init under the thresholds',
							'self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable is ',
							str(self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable)
						]
					)
					'''

					#set
					self.NumscipyingMeanFloat=100.*(
						self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable.min()-0.5
					)
					"""



			#Check
			elif self.LeakedParentPopulationDeriveLeakerVariable.ManagementTagStr=="Decoder":

				#debug
				'''
				self.debug(
					[
						'We set a special label name for the Decoder'
					]
				)
				'''

				#set
				self.BrianingActivityStr="\hat{x}"

		#Check
		elif self.ManagementTagStr=='I_Command':

			#debug
			'''
			self.debug(
				[
					'We set a special label name for the I_Command'
				]
			)
			'''

			#set
			self.BrianingActivityStr="c"

		#Check
		elif self.ManagementTagStr in ['J_EncodU','J_EncodI_Command']:

			#set
			self.BrianingViewBool=False


		#/################/#
		# brianTrace base
		#

		#debug
		'''
		self.debug(
			[
				'We call the base method',
				str(BaseClass.brianTrace)
			]
		)
		'''

		#call the base
		BaseClass.brianTrace(self)

	"""
	def brianSample(self):

		#base method
		BaseClass.brianSample(self)

		#debug
		'''
		self.debug(
			[
				"We brian sample predict ",
				('self.',self,[
						'ManagementTagStr'
					])
			]
		)
		'''

		#Check
		if self.ManagementTagStr=="J_EncodI_Command":

			#debug
			'''
			self.debug(
				[
					"We brian sample predict J_EncodI_Command here"
				]
			)
			'''
			pass
	"""

	#/######################/#
	# Augment view
	#

	def viewSample(self):

		#debug
		'''
		self.debug(
			[
				'We predict view sample here',
				('self.',self,[
						'StructureTagStr',
						'ManagementTagStr'
					])
			]
		)
		'''

		#base
		BaseClass.viewSample(self)

		#/#################/#
		# Special Agent case
		#

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.ManagementTagStr=="Agent":

			#debug
			'''
			self.debug(
				[
					"self.BrianedParentDeriveRecorderVariable.RecordKeyStr is "+str(self.BrianedParentDeriveRecorderVariable.RecordKeyStr),
					"self.BrianedParentPopulationDeriveBrianerVariable.LeakedSymbolStr is "+str(self.BrianedParentPopulationDeriveBrianerVariable.LeakedSymbolStr)
				]
			)
			'''

			#Check
			if self.BrianedParentDeriveRecorderVariable.RecordKeyStr==self.BrianedParentPopulationDeriveBrianerVariable.LeakedSymbolStr:

			
				#Check
				if self.BrianedParentPopulationDeriveBrianerVariable.PredictedNetworkDerivePredicterVariable.PredictingDynamicBool:

					#debug
					'''
					self.debug(
						[
							"self.BrianedParentPopulationDeriveBrianerVariable.TeamDict['Traces'].ManagementDict.keys() is "+str(
								self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
								'Traces'].ManagementDict.keys())
						]
					)
					'''

					#get
					ViewedTracesDerivePredicter=ViewedCommandDerivePredicter=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
						'Traces'
					]

					#Check
					if 'J_EncodI_Command' in ViewedTracesDerivePredicter:

						#Check
						ViewedCommandDerivePredicter=ViewedTracesDerivePredicter.ManagementDict[
							'J_EncodI_Command'
						].TeamDict[
							'Samples'
						].ManagementDict[
							'Default'
						]

						#debug
						'''
						self.debug(
							[
								'We view Sample Agent here',
								'We add also the view of the command',
								#'ViewedSensorDerivePredicter is ',
								#SYS._str(ViewedSensorDerivePredicter),
								'ViewedCommandDerivePredicter.PyplotingDrawVariable is ',
								SYS._str(ViewedCommandDerivePredicter.PyplotingDrawVariable)
							]
						)
						'''

						#import 
						import copy

						#copy
						ViewedPyplotDrawVariable=copy.deepcopy(
							ViewedCommandDerivePredicter.PyplotingDrawVariable
						)

						#set
						map(
							lambda __ItemTuple:
							__ItemTuple[1][
								'#kwarg'
							].update(
								{
									'linestyle':'--',
									'linewidth':1
								}
							),
							ViewedPyplotDrawVariable
							#self.PyplotingDrawVariable
						)

						#add
						self.PyplotingDrawVariable.extend(
							ViewedPyplotDrawVariable
						)

						#debug
						'''
						self.debug(
							[
								'In the end',
								('self.',self,[
									'PyplotingDrawVariable'
								])
								
							]
						)
						'''

		#/#################/#
		# Special Decoder case
		#

		#Check
		elif self.BrianedParentPopulationDeriveBrianerVariable.ManagementTagStr == "Decoder":

			#
			ViewedSensorDerivePredicter=self.BrianedParentPopulationDeriveBrianerVariable.PredictedSensorDerivePredicterVariable.TeamDict[
				'Traces'
			].ManagementDict[
				'U'
			].TeamDict[
				'Samples'
			].ManagementDict[
				'Default'
			]

			#debug
			'''
			self.debug(
				[
					'We view Sample Decoder here',
					'We add also the view of the sensor',
					#'ViewedSensorDerivePredicter is ',
					#SYS._str(ViewedSensorDerivePredicter),
					'ViewedSensorDerivePredicter.PyplotingDrawVariable is ',
					SYS._str(ViewedSensorDerivePredicter.PyplotingDrawVariable)
				]
			)
			'''
			
			#import 
			import copy

			#copy
			ViewedPyplotDrawVariable=copy.deepcopy(
				ViewedSensorDerivePredicter.PyplotingDrawVariable
			)

			#set
			map(
				lambda __ItemTuple:
				__ItemTuple[1][
					'#kwarg'
				].update(
					{
						'alpha':0.3
					}
				),
				ViewedPyplotDrawVariable
			)

			#set
			map(
				lambda __ItemTuple:
				__ItemTuple[1][
					'#kwarg'
				].update(
					{
						'linestyle':'-',
						'linewidth':1
					}
				),
				self.PyplotingDrawVariable
			)

			#:
			ViewedReversePyplotDrawVariable=ViewedPyplotDrawVariable[:]
			ViewedReversePyplotDrawVariable.reverse()

			#add
			map(
				lambda __Variable:
				self.PyplotingDrawVariable.insert(
					0,
					__Variable
				),
				ViewedReversePyplotDrawVariable
			)

			#debug
			'''
			self.debug(
				[
					'In the end',
					('self.',self,[
						'PyplotingDrawVariable'
					])
					
				]
			)
			'''

		#/################/#
		# Specify the shift
		#

		#set
		self.BrianedParentDeriveRecorderVariable.PyplotingShiftVariable=[2,0]

	#/################/#
	# Augment view
	#

	def viewPopulation(self):

		#/##################/#
		# base method
		#

		#base
		BaseClass.viewPopulation(self)


		#Check
		if self.ManagementTagStr=="Sensor":

			#debug
			'''
			self.debug(
				[
					'We view predict pop here',
					('self.',self,[
							'BrianingViewNetworkBool'
						])
				]
			)
			'''
			
			#init
			ViewedNetworkDrawsDerivePyploter=None
		
			"""
			#Check
			if self.PredictedNetworkDerivePredicterVariable.PredictingStationaryBool:

				#get
				ViewedPopulationDrawsDerivePyploter=self.PredictedAgentDerivePredicterVariable.getTeamer(
						'Panels'
					).getManager(
						'Run'
					).getTeamer(
						'Charts'
					).getManager(
						Recorder.RecordPrefixStr+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr
					).getTeamer(
						'Draws'
					)

				#/##################/#
				# view at the population scale
				#

				#debug
				self.debug(
					[
						'We add the stationary estimation view',
						('self.',self,[
								'PredictedStationaryStateMonitorVariable'
							])
					]
				)
				
				#set
				ViewedManagementStr='Stationary'

				#get
				ViewedSampleDeriveBrianer=self.PredictedAgentDerivePredicterVariable.TeamDict[
					'Traces'
				].ManagementDict[
					Recorder.RecordPrefixStr+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr
				].TeamDict[
					'Samples'
				].ManagementDict[
					'Default'
				]

				#debug
				self.debug(
					[
						('ViewedSampleDeriveBrianer.',ViewedSampleDeriveBrianer,[
							'RecordingLabelVariable'
						])
					]
				)

				#add
				ViewedPopulationDrawsDerivePyploter.getManager(
						ViewedManagementStr
					).PyplotingDrawVariable=map(
						lambda __IndexInt,__RecordingIndexInt:
						(	
							'plot',
							{
								'#liarg':[
									self.PredictedStationaryStateMonitorVariable.t,
									self.PredictedStationaryStateMonitorVariable.r0[
										__IndexInt,:
									]
								],
								'#kwarg':dict(
									{
										'linestyle':'--',
										'linewidth':10,
										'color':ViewedSampleDeriveBrianer.RecordedColorTuplesList[
											__IndexInt
										],
										'label':'$r_{0}^{'+str(__RecordingIndexInt)+'}$',
										'alpha':0.1
									}
								)
							}	
						),
						xrange(len(ViewedSampleDeriveBrianer.RecordingLabelVariable)),
						ViewedSampleDeriveBrianer.RecordingLabelVariable
					)

				#/##################/#
				# view at the network scale
				#

				ViewedNetworkChartsDerivePyploter=self.BrianedParentNetworkDeriveBrianerVariable.getTeamer(
					'Panels'
				).getManager(
					'Run'
				).getTeamer(
					'Charts'
				)

				#set
				PredictedManagementTagStr=self.PredictedAgentDerivePredicterVariable.ManagementTagStr+'_'+Recorder.RecordPrefixStr+self.PredictedAgentDerivePredicterVariable.LeakedSymbolStr

				#debug
				self.debug(
					[
						'ViewedNetworkChartsDerivePyploter is '+str(
							ViewedNetworkChartsDerivePyploter
						),
						"PredictedManagementTagStr is "+PredictedManagementTagStr
					]
				)

				
				#alias
				ViewedNetworkChartDerivePyploter=ViewedNetworkChartsDerivePyploter.getManager(
					PredictedManagementTagStr
				)

				#get
				ViewedNetworkDrawsDerivePyploter=ViewedNetworkChartDerivePyploter.getTeamer(
					'Draws'
				)

				#get
				ViewedNetworkDrawDerivePyploter=ViewedNetworkDrawsDerivePyploter.getManager(
						ViewedManagementStr
					)

				#set
				ViewedNetworkDrawDerivePyploter.PyplotingDrawVariable=ViewedPopulationDrawsDerivePyploter.ManagementDict[
						ViewedManagementStr
					].PyplotingDrawVariable

				#set
				if ViewedNetworkChartDerivePyploter.PyplotingLegendDict==None:
					ViewedNetworkChartDerivePyploter.PyplotingLegendDict={'ncol':2}
				else:
					ViewedNetworkChartDerivePyploter.PyplotingLegendDict['ncol']=2
				
			"""

	"""
	def pyplotFigure(self):

		#debug
		'''
		self.debug(
			[
				'We pyplot figure predict here'
			]
		)
		'''


		#Check
		if self.PredictedNetworkDerivePredicterVariable.PredictingInteractionStr=="Spike":

			#debug
			'''
			self.debug(
				[
					"It it a spike model, we make bigger the size",
					('self.',self,[
							'PyplotingShapeVariable'
						])
				]
			)
			'''

			#add
			self.PyplotingGridVariable=(
				self.PyplotingGridVariable[0]+15,
				self.PyplotingGridVariable[1]
			)

		#call the base
		BaseClass.pyplotFigure(self)
	"""

#</DefineClass>

#</DefineLocals>
Leaker.LeakersStructurerClass.ManagingValueClass=PredicterClass
#<DefineLocals>

#</DefinePrint>
PredicterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PredictingSensorUnitsInt',
		'PredictingAgentUnitsInt',
		'PredictingDaleBool',
		'PredictingDynamicBool',
		'PredictingJacobianVariable',
		'PredictingEncodPerturbStdFloat',
		'PredictingEncodWeightVariable',
		'PredictingCommandVariable',
		'PredictingRateCostVariable',
		'PredictingRateTransferVariable',
		'PredictingAgentTimeFloat',
		'PredictingAgentThresholdVariable',
		'PredictingAgentRestVariable',
		'PredictingAgentResetVariable',
		'PredictingAgentNoiseVariable',
		'PredictingAgentRefractoryVariable',
		'PredictingFastSymmetryFloat',
		'PredictingSlowPerturbStdFloat',
		'PredictingDecoderVariable',
		'PredictingDecoderMeanVariable',
		'PredictingDecoderStdFloat',
		'PredictingDecoderSparseFloat',
		'PredictingDecoderTimeFloat',
		'PredictingDecoderRecordVariable',
		'PredictingEncodPlasticBool',
		'PredictingSpikeRecordVariable',
		'PredictingFastPerturbStdFloat',
		'PredictingInteractionStr',
		'PredictingFastPlasticBool',
		'PredictingFastLearnRateFloat',
		'PredictingFastWeightVariable',
		'PredictingDelayFloat',
		'PredictingStationaryBool',
		'PredictedDynamicDict',
		'PredictedSensorJacobianFloatsArray',
		'PredictedDecoderFloatsArray',
		'PredictedFastFloatsArray',
		'PredictedThresholdFloatsArray',
		'PredictedSlowFloatsArray',
		'PredictedParentSingularStr',
		'PredictedSlowBool',
		'PredictedDelayFloatsArray',
		'PredictedDecoderInverseFloatsArray',
		'PredictedSensorDerivePredicterVariable',
		'PredictedAgentDerivePredicterVariable',
		'PredictedDecoderDerivePredicterVariable',
		'PredictedNetworkDerivePredicterVariable'
	]
)
#<DefinePrint>